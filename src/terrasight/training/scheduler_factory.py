from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch


def build_scheduler(
    optimizer: torch.optim.Optimizer,
    name: str | None = None,
    epochs: int = 30,
):
    """Build learning-rate scheduler.

    Returns None if no scheduler is requested.
    """

    if name is None:
        return None

    name = name.lower()

    if name in {"none", "null"}:
        return None

    if name == "cosine":
        return torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=epochs,
        )

    if name == "plateau":
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode="min",
            patience=3,
            factor=0.5,
        )

    raise ValueError(f"Unsupported scheduler: {name}")