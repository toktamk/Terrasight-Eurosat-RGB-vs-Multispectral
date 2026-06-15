from __future__ import annotations

import torch.nn as nn
from torchvision import models

from terrasight.models.model_utils import replace_classifier, replace_first_conv


SUPPORTED_BACKBONES = {
    "resnet18",
    "resnet34",
    "resnet50",
}


def _get_resnet_weights(name: str, pretrained: bool):
    if not pretrained:
        return None

    if name == "resnet18":
        return models.ResNet18_Weights.DEFAULT

    if name == "resnet34":
        return models.ResNet34_Weights.DEFAULT

    if name == "resnet50":
        return models.ResNet50_Weights.DEFAULT

    return None


def build_resnet_backbone(
    name: str,
    input_channels: int,
    num_classes: int,
    pretrained: bool = False,
) -> nn.Module:
    """Build a ResNet model with configurable input channels.

    If pretrained=True and input_channels > 3, ImageNet RGB weights are loaded
    first, then the first convolution is expanded to the requested number of
    channels using RGB-weight transfer.
    """

    if name not in SUPPORTED_BACKBONES:
        raise ValueError(f"Unsupported backbone: {name}. Supported: {SUPPORTED_BACKBONES}")

    weights = _get_resnet_weights(name=name, pretrained=pretrained)

    if name == "resnet18":
        model = models.resnet18(weights=weights)
    elif name == "resnet34":
        model = models.resnet34(weights=weights)
    else:
        model = models.resnet50(weights=weights)

    if input_channels != 3:
        model = replace_first_conv(
            model=model,
            input_channels=input_channels,
            preserve_pretrained=pretrained,
        )

    model = replace_classifier(model, num_classes=num_classes)

    return model


def build_model(
    name: str,
    input_channels: int,
    num_classes: int,
    pretrained: bool = False,
) -> nn.Module:
    """Generic model factory."""

    if name.startswith("resnet"):
        return build_resnet_backbone(
            name=name,
            input_channels=input_channels,
            num_classes=num_classes,
            pretrained=pretrained,
        )

    raise ValueError(f"Unsupported model name: {name}")