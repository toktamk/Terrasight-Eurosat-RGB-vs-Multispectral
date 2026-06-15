from __future__ import annotations

import torch


def add_gaussian_noise(
    images: torch.Tensor,
    std: float = 0.05,
) -> torch.Tensor:
    """Add Gaussian noise to image tensor."""

    noise = torch.randn_like(images) * std
    return images + noise


def apply_brightness_shift(
    images: torch.Tensor,
    shift: float = 0.1,
) -> torch.Tensor:
    """Apply additive brightness shift."""

    return images + shift


def dropout_bands(
    images: torch.Tensor,
    band_indices: list[int],
) -> torch.Tensor:
    """Zero selected spectral bands.

    Expected image shape:
        [B, C, H, W]
    """

    output = images.clone()

    for band_index in band_indices:
        output[:, band_index, :, :] = 0.0

    return output


def compute_degradation(
    clean_metric: float,
    perturbed_metric: float,
) -> float:
    """Compute metric degradation."""

    return float(clean_metric - perturbed_metric)