from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch


def _safe_normalized_difference(
    numerator_a: torch.Tensor,
    numerator_b: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute safe normalized difference."""

    return (numerator_a - numerator_b) / (numerator_a + numerator_b + eps)


def compute_ndvi(
    nir: torch.Tensor,
    red: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute NDVI.

    NDVI = (NIR - Red) / (NIR + Red)
    """

    return _safe_normalized_difference(nir, red, eps)


def compute_ndwi(
    green: torch.Tensor,
    nir: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute McFeeters-style NDWI.

    NDWI = (Green - NIR) / (Green + NIR)
    """

    return _safe_normalized_difference(green, nir, eps)


def compute_ndbi(
    swir: torch.Tensor,
    nir: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute NDBI.

    NDBI = (SWIR - NIR) / (SWIR + NIR)
    """

    return _safe_normalized_difference(swir, nir, eps)


def append_indices_to_multispectral(
    image: torch.Tensor,
    band_names: list[str],
) -> torch.Tensor:
    """Append NDVI, NDWI, and NDBI to a multispectral tensor.

    Expected image shape:
        [C, H, W]

    Required bands:
        B3 = Green
        B4 = Red
        B8 = NIR
        B11 = SWIR1
    """

    if image.ndim != 3:
        raise ValueError(f"Expected image shape [C, H, W], got {tuple(image.shape)}")

    required_bands = ["B3", "B4", "B8", "B11"]
    missing = [band for band in required_bands if band not in band_names]

    if missing:
        raise ValueError(f"Missing required bands for spectral indices: {missing}")

    band_to_index = {band: index for index, band in enumerate(band_names)}

    green = image[band_to_index["B3"]]
    red = image[band_to_index["B4"]]
    nir = image[band_to_index["B8"]]
    swir = image[band_to_index["B11"]]

    ndvi = compute_ndvi(nir=nir, red=red).unsqueeze(0)
    ndwi = compute_ndwi(green=green, nir=nir).unsqueeze(0)
    ndbi = compute_ndbi(swir=swir, nir=nir).unsqueeze(0)

    return torch.cat([image, ndvi, ndwi, ndbi], dim=0)