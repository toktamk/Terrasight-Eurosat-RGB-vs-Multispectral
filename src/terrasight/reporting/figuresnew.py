from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix

from terrasight.data.band_registry import EUROSAT_CLASSES


def load_json(path: str | Path) -> Any:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def ensure_output_dir(output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def safe_label(label: str) -> str:
    return (
        label.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )


def load_history(run_dir: str | Path) -> pd.DataFrame | None:
    history_path = Path(run_dir) / "history.json"

    if not history_path.exists():
        print(f"WARNING: history.json not found in {run_dir}.")
        return None

    history = pd.DataFrame(load_json(history_path))
    required = {"epoch", "train_loss", "loss", "macro_f1"}
    missing = required - set(history.columns)

    if missing:
        print(f"WARNING: history.json in {run_dir} missing {sorted(missing)}.")
        return None

    return history


def load_predictions(run_dir: str | Path) -> tuple[list[int], list[int]] | None:
    predictions_path = Path(run_dir) / "predictions.json"

    if not predictions_path.exists():
        print(f"WARNING: predictions.json not found in {run_dir}.")
        return None

    predictions = load_json(predictions_path)

    if "y_true" not in predictions or "y_pred" not in predictions:
        print(f"WARNING: Invalid predictions.json in {run_dir}.")
        return None

    return predictions["y_true"], predictions["y_pred"]


def save_combined_loss_curve(
    runs: list[tuple[Path, str]],
    output_dir: Path,
) -> Path | None:
    output_path = output_dir / "combined_loss_curves.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    plotted = False

    for run_dir, label in runs:
        history = load_history(run_dir)
        if history is None:
            continue

        ax.plot(
            history["epoch"],
            history["train_loss"],
            linestyle="-",
            marker="o",
            label=f"{label} train",
        )
        ax.plot(
            history["epoch"],
            history["loss"],
            linestyle="--",
            marker="o",
            label=f"{label} validation",
        )
        plotted = True

    if not plotted:
        plt.close(fig)
        return None

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_title("Training and validation loss comparison")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_combined_macro_f1_curve(
    runs: list[tuple[Path, str]],
    output_dir: Path,
) -> Path | None:
    output_path = output_dir / "combined_macro_f1_curves.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    plotted = False

    for run_dir, label in runs:
        history = load_history(run_dir)
        if history is None:
            continue

        ax.plot(
            history["epoch"],
            history["macro_f1"],
            marker="o",
            label=label,
        )
        plotted = True

    if not plotted:
        plt.close(fig)
        return None

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Macro-F1")
    ax.set_title("Validation macro-F1 comparison")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_combined_confusion_matrices(
    runs: list[tuple[Path, str]],
    output_dir: Path,
    normalize: str | None = None,
) -> Path | None:
    valid_runs: list[tuple[list[int], list[int], str]] = []

    for run_dir, label in runs:
        predictions = load_predictions(run_dir)
        if predictions is None:
            continue
        y_true, y_pred = predictions
        valid_runs.append((y_true, y_pred, label))

    if not valid_runs:
        return None

    suffix = "normalized_confusion_matrices" if normalize else "confusion_matrices"
    output_path = output_dir / f"combined_{suffix}.png"

    n = len(valid_runs)
    fig, axes = plt.subplots(
        1,
        n,
        figsize=(8 * n, 7),
        squeeze=False,
    )

    for ax, (y_true, y_pred, label) in zip(axes[0], valid_runs):
        cm = confusion_matrix(
            y_true,
            y_pred,
            labels=list(range(len(EUROSAT_CLASSES))),
            normalize=normalize,
        )

        display = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=EUROSAT_CLASSES,
        )

        display.plot(
            ax=ax,
            xticks_rotation=45,
            colorbar=False,
            values_format=".2f" if normalize else "d",
        )

        ax.set_title(label)

    fig.suptitle(
        "Normalized confusion matrices" if normalize else "Confusion matrices",
        fontsize=14,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_classwise_reports(
    runs: list[tuple[Path, str]],
    output_dir: Path,
) -> dict[str, Path]:
    reports: dict[str, Path] = {}

    for run_dir, label in runs:
        predictions = load_predictions(run_dir)
        if predictions is None:
            continue

        y_true, y_pred = predictions
        safe = safe_label(label)
        output_path = output_dir / f"{safe}_classwise_report.csv"

        report = classification_report(
            y_true,
            y_pred,
            labels=list(range(len(EUROSAT_CLASSES))),
            target_names=EUROSAT_CLASSES,
            output_dict=True,
            zero_division=0,
        )

        pd.DataFrame(report).T.to_csv(output_path)
        reports[label] = output_path

    return reports


def save_combined_per_class_f1(
    reports: dict[str, Path],
    output_dir: Path,
) -> Path | None:
    if not reports:
        return None

    data: dict[str, list[float]] = {}

    for label, report_path in reports.items():
        df = pd.read_csv(report_path, index_col=0)

        if "f1-score" not in df.columns:
            continue

        data[label] = [
            float(df.loc[class_name, "f1-score"])
            for class_name in EUROSAT_CLASSES
            if class_name in df.index
        ]

    if not data:
        return None

    comparison = pd.DataFrame(data, index=EUROSAT_CLASSES)
    output_path = output_dir / "combined_per_class_f1.png"

    fig, ax = plt.subplots(figsize=(14, 7))
    comparison.plot(kind="bar", ax=ax)

    ax.set_xlabel("Class")
    ax.set_ylabel("F1-score")
    ax.set_ylim(0.75, 1.0)
    ax.set_title("Per-class F1 comparison")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Experiment", fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_registry_comparison(
    registry_path: str | Path,
    output_dir: Path,
) -> Path | None:
    registry_path = Path(registry_path)

    if not registry_path.exists():
        print(f"WARNING: Registry file not found: {registry_path}.")
        return None

    registry = pd.read_csv(registry_path)

    required = {
        "experiment_id",
        "accuracy",
        "macro_f1",
        "balanced_accuracy",
    }

    missing = required - set(registry.columns)
    if missing:
        print(f"WARNING: Registry missing columns {sorted(missing)}.")
        return None

    df = registry[
        ["experiment_id", "accuracy", "macro_f1", "balanced_accuracy"]
    ].dropna()

    if df.empty:
        return None

    df = df.drop_duplicates(subset=["experiment_id"], keep="last")
    df = df.set_index("experiment_id")

    output_path = output_dir / "registry_model_performance_comparison.png"

    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(kind="bar", ax=ax)

    ax.set_ylabel("Score")
    ax.set_ylim(0.85, 1.0)
    ax.set_title("Model performance comparison from registry")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(title="Metric")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def print_outputs(outputs: dict[str, Path | None]) -> None:
    for name, path in outputs.items():
        if path is not None:
            print(f"Generated {name}: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TerraSight figures for one experiment run."
    )

    parser.add_argument(
        "--run-dir",
        required=True,
        help="Path to one experiment run directory.",
    )

    parser.add_argument(
        "--name",
        default=None,
        help="Optional figure prefix. If omitted, run folder name is used.",
    )

    parser.add_argument(
        "--registry",
        default="experiments/registry.csv",
        help="Path to experiment registry CSV.",
    )

    parser.add_argument(
        "--output-dir",
        default="reports/figures",
        help="Directory where figures are saved.",
    )

    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    output_dir = ensure_output_dir(args.output_dir)

    name = args.name or run_dir.name

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
        "registry_comparison": save_registry_comparison(
            registry_path=args.registry,
            output_dir=output_dir,
        ),
    }

    print("Report-figure generation complete.")
    print(f"Run directory: {run_dir}")
    print(f"Output directory: {output_dir}")
    print_generated_outputs(outputs)

if __name__ == "__main__":
    main()