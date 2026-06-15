from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


REQUIRED_TOP_LEVEL_KEYS = ["experiment", "seed", "data", "model", "training", "evaluation"]


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(f"Config must be a YAML dictionary: {path}")

    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in config]

    if missing:
        raise ValueError(f"Missing required config keys: {missing}")

    if "id" not in config["experiment"]:
        raise ValueError("Missing experiment.id")

    if "dataset" not in config["data"]:
        raise ValueError("Missing data.dataset")

    if "bands" not in config["data"]:
        raise ValueError("Missing data.bands")

    if "name" not in config["model"]:
        raise ValueError("Missing model.name")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load and validate a TerraSight config file.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)

    print("Config loaded successfully")
    print(f"Experiment ID: {config['experiment']['id']}")
    print(f"Model: {config['model']['name']}")
    print(f"Bands: {config['data']['bands']}")


if __name__ == "__main__":
    main()