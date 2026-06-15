from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch.nn as nn

from terrasight.models.backbone_factory import build_model


def build_multispectral_model(
    model_name: str = "resnet18",
    input_channels: int = 13,
    num_classes: int = 10,
    pretrained: bool = False,
) -> nn.Module:
    """Build multispectral classification model."""

    return build_model(
        name=model_name,
        input_channels=input_channels,
        num_classes=num_classes,
        pretrained=pretrained,
    )