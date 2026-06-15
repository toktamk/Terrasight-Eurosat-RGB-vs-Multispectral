from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.terrasight.data.preprocessing import get_rgb_transform
from src.terrasight.data.dataset import EuroSATRGBDataset
from src.terrasight.evaluation.metrics import compute_classification_metrics
from src.terrasight.models.rgb_model import build_rgb_model
from src.terrasight.training.losses import build_loss
from src.terrasight.training.optimizer_factory import build_optimizer
from src.terrasight.training.scheduler_factory import build_scheduler
from src.terrasight.utils.config import load_config
from src.terrasight.utils.run_setup import setup_run


def get_device() -> torch.device:
    """Return available compute device."""

    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    """Train model for one epoch."""

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


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict[str, Any]:
    """Evaluate model."""

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


def save_checkpoint(
    model: nn.Module,
    run_dir: Path,
    filename: str = "checkpoint.pt",
) -> None:
    """Save model checkpoint."""

    checkpoint_path = run_dir / filename
    torch.save(model.state_dict(), checkpoint_path)


from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_metrics(
    metrics: dict[str, Any],
    run_dir: Path,
) -> None:
    """
    Save evaluation metrics and predictions.

    Outputs:
        metrics.json
            Contains scalar metrics only.

        predictions.json
            Contains ground-truth and predicted labels
            for downstream analysis and visualisation.
    """

    run_dir.mkdir(parents=True, exist_ok=True)

    # Save only serializable scalar metrics
    metrics_for_json = {
        key: value
        for key, value in metrics.items()
        if key not in {"y_true", "y_pred"}
    }

    metrics_path = run_dir / "metrics.json"

    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump(metrics_for_json, file, indent=2)

    # Save predictions separately if available
    if "y_true" in metrics and "y_pred" in metrics:

        predictions = {
            "y_true": metrics["y_true"],
            "y_pred": metrics["y_pred"],
        }

        predictions_path = run_dir / "predictions.json"

        with predictions_path.open("w", encoding="utf-8") as file:
            json.dump(predictions, file, indent=2)


def train_from_config(config_path: str | Path) -> Path:
    """Train RGB baseline from config.

    This trainer currently supports RGB only.
    Multispectral training will be added in the next pipeline part.
    """

    config = load_config(config_path)
    run_dir = setup_run(config_path)

    if config["data"]["input_type"] != "rgb":
        raise ValueError(
            "Part 7 trainer currently supports RGB configs only. "
            "Multispectral support will be added in the multispectral pipeline."
        )

    train_csv = Path(config["data"]["split_dir"]) / "train.csv"
    test_csv = Path(config["data"]["split_dir"]) / "test.csv"

    train_dataset = EuroSATRGBDataset(
        split_csv=train_csv,
        transform=get_rgb_transform(train=True),
    )
    test_dataset = EuroSATRGBDataset(
        split_csv=test_csv,
        transform=get_rgb_transform(train=False),
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

    model = build_rgb_model(
        model_name=config["model"]["name"],
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
    best_macro_f1 = -1.0
    best_metrics: dict[str, Any] = {}

    history: list[dict[str, Any]] = []

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
            f"Epoch {epoch}/{epochs} | "
            f"train_loss={train_loss:.4f} | "
            f"val_loss={metrics['loss']:.4f} | "
            f"accuracy={metrics['accuracy']:.4f} | "
            f"macro_f1={metrics['macro_f1']:.4f}"
        )

        if scheduler is not None:
            if scheduler.__class__.__name__ == "ReduceLROnPlateau":
                scheduler.step(metrics["loss"])
            else:
                scheduler.step()

        if metrics["macro_f1"] > best_macro_f1:
            best_macro_f1 = metrics["macro_f1"]
            best_metrics = metrics
            save_checkpoint(model, run_dir, "best_model.pt")

    save_metrics(best_metrics, run_dir)
    from terrasight.experiments.experiment_tracker import register_experiment

    register_experiment(
        config=config,
        metrics_file=run_dir / "metrics.json",
        run_dir=run_dir,
    )
    history_path = run_dir / "history.json"
    with history_path.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)

    print("Training complete")
    print(f"Best macro-F1: {best_macro_f1:.4f}")
    print(f"Run directory: {run_dir}")

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Train TerraSight RGB baseline.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    train_from_config(args.config)


if __name__ == "__main__":
    main()