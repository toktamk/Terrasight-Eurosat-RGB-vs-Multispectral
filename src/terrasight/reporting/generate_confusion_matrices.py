from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import matplotlib.pyplot as plt
import pandas as pd
import torch
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from torch.utils.data import DataLoader

from terrasight.data.band_registry import EUROSAT_CLASSES
from terrasight.data.dataset import EuroSATMSDataset, EuroSATRGBDataset
from terrasight.data.preprocessing import get_rgb_transform, normalize_multispectral_tensor
from terrasight.models.multispectral_model import build_multispectral_model
from terrasight.models.rgb_model import build_rgb_model
from terrasight.utils.config import load_config


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def find_checkpoint(run_dir: Path) -> Path | None:
    candidates = [
        run_dir / "best_model.pt",
        run_dir / "best_model.pth",
        run_dir / "checkpoint.pt",
        run_dir / "checkpoint.pth",
        run_dir / "model.pt",
        run_dir / "model.pth",
    ]

    for path in candidates:
        if path.exists():
            return path

    all_candidates = sorted(list(run_dir.glob("*.pt")) + list(run_dir.glob("*.pth")))
    return all_candidates[0] if all_candidates else None


def fix_relative_paths_in_dataset(dataset: Any, project_root: Path) -> Any:
    if not hasattr(dataset, "samples"):
        return dataset

    samples = dataset.samples.copy()

    path_column = None
    for candidate in ["path", "image_path", "filepath", "file_path"]:
        if candidate in samples.columns:
            path_column = candidate
            break

    if path_column is None:
        return dataset

    def resolve_path(value: str) -> str:
        p = Path(str(value))
        if p.is_absolute():
            return str(p.resolve())
        return str((project_root / p).resolve())

    samples[path_column] = samples[path_column].apply(resolve_path)
    dataset.samples = samples
    return dataset


def build_dataset(config: dict, project_root: Path):
    split_dir = project_root / config["data"]["split_dir"]
    test_csv = split_dir / "test.csv"

    if not test_csv.exists():
        raise FileNotFoundError(f"Test split not found: {test_csv}")

    input_type = config["data"]["input_type"]

    if input_type == "rgb":
        dataset = EuroSATRGBDataset(
            split_csv=test_csv,
            transform=get_rgb_transform(train=False),
        )
        return fix_relative_paths_in_dataset(dataset, project_root)

    data_root = project_root / config["data"]["data_root"]

    dataset = EuroSATMSDataset(
        split_csv=test_csv,
        multispectral_root=data_root,
        transform=normalize_multispectral_tensor,
        source_bands=config["data"].get("source_bands"),
        selected_bands=config["data"].get("bands"),
    )

    return fix_relative_paths_in_dataset(dataset, project_root)


def build_model(config: dict):
    input_type = config["data"]["input_type"]

    if input_type == "rgb":
        return build_rgb_model(
            model_name=config["model"]["name"],
            num_classes=int(config["model"]["num_classes"]),
            pretrained=False,
        )

    return build_multispectral_model(
        model_name=config["model"]["name"],
        input_channels=int(config["model"]["input_channels"]),
        num_classes=int(config["model"]["num_classes"]),
        pretrained=False,
    )


def load_checkpoint_into_model(model: torch.nn.Module, checkpoint_path: Path, device: torch.device) -> torch.nn.Module:
    checkpoint = torch.load(checkpoint_path, map_location=device)

    if isinstance(checkpoint, dict):
        if "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
        elif "state_dict" in checkpoint:
            state_dict = checkpoint["state_dict"]
        elif "model" in checkpoint:
            state_dict = checkpoint["model"]
        else:
            state_dict = checkpoint
    else:
        state_dict = checkpoint

    cleaned_state_dict = {}
    for key, value in state_dict.items():
        new_key = key.replace("module.", "")
        cleaned_state_dict[new_key] = value

    model.load_state_dict(cleaned_state_dict)
    return model


def extract_metadata_value(metadata: Any, key: str, batch_size: int) -> list[str]:
    if isinstance(metadata, dict) and key in metadata:
        value = metadata[key]
        if isinstance(value, list):
            return [str(v) for v in value]
        if isinstance(value, tuple):
            return [str(v) for v in value]
        return [str(value)] * batch_size

    return [""] * batch_size


@torch.no_grad()
def predict(model: torch.nn.Module, dataloader: DataLoader, device: torch.device):
    model.eval()

    y_true: list[int] = []
    y_pred: list[int] = []
    paths: list[str] = []
    class_names: list[str] = []

    for batch in dataloader:
        if len(batch) == 3:
            images, labels, metadata = batch
        else:
            images, labels = batch
            metadata = {}

        images = images.to(device)
        labels = labels.cpu()

        logits = model(images)
        predictions = torch.argmax(logits, dim=1).cpu()

        batch_size = len(labels)

        y_true.extend(labels.tolist())
        y_pred.extend(predictions.tolist())
        paths.extend(extract_metadata_value(metadata, "path", batch_size))
        class_names.extend(extract_metadata_value(metadata, "class_name", batch_size))

    return y_true, y_pred, paths, class_names


