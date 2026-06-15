from __future__ import annotations

import argparse
from pathlib import Path

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pandas as pd
from sklearn.model_selection import train_test_split

from terrasight.data.band_registry import CLASS_TO_INDEX, EUROSAT_CLASSES
from terrasight.utils.config import load_config


VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def find_samples(data_root: str | Path) -> pd.DataFrame:
    """Find EuroSAT samples in class-subfolder format."""

    root = Path(data_root)

    if not root.exists():
        raise FileNotFoundError(
            f"Data root not found: {root}. "
            "Place EuroSAT files under data/raw or update data.data_root in the config."
        )

    records: list[dict] = []

    for class_name in EUROSAT_CLASSES:
        class_dir = root / class_name

        if not class_dir.exists():
            continue

        for file_path in class_dir.rglob("*"):
            if file_path.suffix.lower() in VALID_IMAGE_EXTENSIONS:
                records.append(
                    {
                        "path": str(file_path),
                        "class_name": class_name,
                        "label": CLASS_TO_INDEX[class_name],
                    }
                )

    if not records:
        raise ValueError(
            f"No image files found under {root}. Expected class folders such as "
            f"{root / EUROSAT_CLASSES[0]}"
        )

    return pd.DataFrame(records)


def create_stratified_split(
    samples: pd.DataFrame,
    train_ratio: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create stratified train/test split."""

    train_df, test_df = train_test_split(
        samples,
        train_size=train_ratio,
        random_state=seed,
        stratify=samples["label"],
        shuffle=True,
    )

    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def save_split_files(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    split_dir: str | Path,
) -> None:
    split_path = Path(split_dir)
    split_path.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(split_path / "train.csv", index=False)
    test_df.to_csv(split_path / "test.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create EuroSAT stratified train/test split.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)

    data_root = config["data"]["data_root"]
    split_dir = config["data"]["split_dir"]
    train_ratio = float(config["data"]["split"]["train_ratio"])
    seed = int(config["seed"])

    samples = find_samples(data_root)
    train_df, test_df = create_stratified_split(samples, train_ratio, seed)
    save_split_files(train_df, test_df, split_dir)

    print("Split creation complete")
    print(f"Total samples: {len(samples)}")
    print(f"Train samples: {len(train_df)}")
    print(f"Test samples: {len(test_df)}")
    print(f"Split directory: {split_dir}")


if __name__ == "__main__":
    main()