from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from terrasight.data.band_registry import EUROSAT_CLASSES
from terrasight.reporting.generate_confusion_matrices import (
    build_dataset,
    build_model,
    find_checkpoint,
    get_device,
    get_project_root,
    load_checkpoint_into_model,
)
from terrasight.utils.config import load_config


@torch.no_grad()
def predict_probabilities(model, dataloader, device):
    model.eval()

    rows = []

    for batch in dataloader:
        if len(batch) == 3:
            images, labels, metadata = batch
        else:
            images, labels = batch
            metadata = {}

        images = images.to(device)
        logits = model(images)
        probabilities = F.softmax(logits, dim=1).cpu()
        predictions = torch.argmax(probabilities, dim=1)

        batch_size = len(labels)

        paths = metadata.get("path", [""] * batch_size) if isinstance(metadata, dict) else [""] * batch_size

        for i in range(batch_size):
            true_label = int(labels[i])
            pred_label = int(predictions[i])
            probs = probabilities[i].tolist()

            row = {
                "path": str(paths[i]) if i < len(paths) else "",
                "true_label": true_label,
                "predicted_label": pred_label,
                "true_class": EUROSAT_CLASSES[true_label],
                "predicted_class": EUROSAT_CLASSES[pred_label],
                "confidence": max(probs),
                "correct": int(true_label == pred_label),
            }

            for class_index, class_name in enumerate(EUROSAT_CLASSES):
                row[f"prob_{class_name}"] = probs[class_index]

            rows.append(row)

    return pd.DataFrame(rows)


def process_run(run_dir: Path, project_root: Path, output_dir: Path) -> None:
    config_path = run_dir / "config.yaml"
    checkpoint_path = find_checkpoint(run_dir)

    if not config_path.exists() or checkpoint_path is None:
        print(f"Skipping {run_dir}")
        return

    config = load_config(config_path)
    experiment_id = config["experiment"]["id"]

    print(f"Processing: {experiment_id}")

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

    df = predict_probabilities(model, dataloader, device)

    output_path = output_dir / f"{experiment_id}_probabilities.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--versions", nargs="+", default=["v1", "v4"])
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--output-dir", default="reports/tables/probabilities")
    args = parser.parse_args()

    project_root = get_project_root()
    results_root = project_root / args.results_root
    output_dir = project_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    for version in args.versions:
        version_dir = results_root / version

        if not version_dir.exists():
            continue

        for run_dir in sorted(version_dir.iterdir()):
            if run_dir.is_dir():
                process_run(run_dir, project_root, output_dir)


if __name__ == "__main__":
    main()