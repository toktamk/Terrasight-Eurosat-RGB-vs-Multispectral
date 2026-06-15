from __future__ import annotations

import torch


def select_bands(
    image: torch.Tensor,
    source_bands: list[str],
    selected_bands: list[str],
) -> torch.Tensor:
    """Select specific bands from multispectral tensor.

    Args:
        image: Tensor with shape [C, H, W].
        source_bands: Band names corresponding to image channels.
        selected_bands: Band names to extract.

    Returns:
        Tensor with selected channels.
    """

    if image.ndim != 3:
        raise ValueError(f"Expected image shape [C, H, W], got {tuple(image.shape)}")

    missing = [band for band in selected_bands if band not in source_bands]

    if missing:
        raise ValueError(f"Selected bands missing from source bands: {missing}")

    band_to_index = {band: index for index, band in enumerate(source_bands)}
    indices = [band_to_index[band] for band in selected_bands]

    return image[indices, :, :]