import json
from pathlib import Path

from terrasight.experiments.experiment_tracker import register_experiment


def test_registry_append(tmp_path):

    metrics_path = tmp_path / "metrics.json"

    metrics = {
        "accuracy": 0.9,
        "macro_f1": 0.8,
        "weighted_f1": 0.85,
        "balanced_accuracy": 0.82,
    }

    with metrics_path.open("w") as f:
        json.dump(metrics, f)

    config = {
        "experiment": {
            "id": "test",
            "version": "v1",
        },
        "data": {
            "input_type": "rgb",
            "bands": ["B4", "B3", "B2"],
        },
        "model": {
            "name": "resnet18",
            "input_channels": 3,
        },
        "training": {
            "epochs": 1,
        },
    }

    registry_path = tmp_path / "registry.csv"

    register_experiment(
        config=config,
        metrics_file=metrics_path,
        run_dir=tmp_path,
        registry_path=registry_path,
    )

    assert registry_path.exists()