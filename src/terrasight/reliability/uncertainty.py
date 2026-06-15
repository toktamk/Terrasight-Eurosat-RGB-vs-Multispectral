from __future__ import annotations

import numpy as np
import torch


def predictive_entropy(probabilities: torch.Tensor, eps: float = 1e-8) -> np.ndarray:
    """Compute predictive entropy from class probabilities."""

    entropy = -torch.sum(probabilities * torch.log(probabilities + eps), dim=1)
    return entropy.cpu().numpy()


def confidence_margin(probabilities: torch.Tensor) -> np.ndarray:
    """Compute difference between top-1 and top-2 probabilities."""

    top2 = torch.topk(probabilities, k=2, dim=1).values
    margin = top2[:, 0] - top2[:, 1]

    return margin.cpu().numpy()


def confidence_error_flags(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    high_confidence_threshold: float = 0.9,
) -> dict[str, int]:
    """Count high-confidence correct and incorrect predictions."""

    correct = y_true == y_pred
    high_confidence = confidences >= high_confidence_threshold

    return {
        "high_confidence_correct": int(np.sum(high_confidence & correct)),
        "high_confidence_errors": int(np.sum(high_confidence & ~correct)),
        "low_confidence_correct": int(np.sum(~high_confidence & correct)),
        "low_confidence_errors": int(np.sum(~high_confidence & ~correct)),
    }