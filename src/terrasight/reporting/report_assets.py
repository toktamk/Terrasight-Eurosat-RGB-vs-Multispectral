from __future__ import annotations

import argparse
import json
from pathlib import Path

from terrasight.reporting.figures import save_metric_bar_chart, save_training_curve
from terrasight.reporting.tables import (
    load_metrics,
    metrics_to_table,
    save_table,
)


def generate_single_run_assets(
    run_dir: str | Path,
    experiment_name: str | None = None,
    output_dir: str | Path = "reports",
) -> None:
    """Generate report-ready assets for a single run."""

    run_dir = Path(run_dir)
    output_dir = Path(output_dir)

    metrics_path = run_dir / "metrics.json"
    history_path = run_dir / "history.json"

    if experiment_name is None:
        experiment_name = run_dir.name

    metrics = load_metrics(metrics_path)
    table = metrics_to_table(metrics, experiment_name=experiment_name)

    save_table(
        table=table,
        output_path=output_dir / "tables" / f"{experiment_name}_metrics.csv",
    )

    save_metric_bar_chart(
        table=table,
        metric="macro_f1",
        output_path=output_dir / "figures" / f"{experiment_name}_macro_f1.png",
    )

    if history_path.exists():
        with history_path.open("r", encoding="utf-8") as file:
            history = json.load(file)

        save_training_curve(
            history=history,
            output_path=output_dir / "figures" / f"{experiment_name}_training_curve.png",
            metric="macro_f1",
        )

    print("Report assets generated")
    print(f"Output directory: {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TerraSight report assets.")
    parser.add_argument("--run-dir", required=True, help="Path to run directory.")
    parser.add_argument("--experiment-name", default=None, help="Optional display name.")
    parser.add_argument("--output-dir", default="reports", help="Output report directory.")
    args = parser.parse_args()

    generate_single_run_assets(
        run_dir=args.run_dir,
        experiment_name=args.experiment_name,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()