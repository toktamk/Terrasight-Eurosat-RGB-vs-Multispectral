from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def load_metrics(metrics_path: str | Path) -> dict[str, Any]:
    """Load metrics JSON file."""

    metrics_path = Path(metrics_path)

    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {metrics_path}")

    with metrics_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def metrics_to_table(
    metrics: dict[str, Any],
    experiment_name: str,
) -> pd.DataFrame:
    """Convert metrics dictionary to one-row table."""

    row = {
        "experiment": experiment_name,
        "accuracy": metrics.get("accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "weighted_f1": metrics.get("weighted_f1"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "loss": metrics.get("loss"),
    }

    return pd.DataFrame([row])


def build_comparison_table(
    rows: list[pd.DataFrame],
) -> pd.DataFrame:
    """Build experiment comparison table."""

    if not rows:
        raise ValueError("No rows provided for comparison table.")

    return pd.concat(rows, ignore_index=True)


def save_table(
    table: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """Save table as CSV."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table.to_csv(output_path, index=False)


def load_registry_table(
    registry_path: str | Path = "experiments/registry.csv",
) -> pd.DataFrame:
    """Load experiment registry CSV."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        raise FileNotFoundError(f"Registry not found: {registry_path}")

    return pd.read_csv(registry_path)