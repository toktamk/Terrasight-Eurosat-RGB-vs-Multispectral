from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import pandas as pd

from terrasight.experiments.registry import (
    create_registry_if_missing,
    load_registry,
    save_registry,
)


def register_experiment(
    config: dict,
    metrics_file: str | Path,
    run_dir: str | Path,
    registry_path: str | Path = "experiments/registry.csv",
) -> None:

    create_registry_if_missing(registry_path)

    metrics_file = Path(metrics_file)

    with metrics_file.open("r", encoding="utf-8") as file:
        metrics = json.load(file)

    row = {
        "timestamp": datetime.now().isoformat(),
        "experiment_id": config["experiment"]["id"],
        "version": config["experiment"]["version"],
        "input_type": config["data"]["input_type"],
        "model": config["model"]["name"],
        "input_channels": config["model"]["input_channels"],
        "bands": ",".join(config["data"]["bands"]),
        "epochs": config["training"]["epochs"],
        "accuracy": metrics.get("accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "weighted_f1": metrics.get("weighted_f1"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "run_directory": str(run_dir),
    }

    registry = load_registry(registry_path)

    new_row = pd.DataFrame([row])

    if registry.empty:
        registry = new_row
    else:
        registry = pd.concat(
            [registry, new_row],
            ignore_index=True,
        )

    save_registry(registry, registry_path)