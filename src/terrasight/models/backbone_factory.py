from __future__ import annotations

import torch.nn as nn
from torchvision import models

from terrasight.models.model_utils import replace_classifier, replace_first_conv


SUPPORTED_BACKBONES = {
    "resnet18",
    "resnet50",
    "efficientnet_b0",
    "efficientnet_b2",
}


def _get_pretrained_weights(name: str, pretrained: bool):
    if not pretrained:
        return None

    if name == "resnet18":
        return models.ResNet18_Weights.DEFAULT

    if name == "resnet50":
        return models.ResNet50_Weights.DEFAULT

    if name == "efficientnet_b0":
        return models.EfficientNet_B0_Weights.DEFAULT

    if name == "efficientnet_b2":
        return models.EfficientNet_B2_Weights.DEFAULT

    return None


def build_model_backbone(
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

    weights = _get_pretrained_weights(name=name, pretrained=pretrained)

    if name == "resnet18":
        model = models.resnet18(weights=weights)
    elif name == "resnet50":
        model = models.resnet50(weights=weights)
    elif name == "efficientnet_b0":
        model = models.efficientnet_b0(weights=weights)
    elif name == "efficientnet_b2":
        model = models.efficientnet_b2(weights=weights)
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

    return build_model_backbone(
            name=name,
            input_channels=input_channels,
            num_classes=num_classes,
            pretrained=pretrained,
    )

    raise ValueError(f"Unsupported model name: {name}")