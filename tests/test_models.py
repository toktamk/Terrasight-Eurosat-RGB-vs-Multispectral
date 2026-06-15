import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import torch

from terrasight.models.rgb_model import build_rgb_model
from terrasight.models.multispectral_model import build_multispectral_model


def test_rgb_model_forward_pass() -> None:
    model = build_rgb_model(
        model_name="resnet18",
        num_classes=10,
        pretrained=False,
    )

    x = torch.randn(2, 3, 64, 64)
    y = model(x)

    assert y.shape == (2, 10)


def test_multispectral_model_forward_pass() -> None:
    model = build_multispectral_model(
        model_name="resnet18",
        input_channels=13,
        num_classes=10,
        pretrained=False,
    )

    x = torch.randn(2, 13, 64, 64)
    y = model(x)

    assert y.shape == (2, 10)


def test_index_augmented_model_forward_pass() -> None:
    model = build_multispectral_model(
        model_name="resnet18",
        input_channels=16,
        num_classes=10,
        pretrained=False,
    )

    x = torch.randn(2, 16, 64, 64)
    y = model(x)

    assert y.shape == (2, 10)