from __future__ import annotations

import torch
import torch.nn as nn


def replace_first_conv(
    model: nn.Module,
    input_channels: int,
    preserve_pretrained: bool = True,
) -> nn.Module:
    """Replace ResNet first conv and optionally transfer pretrained RGB weights."""

    if not hasattr(model, "conv1"):
        raise ValueError("Model does not have attribute 'conv1'.")

    old_conv = model.conv1

    new_conv = nn.Conv2d(
        in_channels=input_channels,
        out_channels=old_conv.out_channels,
        kernel_size=old_conv.kernel_size,
        stride=old_conv.stride,
        padding=old_conv.padding,
        bias=old_conv.bias is not None,
    )

    if preserve_pretrained:
        with torch.no_grad():
            if input_channels >= 3:
                new_conv.weight[:, :3, :, :] = old_conv.weight[:, :3, :, :]

                if input_channels > 3:
                    mean_weight = old_conv.weight.mean(dim=1, keepdim=True)
                    for channel in range(3, input_channels):
                        new_conv.weight[:, channel : channel + 1, :, :] = mean_weight
            else:
                new_conv.weight[:, :, :, :] = old_conv.weight[:, :input_channels, :, :]

            if old_conv.bias is not None and new_conv.bias is not None:
                new_conv.bias.copy_(old_conv.bias)

    model.conv1 = new_conv
    return model


def replace_classifier(
    model: nn.Module,
    num_classes: int,
) -> nn.Module:
    """Replace final classifier layer of a ResNet-style model."""

    if not hasattr(model, "fc"):
        raise ValueError("Model does not have attribute 'fc'.")

    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    return model