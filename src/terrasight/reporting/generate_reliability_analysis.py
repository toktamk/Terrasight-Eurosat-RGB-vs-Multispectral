from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from terrasight.data.band_registry import EUROSAT_CLASSES


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def probability_columns(df: pd.DataFrame) -> list[str]:
    return [f"prob_{class_name}" for class_name in EUROSAT_CLASSES]


def compute_ece(df: pd.DataFrame, n_bins: int = 10) -> tuple[float, float, pd.DataFrame]:
    bins = np.linspace(0.0, 1.0, n_bins + 1)

    rows = []
    ece = 0.0
    mce = 0.0

    for i in range(n_bins):
        lower = bins[i]
        upper = bins[i + 1]

        if i == n_bins - 1:
            mask = (df["confidence"] >= lower) & (df["confidence"] <= upper)
        else:
            mask = (df["confidence"] >= lower) & (df["confidence"] < upper)

        bin_df = df[mask]

        if bin_df.empty:
            accuracy = 0.0
            confidence = 0.0
            count = 0
        else:
            accuracy = float(bin_df["correct"].mean())
            confidence = float(bin_df["confidence"].mean())
            count = len(bin_df)

        gap = abs(accuracy - confidence)
        weight = count / len(df)

        ece += weight * gap
        mce = max(mce, gap)

        rows.append(
            {
                "bin_lower": lower,
                "bin_upper": upper,
                "count": count,
                "accuracy": accuracy,
                "confidence": confidence,
                "gap": gap,
            }
        )

    return ece, mce, pd.DataFrame(rows)


def compute_brier_score(df: pd.DataFrame) -> float:
    prob_cols = probability_columns(df)
    probs = df[prob_cols].to_numpy()

    labels = df["true_label"].to_numpy()
    one_hot = np.zeros_like(probs)
    one_hot[np.arange(len(labels)), labels] = 1.0

    return float(np.mean(np.sum((probs - one_hot) ** 2, axis=1)))


def plot_reliability_curve(calib_df: pd.DataFrame, title: str, output_path: Path) -> None:
    plt.figure(figsize=(6, 6))
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.plot(calib_df["confidence"], calib_df["accuracy"], marker="o")
    plt.xlabel("Mean confidence")
    plt.ylabel("Accuracy")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_confidence_histogram(df: pd.DataFrame, title: str, output_path: Path) -> None:
    plt.figure(figsize=(7, 5))
    plt.hist(df["confidence"], bins=20)
    plt.xlabel("Prediction confidence")
    plt.ylabel("Number of samples")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def process_file(path: Path, output_figures: Path) -> dict:
    df = pd.read_csv(path)
    model_name = path.stem.replace("_probabilities", "")

    ece, mce, calib_df = compute_ece(df)
    brier = compute_brier_score(df)

    calib_path = output_figures / f"{model_name}_reliability_diagram.png"
    hist_path = output_figures / f"{model_name}_confidence_histogram.png"

    plot_reliability_curve(
        calib_df,
        title=f"{model_name} reliability diagram",
        output_path=calib_path,
    )

    plot_confidence_histogram(
        df,
        title=f"{model_name} confidence histogram",
        output_path=hist_path,
    )

    calib_df.to_csv(output_figures / f"{model_name}_calibration_bins.csv", index=False)

    return {
        "model": model_name,
        "accuracy": float(df["correct"].mean()),
        "mean_confidence": float(df["confidence"].mean()),
        "ece": ece,
        "mce": mce,
        "brier_score": brier,
        "reliability_diagram": str(calib_path),
        "confidence_histogram": str(hist_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="reports/tables/probabilities")
    parser.add_argument("--output-dir", default="reports/figures/reliability")
    parser.add_argument("--summary", default="reports/tables/reliability_summary.csv")
    args = parser.parse_args()

    project_root = get_project_root()
    input_dir = project_root / args.input_dir
    output_dir = project_root / args.output_dir
    summary_path = project_root / args.summary

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for path in sorted(input_dir.glob("*_probabilities.csv")):
        rows.append(process_file(path, output_dir))

    pd.DataFrame(rows).to_csv(summary_path, index=False)

    print(f"Saved: {summary_path}")
    print(f"Saved reliability figures to: {output_dir}")


if __name__ == "__main__":
    main()