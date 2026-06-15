from __future__ import annotations

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import argparse
import json
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from terrasight.data.dataset import EuroSATMSDataset
from terrasight.data.preprocessing import normalize_multispectral_tensor
from terrasight.evaluation.metrics import compute_classification_metrics
from terrasight.models.multispectral_model import build_multispectral_model
from terrasight.training.losses import build_loss
from terrasight.training.optimizer_factory import build_optimizer
from terrasight.training.scheduler_factory import build_scheduler
from terrasight.utils.config import load_config
from terrasight.utils.run_setup import setup_run


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict[str, Any]:
    model.eval()

    total_loss = 0.0
    y_true: list[int] = []
    y_pred: list[int] = []

    for images, labels, _metadata in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        logits = model(images)
        loss = criterion(logits, labels)
        predictions = torch.argmax(logits, dim=1)

        total_loss += loss.item() * images.size(0)
        y_true.extend(labels.cpu().tolist())
        y_pred.extend(predictions.cpu().tolist())

    metrics = compute_classification_metrics(y_true, y_pred)
    metrics["loss"] = total_loss / len(dataloader.dataset)
    metrics["y_true"] = y_true
    metrics["y_pred"] = y_pred
    return metrics


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    model.train()

    total_loss = 0.0

    for images, labels, _metadata in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad(set_to_none=True)

        logits = model(images)
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)

    return total_loss / len(dataloader.dataset)


def validate_multispectral_config(config: dict[str, Any]) -> None:
    if config["data"]["input_type"] != "multispectral":
        raise ValueError("Expected data.input_type='multispectral'.")

    bands = config["data"].get("bands")

    if bands is None:
        expected_channels = 13
    else:
        expected_channels = len(bands)

    actual_channels = int(config["model"]["input_channels"])

    if actual_channels != expected_channels:
        raise ValueError(
            f"Expected model.input_channels={expected_channels}, "
            f"but got model.input_channels={actual_channels}. "
            "model.input_channels must match the number of selected data.bands."
        )


def train_multispectral_from_config(config_path: str | Path) -> Path:
    config = load_config(config_path)
    validate_multispectral_config(config)

    run_dir = setup_run(config_path)

    train_csv = Path(config["data"]["split_dir"]) / "train.csv"
    test_csv = Path(config["data"]["split_dir"]) / "test.csv"
    ms_root = Path(config["data"]["data_root"])

    selected_bands = config["data"].get("bands")
    source_bands = config["data"].get("source_bands")

    train_dataset = EuroSATMSDataset(
        split_csv=train_csv,
        multispectral_root=ms_root,
        transform=normalize_multispectral_tensor,
        source_bands=source_bands,
        selected_bands=selected_bands,
    )

    test_dataset = EuroSATMSDataset(
        split_csv=test_csv,
        multispectral_root=ms_root,
        transform=normalize_multispectral_tensor,
        source_bands=source_bands,
        selected_bands=selected_bands,
    )

    batch_size = int(config["training"]["batch_size"])

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
    )

    model = build_multispectral_model(
        model_name=config["model"]["name"],
        input_channels=int(config["model"]["input_channels"]),
        num_classes=int(config["model"]["num_classes"]),
        pretrained=bool(config["model"].get("pretrained", False)),
    )

    device = get_device()
    model = model.to(device)

    criterion = build_loss("cross_entropy")

    optimizer = build_optimizer(
        model=model,
        name=config["training"]["optimizer"],
        learning_rate=float(config["training"]["learning_rate"]),
        weight_decay=float(config["training"].get("weight_decay", 0.0)),
    )

    scheduler = build_scheduler(
        optimizer=optimizer,
        name=config["training"].get("scheduler"),
        epochs=int(config["training"]["epochs"]),
    )

    epochs = int(config["training"]["epochs"])

    early_cfg = config["training"].get("early_stopping", {})
    early_enabled = bool(early_cfg.get("enabled", False))
    monitor = early_cfg.get("monitor", "macro_f1")
    patience = int(early_cfg.get("patience", 7))
    min_delta = float(early_cfg.get("min_delta", 0.0))

    if monitor not in {
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
        "macro_precision",
        "macro_recall",
    }:
        raise ValueError(
            f"Unsupported early-stopping monitor: {monitor}. "
            "Use one of: accuracy, macro_f1, weighted_f1, "
            "balanced_accuracy, macro_precision, macro_recall."
        )

    best_score = -float("inf")
    best_macro_f1 = -1.0
    best_metrics: dict[str, Any] = {}
    history: list[dict[str, Any]] = []
    epochs_without_improvement = 0

    for epoch in range(1, epochs + 1):
        train_loss = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
        )

        metrics = evaluate_model(
            model=model,
            dataloader=test_loader,
            criterion=criterion,
            device=device,
        )

        metrics["epoch"] = epoch
        metrics["train_loss"] = train_loss
        history.append(metrics)

        print(
            f"Epoch {epoch}/{epochs} , "
            f"train_loss={train_loss:.4f} , "
            f"val_loss={metrics['loss']:.4f} , "
            f"accuracy={metrics['accuracy']:.4f} , "
            f"macro_f1={metrics['macro_f1']:.4f}"
        )

        if scheduler is not None:
            if scheduler.__class__.__name__ == "ReduceLROnPlateau":
                scheduler.step(metrics["loss"])
            else:
                scheduler.step()

        current_score = float(metrics[monitor])

        if current_score > best_score + min_delta:
            best_score = current_score
            best_macro_f1 = float(metrics["macro_f1"])
            best_metrics = metrics
            epochs_without_improvement = 0

            torch.save(
                model.state_dict(),
                run_dir / "best_model.pt",
            )

            print(f"New best {monitor}: {current_score:.4f}")

        else:
            epochs_without_improvement += 1

            print(
                f"No improvement in {monitor} "
                f"for {epochs_without_improvement}/{patience} epochs."
            )

        if early_enabled and epochs_without_improvement >= patience:
            print(
                f"\nEarly stopping triggered at epoch {epoch}. "
                f"No improvement in {monitor} for {patience} consecutive epochs."
            )
            break

    with (run_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(best_metrics, file, indent=2)

    with (run_dir / "history.json").open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)

    from terrasight.experiments.experiment_tracker import register_experiment

    register_experiment(
        config=config,
        metrics_file=run_dir / "metrics.json",
        run_dir=run_dir,
    )

    print("Multispectral training complete")
    print(f"Best macro-F1: {best_macro_f1:.4f}")
    print(f"Run directory: {run_dir}")

    from terrasight.experiments.experiment_tracker import register_experiment

    register_experiment(
        config=config,
        metrics_file=run_dir / "metrics.json",
        run_dir=run_dir,
    )

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TerraSight multispectral pipeline.")
    parser.add_argument(
        "--config",
        default="configs/v1_multispectral.yaml",
        help="Path to multispectral config file.",
    )

    args = parser.parse_args()

    train_multispectral_from_config(args.config)


if __name__ == "__main__":
    main()