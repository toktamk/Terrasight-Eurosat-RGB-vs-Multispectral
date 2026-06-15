import pandas as pd

from terrasight.reporting.comparison import (
    add_rgb_vs_ms_delta,
    build_comparison_table,
)


def test_build_comparison_table() -> None:
    registry = pd.DataFrame(
        [
            {
                "experiment_id": "rgb",
                "version": "v1",
                "input_type": "rgb",
                "model": "resnet18",
                "input_channels": 3,
                "bands": "B4,B3,B2",
                "epochs": 1,
                "accuracy": 0.90,
                "macro_f1": 0.89,
                "weighted_f1": 0.90,
                "balanced_accuracy": 0.88,
                "run_directory": "results/v1/rgb",
            },
            {
                "experiment_id": "ms",
                "version": "v1",
                "input_type": "multispectral",
                "model": "resnet18",
                "input_channels": 13,
                "bands": "B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B10,B11,B12",
                "epochs": 1,
                "accuracy": 0.95,
                "macro_f1": 0.94,
                "weighted_f1": 0.95,
                "balanced_accuracy": 0.93,
                "run_directory": "results/v1/ms",
            },
        ]
    )

    comparison = build_comparison_table(registry)

    assert comparison.shape[0] == 2
    assert comparison.iloc[0]["experiment_id"] == "ms"


def test_add_rgb_vs_ms_delta() -> None:
    comparison = pd.DataFrame(
        [
            {
                "experiment_id": "rgb",
                "version": "v1",
                "input_type": "rgb",
                "model": "resnet18",
                "input_channels": 3,
                "bands": "B4,B3,B2",
                "epochs": 1,
                "accuracy": 0.90,
                "macro_f1": 0.89,
                "weighted_f1": 0.90,
                "balanced_accuracy": 0.88,
                "run_directory": "results/v1/rgb",
            },
            {
                "experiment_id": "ms",
                "version": "v1",
                "input_type": "multispectral",
                "model": "resnet18",
                "input_channels": 13,
                "bands": "full_13",
                "epochs": 1,
                "accuracy": 0.95,
                "macro_f1": 0.94,
                "weighted_f1": 0.95,
                "balanced_accuracy": 0.93,
                "run_directory": "results/v1/ms",
            },
        ]
    )

    output = add_rgb_vs_ms_delta(
        comparison=comparison,
        rgb_experiment_id="rgb",
        ms_experiment_id="ms",
        metric="macro_f1",
    )

    delta_value = output.loc[
        output["experiment_id"] == "ms",
        "delta_vs_rgb_macro_f1",
    ].iloc[0]

    assert abs(delta_value - 0.05) < 1e-8