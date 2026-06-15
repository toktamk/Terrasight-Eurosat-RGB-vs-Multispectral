from __future__ import annotations

import argparse
from pathlib import Path

from src.terrasight.training.trainer import train_from_config
from src.terrasight.utils.config import load_config


EXPECTED_RGB_BANDS = ["B4", "B3", "B2"]


def validate_rgb_config(config_path: str | Path) -> None:
    """Validate that the config is suitable for RGB baseline training."""

    config = load_config(config_path)

    input_type = config["data"].get("input_type")
    if input_type != "rgb":
        raise ValueError(f"Expected data.input_type='rgb', got '{input_type}'.")

    input_channels = int(config["model"].get("input_channels"))
    if input_channels != 3:
        raise ValueError(f"Expected model.input_channels=3, got {input_channels}.")

    bands = config["data"].get("bands")
    if bands != EXPECTED_RGB_BANDS:
        raise ValueError(f"Expected RGB bands {EXPECTED_RGB_BANDS}, got {bands}.")


def run_rgb_pipeline(config_path: str | Path) -> Path:
    """Run the RGB baseline training pipeline."""

    validate_rgb_config(config_path)

    run_dir = train_from_config(config_path)

    print("RGB baseline pipeline complete")
    print(f"Outputs saved to: {run_dir}")

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TerraSight RGB baseline pipeline.")
    parser.add_argument(
        "--config",
        default="configs/v1_rgb_baseline.yaml",
        help="Path to RGB baseline config file.",
    )
    args = parser.parse_args()

    run_rgb_pipeline(args.config)


if __name__ == "__main__":
    main()