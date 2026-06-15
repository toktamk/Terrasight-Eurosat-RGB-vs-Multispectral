from __future__ import annotations

from typing import Callable

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
from torchvision import transforms


RGB_MEAN = [0.485, 0.456, 0.406]
RGB_STD = [0.229, 0.224, 0.225]


def get_rgb_transform(train: bool = False) -> Callable:
    """Return RGB preprocessing transform."""

    transform_steps = []

    if train:
        transform_steps.extend(
            [
                transforms.RandomHorizontalFlip(),
                transforms.RandomVerticalFlip(),
            ]
        )

    transform_steps.extend(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=RGB_MEAN, std=RGB_STD),
        ]
    )

    return transforms.Compose(transform_steps)


def normalize_multispectral_tensor(
    image: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Channel-wise normalize a multispectral tensor.

    Expected shape:
        [C, H, W]
    """

    if image.ndim != 3:
        raise ValueError(f"Expected tensor shape [C, H, W], got {tuple(image.shape)}")

    mean = image.mean(dim=(1, 2), keepdim=True)
    std = image.std(dim=(1, 2), keepdim=True)

    return (image - mean) / (std + eps)


def minmax_scale_tensor(
    image: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Scale tensor values to [0, 1]."""

    min_value = image.amin(dim=(-2, -1), keepdim=True)
    max_value = image.amax(dim=(-2, -1), keepdim=True)

    return (image - min_value) / (max_value - min_value + eps)