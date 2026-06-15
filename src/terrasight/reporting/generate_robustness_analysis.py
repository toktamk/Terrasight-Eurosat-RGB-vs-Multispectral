from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score
from torch.utils.data import DataLoader

from terrasight.data.band_registry import EUROSAT_CLASSES
from terrasight.reliability.robustness import add_gaussian_noise, apply_brightness_shift, dropout_bands
from terrasight.reporting.generate_prediction_probabilities import (
    build_dataset,
    build_model,
    find_checkpoint,
    load_checkpoint,
    project_root,
)
from terrasight.utils.config import load_config


@torch.no_grad()
def evaluate(model, dataloader, device, perturbation: str, band_index: int | None = None) -> dict:
    model.eval()
    y_true, y_pred = [], []

    for images, labels, _metadata in dataloader:
        images = images.to(device)

        if perturbation == "gaussian_noise":
            images = add_gaussian_noise(images, std=0.05)
        elif perturbation == "brightness_plus":
            images = apply_brightness_shift(images, shift=0.10)
        elif perturbation == "brightness_minus":
            images = apply_brightness_shift(images, shift=-0.10)
        elif perturbation == "band_dropout":
            if band_index is None:
                raise ValueError("band_index required for band_dropout")
            images = dropout_bands(images, [band_index])
        elif perturbation == "clean":
            pass
        else:
            raise ValueError(perturbation)

        logits = model(images)
        preds = torch.argmax(logits, dim=1).cpu().tolist()

        y_true.extend(labels.tolist())
        y_pred.extend(preds)

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


def process_run(run_dir: Path, output_dir: Path) -> None:
    root = project_root()
    config_path = run_dir / "config.yaml"
    checkpoint_path = find_checkpoint(run_dir)

    if not config_path.exists() or checkpoint_path is None:
        return

    config = load_config(config_path)
    experiment_id = config["experiment"]["id"]

    dataset = build_dataset(config, root)
    dataloader = DataLoader(dataset, batch_size=int(config["training"]["batch_size"]), shuffle=False, num_workers=0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model(config)
    model = load_checkpoint(model, checkpoint_path, device).to(device)

    clean = evaluate(model, dataloader, device, "clean")
    rows = []

    for perturbation in ["gaussian_noise", "brightness_plus", "brightness_minus"]:
        result = evaluate(model, dataloader, device, perturbation)
        rows.append(
            {
                "experiment_id": experiment_id,
                "perturbation": perturbation,
                "band": "",
                "accuracy": result["accuracy"],
                "macro_f1": result["macro_f1"],
                "accuracy_drop": clean["accuracy"] - result["accuracy"],
                "macro_f1_drop": clean["macro_f1"] - result["macro_f1"],
            }
        )

    bands = config["data"].get("bands", [])
    for i, band in enumerate(bands):
        result = evaluate(model, dataloader, device, "band_dropout", band_index=i)
        rows.append(
            {
                "experiment_id": experiment_id,
                "perturbation": "band_dropout",
                "band": band,
                "accuracy": result["accuracy"],
                "macro_f1": result["macro_f1"],
                "accuracy_drop": clean["accuracy"] - result["accuracy"],
                "macro_f1_drop": clean["macro_f1"] - result["macro_f1"],
            }
        )

    output_path = output_dir / f"{experiment_id}_robustness.csv"
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output-dir", default="reports/tables/robustness")
    args = parser.parse_args()

    root = project_root()
    output_dir = root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    process_run(root / args.run_dir, output_dir)


if __name__ == "__main__":
    main()