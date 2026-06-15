import json

import pandas as pd

from terrasight.reporting.figures import save_metric_bar_chart, save_training_curve
from terrasight.reporting.report_assets import generate_single_run_assets
from terrasight.reporting.tables import build_comparison_table, load_metrics, metrics_to_table


def test_metrics_to_table() -> None:
    metrics = {
        "accuracy": 0.9,
        "macro_f1": 0.8,
        "weighted_f1": 0.85,
        "balanced_accuracy": 0.82,
        "loss": 0.3,
    }

    table = metrics_to_table(metrics, experiment_name="test_exp")

    assert table.shape[0] == 1
    assert table.loc[0, "experiment"] == "test_exp"
    assert table.loc[0, "accuracy"] == 0.9


def test_build_comparison_table() -> None:
    row1 = pd.DataFrame([{"experiment": "rgb", "accuracy": 0.9}])
    row2 = pd.DataFrame([{"experiment": "ms", "accuracy": 0.95}])

    table = build_comparison_table([row1, row2])

    assert table.shape[0] == 2


def test_load_metrics(tmp_path) -> None:
    metrics_path = tmp_path / "metrics.json"

    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump({"accuracy": 0.9}, file)

    metrics = load_metrics(metrics_path)

    assert metrics["accuracy"] == 0.9


def test_save_metric_bar_chart(tmp_path) -> None:
    table = pd.DataFrame(
        [
            {"experiment": "rgb", "macro_f1": 0.8},
            {"experiment": "ms", "macro_f1": 0.9},
        ]
    )

    output_path = tmp_path / "figures" / "bar.png"

    save_metric_bar_chart(
        table=table,
        metric="macro_f1",
        output_path=output_path,
    )

    assert output_path.exists()


def test_save_training_curve(tmp_path) -> None:
    history = [
        {"epoch": 1, "macro_f1": 0.7},
        {"epoch": 2, "macro_f1": 0.8},
    ]

    output_path = tmp_path / "figures" / "curve.png"

    save_training_curve(
        history=history,
        output_path=output_path,
        metric="macro_f1",
    )

    assert output_path.exists()


def test_generate_single_run_assets(tmp_path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    with (run_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(
            {
                "accuracy": 0.9,
                "macro_f1": 0.8,
                "weighted_f1": 0.85,
                "balanced_accuracy": 0.82,
                "loss": 0.3,
            },
            file,
        )

    with (run_dir / "history.json").open("w", encoding="utf-8") as file:
        json.dump(
            [
                {"epoch": 1, "macro_f1": 0.7},
                {"epoch": 2, "macro_f1": 0.8},
            ],
            file,
        )

    output_dir = tmp_path / "reports"

    generate_single_run_assets(
        run_dir=run_dir,
        experiment_name="test_exp",
        output_dir=output_dir,
    )

    assert (output_dir / "tables" / "test_exp_metrics.csv").exists()
    assert (output_dir / "figures" / "test_exp_macro_f1.png").exists()
    assert (output_dir / "figures" / "test_exp_training_curve.png").exists()