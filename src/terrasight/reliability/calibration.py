from __future__ import annotations

import numpy as np
import torch


def softmax_confidences(logits: torch.Tensor) -> tuple[np.ndarray, np.ndarray]:
    """Return predicted classes and confidence scores from logits."""

    probabilities = torch.softmax(logits, dim=1)
    confidences, predictions = torch.max(probabilities, dim=1)

    return predictions.cpu().numpy(), confidences.cpu().numpy()


def expected_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10,
) -> float:
    """Compute Expected Calibration Error."""

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for lower, upper in zip(bin_boundaries[:-1], bin_boundaries[1:]):
        in_bin = (confidences > lower) & (confidences <= upper)

        if not np.any(in_bin):
            continue

        bin_accuracy = np.mean(y_true[in_bin] == y_pred[in_bin])
        bin_confidence = np.mean(confidences[in_bin])
        bin_weight = np.mean(in_bin)

        ece += bin_weight * abs(bin_accuracy - bin_confidence)

    return float(ece)


def maximum_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10,
) -> float:
    """Compute Maximum Calibration Error."""

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    errors = []

    for lower, upper in zip(bin_boundaries[:-1], bin_boundaries[1:]):
        in_bin = (confidences > lower) & (confidences <= upper)

        if not np.any(in_bin):
            continue

        bin_accuracy = np.mean(y_true[in_bin] == y_pred[in_bin])
        bin_confidence = np.mean(confidences[in_bin])
        errors.append(abs(bin_accuracy - bin_confidence))

    if not errors:
        return 0.0

    return float(max(errors))


def brier_score(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    num_classes: int,
) -> float:
    """Compute multiclass Brier score."""

    one_hot = np.eye(num_classes)[y_true]
    score = np.mean(np.sum((probabilities - one_hot) ** 2, axis=1))

    return float(score)