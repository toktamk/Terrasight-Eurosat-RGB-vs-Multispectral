from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_METRICS = [
    "accuracy",
    "macro_f1",
    "weighted_f1",
    "balanced_accuracy",
]


def load_registry(
    registry_path: str | Path = "experiments/registry.csv",
) -> pd.DataFrame:
    """Load experiment registry."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")

    return pd.read_csv(registry_path)


def build_comparison_table(
    registry: pd.DataFrame,
    metrics: list[str] | None = None,
) -> pd.DataFrame:
    """Build compact experiment comparison table from registry."""

    metrics = metrics or DEFAULT_METRICS

    required_columns = [
        "experiment_id",
        "version",
        "input_type",
        "model",
        "input_channels",
        "bands",
        "epochs",
        "run_directory",
        *metrics,
    ]

    missing = [column for column in required_columns if column not in registry.columns]

    if missing:
        raise ValueError(f"Missing required registry columns: {missing}")

    comparison = registry[required_columns].copy()

    sort_columns = [metric for metric in ["macro_f1", "accuracy"] if metric in comparison.columns]

    if sort_columns:
        comparison = comparison.sort_values(
            by=sort_columns,
            ascending=False,
        )

    return comparison.reset_index(drop=True)


def add_rgb_vs_ms_delta(
    comparison: pd.DataFrame,
    rgb_experiment_id: str,
    ms_experiment_id: str,
    metric: str = "macro_f1",
) -> pd.DataFrame:
    """Add absolute delta between one RGB and one multispectral experiment."""

    if metric not in comparison.columns:
        raise ValueError(f"Metric not found in comparison table: {metric}")

    rgb_rows = comparison[comparison["experiment_id"] == rgb_experiment_id]
    ms_rows = comparison[comparison["experiment_id"] == ms_experiment_id]

    if rgb_rows.empty:
        raise ValueError(f"RGB experiment not found: {rgb_experiment_id}")

    if ms_rows.empty:
        raise ValueError(f"Multispectral experiment not found: {ms_experiment_id}")

    rgb_score = float(rgb_rows.iloc[0][metric])
    ms_score = float(ms_rows.iloc[0][metric])
    delta = ms_score - rgb_score

    output = comparison.copy()
    output[f"delta_vs_rgb_{metric}"] = None

    output.loc[
        output["experiment_id"] == ms_experiment_id,
        f"delta_vs_rgb_{metric}",
    ] = delta

    return output


def save_comparison_table(
    comparison: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """Save comparison table."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    comparison.to_csv(output_path, index=False)


def generate_comparison_table(
    registry_path: str | Path = "experiments/registry.csv",
    output_path: str | Path = "reports/tables/comparison_table.csv",
) -> pd.DataFrame:
    """Generate and save comparison table from registry."""

    registry = load_registry(registry_path)
    comparison = build_comparison_table(registry)
    save_comparison_table(comparison, output_path)

    print("Comparison table generated")
    print(f"Output: {output_path}")

    return comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TerraSight experiment comparison table.")
    parser.add_argument(
        "--registry",
        default="experiments/registry.csv",
        help="Path to experiment registry CSV.",
    )
    parser.add_argument(
        "--output",
        default="reports/tables/comparison_table.csv",
        help="Output comparison table path.",
    )

    args = parser.parse_args()

    generate_comparison_table(
        registry_path=args.registry,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()