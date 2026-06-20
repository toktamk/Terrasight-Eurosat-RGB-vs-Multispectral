from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tifffile


BANDS = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8A", "B9", "B10", "B11", "B12"]


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def image_signature(path: Path) -> np.ndarray:
    image = tifffile.imread(path).astype(np.float32)

    if image.ndim != 3:
        raise ValueError(f"Expected 3D multispectral image, got {image.shape}: {path}")

    if image.shape[0] == 13:
        image = np.moveaxis(image, 0, -1)

    if image.shape[-1] != 13:
        raise ValueError(f"Expected 13 bands, got {image.shape}: {path}")

    return image.reshape(-1, 13).mean(axis=0)


def collect_signatures(data_dir: Path, max_per_class: int | None = None) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    class_dirs = sorted([p for p in data_dir.iterdir() if p.is_dir()])

    for class_dir in class_dirs:
        files = sorted(class_dir.glob("*.tif")) + sorted(class_dir.glob("*.tiff"))
        if max_per_class is not None:
            files = files[:max_per_class]

        for path in files:
            sig = image_signature(path)
            row: dict[str, object] = {"class": class_dir.name, "path": str(path)}
            row.update({band: float(value) for band, value in zip(BANDS, sig)})
            rows.append(row)

    if not rows:
        raise ValueError(f"No TIFF images found in {data_dir}")

    return pd.DataFrame(rows)