def save_outputs(
    run_dir: Path,
    experiment_id: str,
    y_true: list[int],
    y_pred: list[int],
    paths: list[str],
    class_names: list[str],
    output_figures: Path,
    output_tables: Path,
) -> None:
    safe_name = experiment_id.replace("/", "_").replace("\\", "_")

    prediction_df = pd.DataFrame(
        {
            "path": paths,
            "true_label": y_true,
            "predicted_label": y_pred,
            "true_class": [EUROSAT_CLASSES[i] for i in y_true],
            "predicted_class": [EUROSAT_CLASSES[i] for i in y_pred],
            "source_class_name": class_names,
        }
    )

    prediction_csv = output_tables / f"{safe_name}_predictions.csv"
    prediction_df.to_csv(prediction_csv, index=False)

    prediction_json = run_dir / "predictions.json"
    with prediction_json.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "experiment_id": experiment_id,
                "y_true": y_true,
                "y_pred": y_pred,
            },
            file,
            indent=2,
        )

    report = classification_report(
        y_true,
        y_pred,
        labels=list(range(len(EUROSAT_CLASSES))),
        target_names=EUROSAT_CLASSES,
        output_dict=True,
        zero_division=0,
    )

    report_csv = output_tables / f"{safe_name}_classwise_report.csv"
    pd.DataFrame(report).T.to_csv(report_csv)

    for normalize, suffix, value_format in [
        (None, "confusion_matrix", "d"),
        ("true", "normalized_confusion_matrix", ".2f"),
    ]:
        cm = confusion_matrix(
            y_true,
            y_pred,
            labels=list(range(len(EUROSAT_CLASSES))),
            normalize=normalize,
        )

        fig, ax = plt.subplots(figsize=(11, 11))
        display = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=EUROSAT_CLASSES,
        )

        display.plot(
            ax=ax,
            xticks_rotation=45,
            colorbar=True,
            values_format=value_format,
        )

        ax.set_title(f"{experiment_id}\n{suffix}")
        fig.tight_layout()

        output_path = output_figures / f"{safe_name}_{suffix}.png"
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    print(f"Saved predictions and confusion matrices for: {experiment_id}")


def process_run(
    run_dir: Path,
    project_root: Path,
    output_figures: Path,
    output_tables: Path,
) -> None:
    config_path = run_dir / "config.yaml"

    if not config_path.exists():
        return

    checkpoint_path = find_checkpoint(run_dir)

    if checkpoint_path is None:
        print(f"Skipping {run_dir}: no checkpoint found")
        return

    print(f"Processing: {run_dir.name}")
    print(f"Checkpoint: {checkpoint_path.name}")

    config = load_config(config_path)
    experiment_id = config["experiment"]["id"]

    dataset = build_dataset(config, project_root)

    dataloader = DataLoader(
        dataset,
        batch_size=int(config["training"]["batch_size"]),
        shuffle=False,
        num_workers=0,
    )

    device = get_device()

    model = build_model(config)
    model = load_checkpoint_into_model(model, checkpoint_path, device)
    model = model.to(device)

    y_true, y_pred, paths, class_names = predict(
        model=model,
        dataloader=dataloader,
        device=device,
    )

    save_outputs(
        run_dir=run_dir,
        experiment_id=experiment_id,
        y_true=y_true,
        y_pred=y_pred,
        paths=paths,
        class_names=class_names,
        output_figures=output_figures,
        output_tables=output_tables,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate predictions and confusion matrices for saved TerraSight runs."
    )

    parser.add_argument(
        "--results-root",
        default="results",
        help="Root results directory containing version folders such as v1 and v4.",
    )

    parser.add_argument(
        "--versions",
        nargs="+",
        default=["v1", "v4"],
        help="Version folders to scan, for example: v1 v4.",
    )

    parser.add_argument(
        "--output-figures",
        default="reports/figures/confusion_matrices",
        help="Output directory for confusion matrix figures.",
    )

    parser.add_argument(
        "--output-tables",
        default="reports/tables/predictions",
        help="Output directory for prediction CSVs and classwise reports.",
    )

    args = parser.parse_args()

    project_root = get_project_root()

    results_root = project_root / args.results_root
    output_figures = project_root / args.output_figures
    output_tables = project_root / args.output_tables

    output_figures.mkdir(parents=True, exist_ok=True)
    output_tables.mkdir(parents=True, exist_ok=True)

    if not results_root.exists():
        raise FileNotFoundError(f"Results root not found: {results_root}")

    run_dirs: list[Path] = []

    for version in args.versions:
        version_dir = results_root / version

        if not version_dir.exists():
            print(f"Skipping missing version directory: {version_dir}")
            continue

        version_runs = sorted(
            p for p in version_dir.iterdir()
            if p.is_dir() and (p / "config.yaml").exists()
        )

        run_dirs.extend(version_runs)

    if not run_dirs:
        raise FileNotFoundError("No run directories with config.yaml were found.")

    for run_dir in run_dirs:
        process_run(
            run_dir=run_dir,
            project_root=project_root,
            output_figures=output_figures,
            output_tables=output_tables,
        )

    print("Done.")


if __name__ == "__main__":
    main()