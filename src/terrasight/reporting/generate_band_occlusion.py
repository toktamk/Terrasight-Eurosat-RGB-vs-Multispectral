from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import DataLoader

from terrasight.data.band_registry import SENTINEL2_BANDS
from terrasight.explainability.band_occlusion import (
    run_band_occlusion,
    summarize_band_occlusion,
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Sentinel-2 band-occlusion analysis for a trained TerraSight run."
    )

    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output-dir", default="reports/tables/band_occlusion")
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--strategy", default="zero", choices=["zero"])
    parser.add_argument("--target-mode", default="predicted", choices=["predicted", "true"])

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

    batch_size = args.batch_size
    if batch_size is None:
        batch_size = int(config.get("training", {}).get("batch_size", 32))

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
    )

    device = get_device()

    model = build_model(config)
    model = load_checkpoint_into_model(model, checkpoint_path, device)
    model = model.to(device)
    model.eval()

    band_names = get_band_names(config)

    details_path = output_dir / f"{experiment_id}_band_occlusion_details.csv"
    summary_path = output_dir / f"{experiment_id}_band_occlusion_summary.csv"

    details = run_band_occlusion(
        model=model,
        dataloader=dataloader,
        band_names=band_names,
        occlusion_strategy=args.strategy,
        target_mode=args.target_mode,
        device=device,
        max_batches=args.max_batches,
        output_csv=details_path,
    )

    summary = summarize_band_occlusion(
        occlusion_df=details,
        output_csv=summary_path,
    )

    print(f"Saved details: {details_path}")
    print(f"Saved summary: {summary_path}")
    print(summary.head(10).to_string(index=False))


if __name__ == "__main__":
    main()