def regularized_covariance(values: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    cov = np.cov(values, rowvar=False)
    return cov + np.eye(cov.shape[0]) * eps


def bhattacharyya_distance(x1: np.ndarray, x2: np.ndarray) -> float:
    mu1 = x1.mean(axis=0)
    mu2 = x2.mean(axis=0)

    cov1 = regularized_covariance(x1)
    cov2 = regularized_covariance(x2)
    cov_avg = (cov1 + cov2) / 2.0

    diff = mu2 - mu1

    inv_cov_avg = np.linalg.pinv(cov_avg)

    term1 = 0.125 * float(diff.T @ inv_cov_avg @ diff)

    det_cov_avg = max(float(np.linalg.det(cov_avg)), 1e-12)
    det_cov1 = max(float(np.linalg.det(cov1)), 1e-12)
    det_cov2 = max(float(np.linalg.det(cov2)), 1e-12)

    term2 = 0.5 * np.log(det_cov_avg / np.sqrt(det_cov1 * det_cov2))

    return float(term1 + term2)


def spectral_angle_mapper(v1: np.ndarray, v2: np.ndarray) -> float:
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom == 0:
        return 0.0

    cosine = np.clip(float(np.dot(v1, v2) / denom), -1.0, 1.0)
    return float(np.degrees(np.arccos(cosine)))


def pairwise_analysis(signatures: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    classes = sorted(signatures["class"].unique())
    feature_df = signatures[BANDS]

    mean_rows = []
    for cls in classes:
        cls_values = signatures.loc[signatures["class"] == cls, BANDS].to_numpy()
        mean_rows.append({"class": cls, **dict(zip(BANDS, cls_values.mean(axis=0)))})
    class_means = pd.DataFrame(mean_rows)

    bhatta_matrix = pd.DataFrame(0.0, index=classes, columns=classes)
    sam_matrix = pd.DataFrame(0.0, index=classes, columns=classes)

    pair_rows = []

    for cls_a, cls_b in combinations(classes, 2):
        x1 = signatures.loc[signatures["class"] == cls_a, BANDS].to_numpy()
        x2 = signatures.loc[signatures["class"] == cls_b, BANDS].to_numpy()

        mean_a = x1.mean(axis=0)
        mean_b = x2.mean(axis=0)

        bd = bhattacharyya_distance(x1, x2)
        sam = spectral_angle_mapper(mean_a, mean_b)

        bhatta_matrix.loc[cls_a, cls_b] = bd
        bhatta_matrix.loc[cls_b, cls_a] = bd

        sam_matrix.loc[cls_a, cls_b] = sam
        sam_matrix.loc[cls_b, cls_a] = sam

        pair_rows.append(
            {
                "class_a": cls_a,
                "class_b": cls_b,
                "bhattacharyya_distance": bd,
                "spectral_angle_degrees": sam,
            }
        )

    pair_df = pd.DataFrame(pair_rows)
    return class_means, bhatta_matrix, sam_matrix, pair_df


def save_heatmap(matrix: pd.DataFrame, output_path: Path, title: str, colorbar_label: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(matrix.to_numpy())

    ax.set_xticks(np.arange(len(matrix.columns)))
    ax.set_yticks(np.arange(len(matrix.index)))
    ax.set_xticklabels(matrix.columns, rotation=45, ha="right")
    ax.set_yticklabels(matrix.index)

    ax.set_title(title)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(colorbar_label)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def save_pair_barplot(df: pd.DataFrame, value_col: str, output_path: Path, title: str, ylabel: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plot_df = df.copy()
    plot_df["pair"] = plot_df["class_a"] + " vs " + plot_df["class_b"]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(plot_df["pair"], plot_df[value_col])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate spectral separability analysis using Bhattacharyya distance and Spectral Angle Mapper."
    )
    parser.add_argument(
        "--data-dir",
        default="data/raw/multispectral",
        help="Path to EuroSAT multispectral class folders.",
    )
    parser.add_argument(
        "--tables-dir",
        default="reports/tables/spectral_analysis",
        help="Output directory for CSV tables.",
    )
    parser.add_argument(
        "--figures-dir",
        default="reports/figures/spectral_analysis",
        help="Output directory for figures.",
    )
    parser.add_argument(
        "--max-per-class",
        type=int,
        default=None,
        help="Optional limit on number of images per class for faster testing.",
    )
    args = parser.parse_args()

    project_root = get_project_root()

    data_dir = project_root / args.data_dir
    tables_dir = project_root / args.tables_dir
    figures_dir = project_root / args.figures_dir

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    signatures = collect_signatures(data_dir=data_dir, max_per_class=args.max_per_class)
    signatures.to_csv(tables_dir / "image_spectral_signatures.csv", index=False)

    class_means, bhatta_matrix, sam_matrix, pair_df = pairwise_analysis(signatures)

    class_means.to_csv(tables_dir / "class_mean_signatures.csv", index=False)
    bhatta_matrix.to_csv(tables_dir / "bhattacharyya_distances.csv")
    sam_matrix.to_csv(tables_dir / "spectral_angles.csv")
    pair_df.to_csv(tables_dir / "pairwise_spectral_separability.csv", index=False)

    most_bhatta = pair_df.sort_values("bhattacharyya_distance", ascending=False).head(10)
    least_bhatta = pair_df.sort_values("bhattacharyya_distance", ascending=True).head(10)
    most_sam = pair_df.sort_values("spectral_angle_degrees", ascending=False).head(10)
    least_sam = pair_df.sort_values("spectral_angle_degrees", ascending=True).head(10)

    most_bhatta.to_csv(tables_dir / "most_separable_pairs_bhattacharyya.csv", index=False)
    least_bhatta.to_csv(tables_dir / "least_separable_pairs_bhattacharyya.csv", index=False)
    most_sam.to_csv(tables_dir / "most_separable_pairs_sam.csv", index=False)
    least_sam.to_csv(tables_dir / "least_separable_pairs_sam.csv", index=False)

    save_heatmap(
        bhatta_matrix,
        figures_dir / "bhattacharyya_heatmap.png",
        "Pairwise Spectral Separability: Bhattacharyya Distance",
        "Bhattacharyya Distance",
    )

    save_heatmap(
        sam_matrix,
        figures_dir / "spectral_angle_heatmap.png",
        "Pairwise Spectral Separability: Spectral Angle Mapper",
        "Spectral Angle (degrees)",
    )

    save_pair_barplot(
        least_bhatta,
        "bhattacharyya_distance",
        figures_dir / "top10_least_separable_pairs_bhattacharyya.png",
        "Top 10 Least Separable Class Pairs: Bhattacharyya Distance",
        "Bhattacharyya Distance",
    )

    save_pair_barplot(
        most_bhatta,
        "bhattacharyya_distance",
        figures_dir / "top10_most_separable_pairs_bhattacharyya.png",
        "Top 10 Most Separable Class Pairs: Bhattacharyya Distance",
        "Bhattacharyya Distance",
    )

    save_pair_barplot(
        least_sam,
        "spectral_angle_degrees",
        figures_dir / "top10_most_similar_pairs_sam.png",
        "Top 10 Most Spectrally Similar Class Pairs: SAM",
        "Spectral Angle (degrees)",
    )

    save_pair_barplot(
        most_sam,
        "spectral_angle_degrees",
        figures_dir / "top10_most_different_pairs_sam.png",
        "Top 10 Most Spectrally Different Class Pairs: SAM",
        "Spectral Angle (degrees)",
    )

    print(f"Saved tables to: {tables_dir}")
    print(f"Saved figures to: {figures_dir}")


if __name__ == "__main__":
    main()