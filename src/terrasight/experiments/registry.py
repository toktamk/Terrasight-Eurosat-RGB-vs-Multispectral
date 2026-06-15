from __future__ import annotations

from pathlib import Path
import pandas as pd


REGISTRY_COLUMNS = [
    "timestamp",
    "experiment_id",
    "version",
    "input_type",
    "model",
    "input_channels",
    "bands",
    "epochs",
    "accuracy",
    "macro_f1",
    "weighted_f1",
    "balanced_accuracy",
    "run_directory",
]


def create_registry_if_missing(
    registry_path: str | Path,
) -> None:
    registry_path = Path(registry_path)

    if registry_path.exists():
        return

    df = pd.DataFrame(columns=REGISTRY_COLUMNS)
    df.to_csv(registry_path, index=False)


def load_registry(
    registry_path: str | Path,
) -> pd.DataFrame:
    create_registry_if_missing(registry_path)
    return pd.read_csv(registry_path)


def save_registry(
    dataframe: pd.DataFrame,
    registry_path: str | Path,
) -> None:
    dataframe.to_csv(registry_path, index=False)