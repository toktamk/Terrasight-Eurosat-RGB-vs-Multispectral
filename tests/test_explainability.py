import torch
import torch.nn as nn

from terrasight.explainability.gradcam import GradCAM
from terrasight.explainability.spectral_attribution import (
    band_occlusion_scores,
    rank_band_importance,
)


class TinyCNN(nn.Module):
    def __init__(self, input_channels: int = 3, num_classes: int = 2) -> None:
        super().__init__()
        self.conv = nn.Conv2d(input_channels, 4, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(4, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.relu(self.conv(x))
        x = self.pool(x).flatten(1)
        return self.fc(x)


def test_gradcam_generates_heatmap() -> None:
    model = TinyCNN(input_channels=3, num_classes=2)
    target_layer = model.conv

    gradcam = GradCAM(model=model, target_layer=target_layer)

    image = torch.randn(1, 3, 32, 32)
    heatmap = gradcam.generate(image=image, class_index=1)

    gradcam.close()

    assert heatmap.shape == (32, 32)
    assert torch.all(heatmap >= 0)
    assert torch.all(heatmap <= 1)


def test_band_occlusion_scores() -> None:
    model = TinyCNN(input_channels=3, num_classes=2)
    image = torch.randn(1, 3, 32, 32)
    band_names = ["B4", "B3", "B2"]

    scores = band_occlusion_scores(
        model=model,
        image=image,
        target_class=1,
        band_names=band_names,
    )

    assert set(scores.keys()) == set(band_names)


def test_rank_band_importance() -> None:
    scores = {
        "B4": 0.1,
        "B3": 0.3,
        "B2": -0.2,
    }

    ranked = rank_band_importance(scores)

    assert ranked[0][0] == "B3"
    assert ranked[-1][0] == "B2"