from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
import torch

from terrasight.data.band_registry import EUROSAT_CLASSES, SENTINEL2_BANDS
from terrasight.explainability.spectral_attribution import (
    band_occlusion_scores,
    rank_band_importance,
)
from terrasight.reporting.generate_prediction_probabilities import (
    build_dataset,
    build_model,
    find_checkpoint,
)
from terrasight.reporting.generate_confusion_matrices import (
    get_device,
    get_project_root,
    load_checkpoint_into_model,
)
from terrasight.utils.config import load_config


def get_band_names(config: dict) -> list[str]:
    bands = config.get("data", {}).get("bands")
    if bands:
        return list(bands)

    input_channels = int(config.get("model", {}).get("in_channels", 13))

    if input_channels == 13:
        return list(SENTINEL2_BANDS)

    return [f"band_{i}" for i in range(input_channels)]


def get_sample_path(metadata: Any) -> str:
    if isinstance(metadata, dict):
        for key in ["path", "image_path", "filepath", "file_path"]:
            if key in metadata:
                return str(metadata[key])
    return ""


@torch.no_grad()
def predict_single(model: torch.nn.Module, image: torch.Tensor, device: torch.device) -> tuple[int, float]:
    model.eval()
    logits = model(image.unsqueeze(0).to(device))
    probs = torch.softmax(logits, dim=1)
    pred = int(torch.argmax(probs, dim=1).item())
    conf = float(probs[0, pred].item())
    return pred, conf


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate single-sample spectral attribution using band occlusion."
    )

    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output-dir", default="reports/tables/spectral_attribution")
    parser.add_argument("--num-examples", type=int, default=20)
    parser.add_argument(
        "--selection-mode",
        default="first",
        choices=["first", "correct", "incorrect"],
    )

    args = parser.parse_args()

    root = get_project_root()
    run_dir = root / args.run_dir
    output_dir = root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = run_dir / "config.yaml"
    checkpoint_path = find_checkpoint(run_dir)

    if not config_path.exists():
        raise FileNotFoundError(config_path)

    if checkpoint_path is None:
        raise FileNotFoundError(f"No checkpoint found in {run_dir}")

    config = load_config(config_path)
    experiment_id = config["experiment"]["id"]

    dataset = build_dataset(config, root)

    device = get_device()

    model = build_model(config)
    model = load_checkpoint_into_model(model, checkpoint_path, device)
    model = model.to(device)
    model.eval()

    band_names = get_band_names(config)

    long_rows: list[dict] = []
    top_rows: list[dict] = []

    saved = 0

    for idx in range(len(dataset)):
        image, label, metadata = dataset[idx]
        label = int(label)

        pred, confidence = predict_single(model, image, device)
        correct = pred == label

        if args.selection_mode == "correct" and not correct:
            continue

        if args.selection_mode == "incorrect" and correct:
            continue

        target_class = pred

        scores = band_occlusion_scores(
            model=model,
            image=image.unsqueeze(0).to(device),
            target_class=target_class,
            band_names=band_names,
        )

        ranked = rank_band_importance(scores)

        sample_path = get_sample_path(metadata)

        for rank, (band_name, score) in enumerate(ranked, start=1):
            long_rows.append(
                {
                    "experiment_id": experiment_id,
                    "sample_index": idx,
                    "path": sample_path,
                    "true_label": label,
                    "true_class": EUROSAT_CLASSES[label],
                    "predicted_label": pred,
                    "predicted_class": EUROSAT_CLASSES[pred],
                    "confidence": confidence,
                    "correct": correct,
                    "target_class": target_class,
                    "target_class_name": EUROSAT_CLASSES[target_class],
                    "band_rank": rank,
                    "band_name": band_name,
                    "attribution_score": score,
                }
            )

        top_band, top_score = ranked[0]

        top_rows.append(
            {
                "experiment_id": experiment_id,
                "sample_index": idx,
                "path": sample_path,
                "true_class": EUROSAT_CLASSES[label],
                "predicted_class": EUROSAT_CLASSES[pred],
                "confidence": confidence,
                "correct": correct,
                "top_band": top_band,
                "top_score": top_score,
            }
        )

        saved += 1

        if saved >= args.num_examples:
            break

    long_path = output_dir / f"{experiment_id}_spectral_attribution_long.csv"
    top_path = output_dir / f"{experiment_id}_spectral_attribution_top.csv"

    pd.DataFrame(long_rows).to_csv(long_path, index=False)
    pd.DataFrame(top_rows).to_csv(top_path, index=False)

    print(f"Saved attribution table: {long_path}")
    print(f"Saved top-band table: {top_path}")


if __name__ == "__main__":
    main()