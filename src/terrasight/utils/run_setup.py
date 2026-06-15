from __future__ import annotations

import argparse
import json
import platform
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from terrasight.utils.config import load_config
from terrasight.utils.reproducibility import get_seed_from_config, set_seed


def create_run_dir(config: dict[str, Any], base_dir: str | Path = "results") -> Path:
    """Create a timestamped run directory."""

    experiment_id = config["experiment"]["id"]
    version = config["experiment"].get("version", "unknown_version")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = Path(base_dir) / version / f"{timestamp}_{experiment_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    return run_dir


def save_config_copy(config_path: str | Path, run_dir: Path) -> None:
    """Copy original config file into run directory."""

    config_path = Path(config_path)
    destination = run_dir / "config.yaml"
    shutil.copy2(config_path, destination)


def save_metadata(config: dict[str, Any], run_dir: Path) -> None:
    """Save reproducibility metadata."""

    metadata = {
        "experiment_id": config["experiment"]["id"],
        "version": config["experiment"].get("version"),
        "seed": config.get("seed"),
        "created_at": datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }

    metadata_path = run_dir / "metadata.json"

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def setup_run(config_path: str | Path) -> Path:
    """Load config, set seed, create run directory, and save metadata."""

    config = load_config(config_path)

    seed = get_seed_from_config(config)
    set_seed(seed)

    run_dir = create_run_dir(config)
    save_config_copy(config_path, run_dir)
    save_metadata(config, run_dir)

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare reproducible TerraSight run folder.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    run_dir = setup_run(args.config)

    print("Run setup complete")
    print(f"Run directory: {run_dir}")


if __name__ == "__main__":
    main()