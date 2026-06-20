from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from tqdm import tqdm


SENTINEL2_BANDS = [
    "B1", "B2", "B3", "B4", "B5", "B6", "B7",
    "B8", "B8A", "B9", "B10", "B11", "B12"
]


def read_multispectral_image(path: Path) -> np.ndarray:
    with rasterio.open(path) as src:
        image = src.read().astype(np.float32)
    return image


def compute_image_signature(image: np.ndarray) -> np.ndarray:
    # image shape: [bands, height, width]
    return image.reshape(image.shape[0], -1).mean(axis=1)


def collect_class_signatures(
    data_dir: Path,
    max_images_per_class: int | None = None,
) -> pd.DataFrame:
    rows = []

    class_dirs = sorted([p for p in data_dir.iterdir() if p.is_dir()])

    for class_dir in class_dirs:
        image_paths = sorted(
            list(class_dir.glob("*.tif"))
            + list(class_dir.glob("*.tiff"))
        )

        if max_images_per_class is not None:
            image_paths = image_paths[:max_images_per_class]

        for image_path in tqdm(image_paths, desc=f"Processing {class_dir.name}"):
            try:
                image = read_multispectral_image(image_path)

                if image.shape[0] != len(SENTINEL2_BANDS):
                    print(
                        f"Skipping {image_path}: expected 13 bands, "
                        f"found {image.shape[0]}"
                    )
                    continue

                signature = compute_image_signature(image)

                row = {
                    "class": class_dir.name,
                    "image": image_path.name,
                }

                for band_name, value in zip(SENTINEL2_BANDS, signature):
                    row[band_name] = float(value)

                rows.append(row)

            except Exception as exc:
                print(f"Failed to process {image_path}: {exc}")

    return pd.DataFrame(rows)


def summarize_signatures(df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []

    for class_name, group in df.groupby("class"):
        for band in SENTINEL2_BANDS:
            values = group[band].to_numpy(dtype=np.float32)

            summary_rows.append(
                {
                    "class": class_name,
                    "band": band,
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "median": float(np.median(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                }
            )

    return pd.DataFrame(summary_rows)


def plot_per_class_signatures(
    summary_df: pd.DataFrame,
    output_path: Path,
    title: str,
) -> None:
    plt.figure(figsize=(14, 8))

    for class_name, group in summary_df.groupby("class"):
        group = group.set_index("band").loc[SENTINEL2_BANDS].reset_index()

        x = np.arange(len(SENTINEL2_BANDS))
        mean = group["mean"].to_numpy(dtype=np.float32)
        std = group["std"].to_numpy(dtype=np.float32)

        plt.plot(x, mean, marker="o", linewidth=2, label=class_name)
        plt.fill_between(x, mean - std, mean + std, alpha=0.12)

    plt.xticks(np.arange(len(SENTINEL2_BANDS)), SENTINEL2_BANDS)
    plt.xlabel("Sentinel-2 spectral band")
    plt.ylabel("Mean reflectance / pixel intensity")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_individual_class_signatures(
    summary_df: pd.DataFrame,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for class_name, group in summary_df.groupby("class"):
        group = group.set_index("band").loc[SENTINEL2_BANDS].reset_index()

        x = np.arange(len(SENTINEL2_BANDS))
        mean = group["mean"].to_numpy(dtype=np.float32)
        std = group["std"].to_numpy(dtype=np.float32)

        plt.figure(figsize=(10, 6))
        plt.plot(x, mean, marker="o", linewidth=2)
        plt.fill_between(x, mean - std, mean + std, alpha=0.2)

        plt.xticks(x, SENTINEL2_BANDS)
        plt.xlabel("Sentinel-2 spectral band")
        plt.ylabel("Mean reflectance / pixel intensity")
        plt.title(f"Spectral signature: {class_name}")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        output_path = output_dir / f"{class_name}_spectral_signature.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate per-class Sentinel-2 spectral signature plots."
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw/multispectral"),
        help="Path to multispectral EuroSAT class folders.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports/figures/spectral_signatures"),
        help="Directory where plots and tables are saved.",
    )

    parser.add_argument(
        "--max-images-per-class",
        type=int,
        default=None,
        help="Optional maximum number of images per class.",
    )

    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    signatures_df = collect_class_signatures(
        data_dir=args.data_dir,
        max_images_per_class=args.max_images_per_class,
    )

    if signatures_df.empty:
        raise RuntimeError("No valid multispectral images were processed.")

    summary_df = summarize_signatures(signatures_df)

    signatures_csv = args.output_dir / "spectral_signatures_per_image.csv"
    summary_csv = args.output_dir / "spectral_signatures_summary.csv"

    signatures_df.to_csv(signatures_csv, index=False)
    summary_df.to_csv(summary_csv, index=False)

    plot_per_class_signatures(
        summary_df=summary_df,
        output_path=args.output_dir / "per_class_spectral_signatures.png",
        title="Per-class Sentinel-2 spectral signatures",
    )

    plot_individual_class_signatures(
        summary_df=summary_df,
        output_dir=args.output_dir / "individual_classes",
    )

    print(f"Saved per-image signatures to: {signatures_csv}")
    print(f"Saved summary table to: {summary_csv}")
    print(f"Saved figures to: {args.output_dir}")


if __name__ == "__main__":
    main()