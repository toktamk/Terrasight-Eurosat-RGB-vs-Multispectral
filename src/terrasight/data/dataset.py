from __future__ import annotations

from pathlib import Path
from typing import Callable

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pandas as pd
from PIL import Image

from terrasight.data.band_registry import CLASS_TO_INDEX


class EuroSATRGBDataset:
    """EuroSAT RGB dataset using image paths from a split CSV."""

    def __init__(
        self,
        split_csv: str | Path,
        transform: Callable | None = None,
    ) -> None:
        self.split_csv = Path(split_csv)
        self.transform = transform

        if not self.split_csv.exists():
            raise FileNotFoundError(f"Split CSV not found: {self.split_csv}")

        self.samples = pd.read_csv(self.split_csv)

        required_columns = {"path", "label", "class_name"}
        missing = required_columns - set(self.samples.columns)
        if missing:
            raise ValueError(f"Missing columns in split CSV: {missing}")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        row = self.samples.iloc[index]
        image_path = Path(row["path"])

        image = Image.open(image_path).convert("RGB")
        label = int(row["label"])

        if self.transform is not None:
            image = self.transform(image)

        metadata = {
            "path": str(image_path),
            "class_name": row["class_name"],
        }

        return image, label, metadata


class EuroSATMSDataset:
    """EuroSAT multispectral dataset using RGB split CSV mapped to TIFF files."""

    def __init__(
        self,
        split_csv: str | Path,
        multispectral_root: str | Path,
        transform: Callable | None = None,
        source_bands: list[str] | None = None,
        selected_bands: list[str] | None = None,
    ) -> None:
        from terrasight.data.band_registry import SENTINEL2_BANDS

        self.source_bands = source_bands or SENTINEL2_BANDS
        self.selected_bands = selected_bands
        self.split_csv = Path(split_csv)
        self.multispectral_root = Path(multispectral_root)
        self.transform = transform

        if not self.split_csv.exists():
            raise FileNotFoundError(f"Split CSV not found: {self.split_csv}")

        if not self.multispectral_root.exists():
            raise FileNotFoundError(f"Multispectral root not found: {self.multispectral_root}")

        self.samples = pd.read_csv(self.split_csv)

        required_columns = {"path", "label", "class_name"}
        missing = required_columns - set(self.samples.columns)
        if missing:
            raise ValueError(f"Missing columns in split CSV: {missing}")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        import torch
        import tifffile

        row = self.samples.iloc[index]

        rgb_path = Path(row["path"])
        class_name = row["class_name"]
        tif_name = rgb_path.with_suffix(".tif").name
        tif_path = self.multispectral_root / class_name / tif_name

        if not tif_path.exists():
            raise FileNotFoundError(f"Multispectral TIFF not found: {tif_path}")

        image = tifffile.imread(tif_path)

        if image.ndim != 3:
            raise ValueError(f"Expected multispectral image with 3 dimensions, got {image.shape}")

        image = torch.tensor(image, dtype=torch.float32)

        if image.shape[-1] == 13:
            image = image.permute(2, 0, 1)

        if self.selected_bands is not None:
            from terrasight.features.band_selection import select_bands

            image = select_bands(
                image=image,
                source_bands=self.source_bands,
                selected_bands=self.selected_bands,
            )
            
        label = int(row["label"])

        if self.transform is not None:
            image = self.transform(image)

        metadata = {
            "path": str(tif_path),
            "class_name": class_name,
        }

        return image, label, metadata

def class_name_to_label(class_name: str) -> int:
    if class_name not in CLASS_TO_INDEX:
        raise ValueError(f"Unknown EuroSAT class name: {class_name}")
    return CLASS_TO_INDEX[class_name]