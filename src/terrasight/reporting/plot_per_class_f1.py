from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from terrasight.data.band_registry import EUROSAT_CLASSES


def plot_per_class_f1(
    input_csv: Path,
    output_path: Path,
    models: list[str] | None = None,
) -> None:
    df = pd.read_csv(input_csv)

    required = {"model", "class", "f1"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {input_csv}: {missing}")

    if models is not None:
        df = df[df["model"].isin(models)]

    pivot = df.pivot(index="class", columns="model", values="f1")
    pivot = pivot.reindex(EUROSAT_CLASSES)

    ax = pivot.plot(kind="bar", figsize=(14, 6), width=0.82)

    ax.set_title("Per-Class F1 Score Comparison")
    ax.set_xlabel("EuroSAT Class")
    ax.set_ylabel("F1 Score")
    ax.set_ylim(0.85, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved figure: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot per-class F1 comparison from classwise_comparison.csv."
    )

    parser.add_argument(
        "--input-csv",
        default="reports/tables/classwise_comparison.csv",
    )

    parser.add_argument(
        "--output",
        default="reports/figures/per_class_f1_comparison.png",
    )

    parser.add_argument(
        "--models",
        nargs="*",
        default=None,
        help="Optional list of model names to include.",
    )

    args = parser.parse_args()

    plot_per_class_f1(
        input_csv=Path(args.input_csv),
        output_path=Path(args.output),
        models=args.models,
    )


if __name__ == "__main__":
    main()