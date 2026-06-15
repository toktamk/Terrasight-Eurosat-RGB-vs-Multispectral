from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch.nn as nn


def build_loss(name: str = "cross_entropy") -> nn.Module:
    """Build loss function."""

    name = name.lower()

    if name in {"cross_entropy", "ce"}:
        return nn.CrossEntropyLoss()

    raise ValueError(f"Unsupported loss function: {name}")