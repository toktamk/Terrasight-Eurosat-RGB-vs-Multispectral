from __future__ import annotations

from typing import Callable

import torch
from torch import nn


@torch.no_grad()
def band_occlusion_scores(
    model: nn.Module,
    image: torch.Tensor,
    target_class: int,
    band_names: list[str],
    score_fn: Callable[[torch.Tensor, int], float] | None = None,
) -> dict[str, float]:
    """Compute band-occlusion attribution scores.

    Args:
        model: Classification model.
        image: Input tensor with shape [1, C, H, W].
        target_class: Class index to explain.
        band_names: Names of input bands.
        score_fn: Optional scoring function.

    Returns:
        Mapping from band name to drop in target-class probability.
    """

    if image.ndim != 4:
        raise ValueError(f"Expected image shape [1, C, H, W], got {tuple(image.shape)}")

    if image.shape[1] != len(band_names):
        raise ValueError(
            f"Number of bands ({image.shape[1]}) does not match band_names ({len(band_names)})."
        )

    model.eval()

    def default_score_fn(logits: torch.Tensor, cls: int) -> float:
        probs = torch.softmax(logits, dim=1)
        return float(probs[0, cls].item())

    score_function = score_fn or default_score_fn

    baseline_logits = model(image)
    baseline_score = score_function(baseline_logits, target_class)

    scores: dict[str, float] = {}

    for band_index, band_name in enumerate(band_names):
        occluded = image.clone()
        occluded[:, band_index, :, :] = 0.0

        logits = model(occluded)
        occluded_score = score_function(logits, target_class)

        scores[band_name] = float(baseline_score - occluded_score)

    return scores


def rank_band_importance(scores: dict[str, float]) -> list[tuple[str, float]]:
    """Rank bands by descending occlusion score."""

    return sorted(scores.items(), key=lambda item: item[1], reverse=True)