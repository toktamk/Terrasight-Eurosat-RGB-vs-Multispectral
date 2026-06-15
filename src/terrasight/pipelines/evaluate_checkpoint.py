from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from terrasight.data.dataset import EuroSATMSDataset
from terrasight.data.preprocessing import normalize_multispectral_tensor
from terrasight.evaluation.metrics import compute_classification_metrics
from terrasight.models.multispectral_model import build_multispectral_model
from terrasight.training.losses import build_loss
from terrasight.utils.config import load_config


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict:
    model.eval()

    total_loss = 0.0
    y_true = []
    y_pred = []

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

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    config_path = run_dir / "config.yaml"
    checkpoint_path = run_dir / "best_model.pt"

    config = load_config(config_path)

    selected_bands = config["data"].get("bands")
    source_bands = config["data"].get("source_bands")

    test_csv = Path(config["data"]["split_dir"]) / "test.csv"
    ms_root = Path(config["data"]["data_root"])

    test_dataset = EuroSATMSDataset(
        split_csv=test_csv,
        multispectral_root=ms_root,
        transform=normalize_multispectral_tensor,
        source_bands=source_bands,
        selected_bands=selected_bands,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=int(config["training"]["batch_size"]),
        shuffle=False,
        num_workers=0,
    )

    model = build_multispectral_model(
        model_name=config["model"]["name"],
        input_channels=int(config["model"]["input_channels"]),
        num_classes=int(config["model"]["num_classes"]),
        pretrained=False,
    )

    device = get_device()
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model = model.to(device)

    criterion = build_loss("cross_entropy")

    metrics = evaluate_model(
        model=model,
        dataloader=test_loader,
        criterion=criterion,
        device=device,
    )

    output_path = run_dir / "checkpoint_metrics.json"
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print(json.dumps(metrics, indent=2))
    print(f"Saved metrics to: {output_path}")


if __name__ == "__main__":
    main()