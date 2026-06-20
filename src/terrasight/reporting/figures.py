from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    confusion_matrix,
)

from terrasight.data.band_registry import EUROSAT_CLASSES

def save_metric_bar_chart(
    table: pd.DataFrame,
    metric: str,
    output_path: str | Path,
) -> None:
    """Save a bar chart for a selected metric from a comparison table."""
    if "experiment" not in table.columns:
        raise ValueError("Input table must contain an 'experiment' column.")

    if metric not in table.columns:
        raise ValueError(f"Metric column not found: {metric}")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(table["experiment"].astype(str), table[metric].astype(float))
    ax.set_xlabel("Experiment")
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} Comparison")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

def save_training_curve(
    history: list[dict[str, float]],
    output_path: str | Path,
    metric: str = "macro_f1",
) -> None:
    """Save a training curve for a selected metric from epoch history."""
    if not history:
        raise ValueError("History is empty.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    epochs = [row.get("epoch", idx + 1) for idx, row in enumerate(history)]

    if metric not in history[0]:
        raise ValueError(f"Metric not found in history: {metric}")

    values = [row[metric] for row in history]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(epochs, values, marker="o")
    ax.set_xlabel("Epoch")
    ax.set_ylabel(metric)
    ax.set_title(f"Training Curve: {metric}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

def load_json(path: str | Path) -> Any:
    """Load a JSON file."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def ensure_output_dir(output_dir: str | Path) -> Path:
    """Create output directory if it does not exist."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path


def make_safe_name(name: str) -> str:
    """Create a filesystem-safe output prefix."""

    return (
        name.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )


def load_history(run_dir: str | Path) -> pd.DataFrame | None:
    """Load training history if available."""

    history_path = Path(run_dir) / "history.json"

    if not history_path.exists():
        print(
            f"WARNING: history.json not found in {run_dir}. "
            "Skipping training-curve figures."
        )
        return None

    history = pd.DataFrame(load_json(history_path))

    required_columns = {
        "epoch",
        "train_loss",
        "loss",
        "macro_f1",
    }

    missing = required_columns - set(history.columns)

    if missing:
        print(
            f"WARNING: history.json in {run_dir} is missing columns "
            f"{sorted(missing)}. Skipping training-curve figures."
        )
        return None

    return history


def load_predictions(
    run_dir: str | Path,
) -> tuple[list[int], list[int]] | None:
    """Load prediction labels if predictions.json exists."""

    predictions_path = Path(run_dir) / "predictions.json"

    if not predictions_path.exists():
        print(
            f"WARNING: predictions.json not found in {run_dir}. "
            "Skipping confusion matrix and classwise report."
        )
        return None

    predictions = load_json(predictions_path)

    if "y_true" not in predictions or "y_pred" not in predictions:
        print(
            f"WARNING: Invalid predictions.json in {run_dir}. "
            "Expected keys: 'y_true' and 'y_pred'."
        )
        return None

    return predictions["y_true"], predictions["y_pred"]


def save_loss_curve(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> Path | None:
    """Save train/validation loss curve if history exists."""

    history = load_history(run_dir)

    if history is None:
        return None

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{make_safe_name(name)}_loss_curve.png"

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        history["epoch"],
        history["train_loss"],
        marker="o",
        label="Train loss",
    )

    ax.plot(
        history["epoch"],
        history["loss"],
        marker="o",
        label="Validation loss",
    )

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_title(f"Training and validation loss: {name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_macro_f1_curve(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> Path | None:
    """Save validation macro-F1 curve if history exists."""

    history = load_history(run_dir)

    if history is None:
        return None

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{make_safe_name(name)}_macro_f1_curve.png"

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        history["epoch"],
        history["macro_f1"],
        marker="o",
        label="Validation macro-F1",
    )

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Macro-F1")
    ax.set_title(f"Validation macro-F1: {name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_confusion_matrix(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
    normalize: str | None = None,
) -> Path | None:
    """Save confusion matrix if predictions exist."""

    predictions = load_predictions(run_dir)

    if predictions is None:
        return None

    y_true, y_pred = predictions

    output_dir = ensure_output_dir(output_dir)

    suffix = (
        "normalized_confusion_matrix"
        if normalize
        else "confusion_matrix"
    )

    output_path = output_dir / f"{make_safe_name(name)}_{suffix}.png"

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=list(range(len(EUROSAT_CLASSES))),
        normalize=normalize,
    )

    fig, ax = plt.subplots(figsize=(10, 10))

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=EUROSAT_CLASSES,
    )

    display.plot(
        ax=ax,
        xticks_rotation=45,
        colorbar=True,
        values_format=".2f" if normalize else "d",
    )

    ax.set_title(f"Confusion matrix: {name}")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_classwise_report(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> Path | None:
    """Save class-wise precision/recall/F1 report if predictions exist."""

    predictions = load_predictions(run_dir)

    if predictions is None:
        return None

    y_true, y_pred = predictions

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{make_safe_name(name)}_classwise_report.csv"

    report = classification_report(
        y_true,
        y_pred,
        labels=list(range(len(EUROSAT_CLASSES))),
        target_names=EUROSAT_CLASSES,
        output_dict=True,
        zero_division=0,
    )

    pd.DataFrame(report).T.to_csv(output_path)

    return output_path


def save_registry_comparison(
    registry_path: str | Path,
    output_dir: str | Path,
) -> Path | None:
    """Save model-performance comparison chart from registry.csv."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        print(
            f"WARNING: Registry file not found: {registry_path}. "
            "Skipping registry comparison."
        )
        return None

    registry = pd.read_csv(registry_path)

    required_columns = {
        "experiment_id",
        "accuracy",
        "macro_f1",
        "balanced_accuracy",
    }

    missing = required_columns - set(registry.columns)

    if missing:
        print(
            f"WARNING: Registry missing columns {sorted(missing)}. "
            "Skipping registry comparison."
        )
        return None

    df = registry[
        [
            "experiment_id",
            "accuracy",
            "macro_f1",
            "balanced_accuracy",
        ]
    ].dropna()

    if df.empty:
        print(
            "WARNING: Registry has no rows with accuracy, macro_f1, "
            "and balanced_accuracy. Skipping registry comparison."
        )
        return None

    df = df.drop_duplicates(
        subset=["experiment_id"],
        keep="last",
    )

    df = df.set_index("experiment_id")

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / "model_performance_comparison.png"

    fig, ax = plt.subplots(figsize=(12, 6))

    df.plot(
        kind="bar",
        ax=ax,
    )

    ax.set_ylabel("Score")
    ax.set_ylim(0.85, 1.0)
    ax.set_title("Model performance comparison")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(title="Metric")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def generate_run_figures(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> dict[str, Path | None]:
    """Generate all available figures for a single run."""

    outputs: dict[str, Path | None] = {
        "loss_curve": save_loss_curve(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
        "macro_f1_curve": save_macro_f1_curve(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
        "confusion_matrix": save_confusion_matrix(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
            normalize=None,
        ),
        "normalized_confusion_matrix": save_confusion_matrix(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
            normalize="true",
        ),
        "classwise_report": save_classwise_report(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
    }

    return outputs


def print_generated_outputs(
    outputs: dict[str, Path | None],
) -> None:
    """Print generated artifact paths."""

    print("\nGenerated files:")

    for output_name, output_path in outputs.items():
        if output_path is not None:
            print(f"  {output_name}: {output_path}")


def save_version_model_comparison(
    registry_path: str | Path,
    version: str,
    output_dir: str | Path,
    metrics: list[str] | None = None,
    min_y: float | None = None,
    max_y: float = 1.0,
) -> Path | None:
    """Save a trimmed-axis comparison chart for all models of one version."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        print(f"WARNING: Registry file not found: {registry_path}")
        return None

    registry = pd.read_csv(registry_path)

    if metrics is None:
        metrics = [
            "accuracy",
            "macro_f1",
            "weighted_f1",
            "balanced_accuracy",
        ]

    required_columns = {
        "experiment_id",
        "version",
        *metrics,
    }

    missing = required_columns - set(registry.columns)

    if missing:
        print(
            f"WARNING: registry.csv is missing required columns: {sorted(missing)}"
        )
        return None

    version_df = registry[
        registry["version"].astype(str).str.lower() == version.lower()
    ]

    if version_df.empty:
        print(f"WARNING: No experiments found for version: {version}")
        return None

    version_df = version_df.drop_duplicates(
        subset=["experiment_id"],
        keep="last",
    )

    plot_df = version_df[
        ["experiment_id", *metrics]
    ].dropna(subset=metrics)

    if plot_df.empty:
        print(f"WARNING: No valid metric rows found for version: {version}")
        return None

    plot_df = plot_df.set_index("experiment_id")

    metric_values = plot_df[metrics].to_numpy().ravel()
    observed_min = float(metric_values.min())

    if min_y is None:
        min_y = max(0.0, observed_min - 0.01)

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{version.lower()}_model_comparison.png"

    fig, ax = plt.subplots(figsize=(14, 7))

    plot_df[metrics].plot(
        kind="bar",
        ax=ax,
    )

    ax.set_xlabel("Experiment")
    ax.set_ylabel("Score")
    ax.set_ylim(min_y, max_y)
    ax.set_title(f"Trimmed model comparison for {version.upper()}")
    ax.tick_params(axis="x", rotation=90)
    ax.legend(title="Metric")

    ax.axhline(
        y=plot_df["accuracy"].max(),
        linestyle="--",
        linewidth=1,
        alpha=0.5,
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TerraSight report figures for a single run."
    )

    parser.add_argument(
        "--run-dir",
        help="Path to one experiment run directory.",
    )

    parser.add_argument(
        "--name",
        default=None,
        help="Optional output name prefix. If omitted, run folder name is used.",
    )

    parser.add_argument(
        "--registry",
        default="experiments/registry.csv",
        help="Optional path to experiment registry CSV.",
    )

    parser.add_argument(
        "--output-dir",
        default="reports/figures",
        help="Directory where figures and classwise reports are saved.",
    )

    parser.add_argument(
        "--version",
        default=None,
        help="Version to compare (v1, v2, v3, v4, v5).",
    )

    args = parser.parse_args()
    print(args)
    if args.output_dir is not None:
        output_dir = ensure_output_dir(args.output_dir)
    else:
        output_dir = "reports/figures"

    if args.version is not None:
        save_version_model_comparison(
            registry_path=args.registry,
            version=args.version,
            output_dir=output_dir,
        )
    if args.run_dir is not None:
        run_dir = Path(args.run_dir)

        if not run_dir.exists():
            raise FileNotFoundError(f"Run directory not found: {run_dir}")

        experiment_name = args.name or run_dir.name

        outputs = generate_run_figures(
            run_dir=run_dir,
            output_dir=output_dir,
            name=experiment_name,
        )

        registry_plot = save_registry_comparison(
            registry_path=args.registry,
            output_dir=output_dir,
        )

        if registry_plot is not None:
            outputs["registry_comparison"] = registry_plot

        print("\nReport-figure generation complete.")
        print(f"Run directory: {run_dir}")
        print(f"Output directory: {output_dir}")

        print_generated_outputs(outputs)


if __name__ == "__main__":
    main()