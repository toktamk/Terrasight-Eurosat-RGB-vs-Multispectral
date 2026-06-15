import numpy as np
import torch

from terrasight.reliability.calibration import (
    expected_calibration_error,
    maximum_calibration_error,
    softmax_confidences,
)
from terrasight.reliability.failure_analysis import (
    confusion_pairs,
    extract_failure_indices,
)
from terrasight.reliability.robustness import (
    add_gaussian_noise,
    apply_brightness_shift,
    compute_degradation,
    dropout_bands,
)
from terrasight.reliability.uncertainty import (
    confidence_error_flags,
    confidence_margin,
    predictive_entropy,
)


def test_softmax_confidences() -> None:
    logits = torch.tensor([[3.0, 1.0], [0.2, 2.0]])

    predictions, confidences = softmax_confidences(logits)

    assert predictions.tolist() == [0, 1]
    assert confidences.shape == (2,)


def test_expected_calibration_error() -> None:
    y_true = np.array([0, 1, 1, 0])
    y_pred = np.array([0, 1, 0, 0])
    confidences = np.array([0.9, 0.8, 0.7, 0.6])

    ece = expected_calibration_error(y_true, y_pred, confidences)

    assert isinstance(ece, float)
    assert ece >= 0.0


def test_maximum_calibration_error() -> None:
    y_true = np.array([0, 1, 1, 0])
    y_pred = np.array([0, 1, 0, 0])
    confidences = np.array([0.9, 0.8, 0.7, 0.6])

    mce = maximum_calibration_error(y_true, y_pred, confidences)

    assert isinstance(mce, float)
    assert mce >= 0.0


def test_predictive_entropy() -> None:
    probs = torch.tensor([[0.8, 0.2], [0.5, 0.5]])

    entropy = predictive_entropy(probs)

    assert entropy.shape == (2,)
    assert entropy[1] > entropy[0]


def test_confidence_margin() -> None:
    probs = torch.tensor([[0.8, 0.2], [0.55, 0.45]])

    margin = confidence_margin(probs)

    assert margin.shape == (2,)
    assert margin[0] > margin[1]


def test_confidence_error_flags() -> None:
    y_true = np.array([0, 1, 1])
    y_pred = np.array([0, 0, 1])
    confidences = np.array([0.95, 0.91, 0.4])

    flags = confidence_error_flags(y_true, y_pred, confidences)

    assert flags["high_confidence_correct"] == 1
    assert flags["high_confidence_errors"] == 1


def test_failure_indices() -> None:
    y_true = np.array([0, 1, 2])
    y_pred = np.array([0, 2, 2])

    failures = extract_failure_indices(y_true, y_pred)

    assert failures == [1]


def test_confusion_pairs() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 2, 2, 1])
    class_names = ["A", "B", "C"]

    pairs = confusion_pairs(y_true, y_pred, class_names)

    assert pairs[0]["true_class"] == "B"
    assert pairs[0]["predicted_class"] == "C"
    assert pairs[0]["count"] == 2


def test_robustness_transforms() -> None:
    images = torch.ones((2, 13, 4, 4))

    noisy = add_gaussian_noise(images, std=0.01)
    bright = apply_brightness_shift(images, shift=0.1)
    dropped = dropout_bands(images, band_indices=[0, 1])

    assert noisy.shape == images.shape
    assert bright.shape == images.shape
    assert torch.all(dropped[:, 0, :, :] == 0)
    assert torch.all(dropped[:, 1, :, :] == 0)


def test_compute_degradation() -> None:
    degradation = compute_degradation(clean_metric=0.95, perturbed_metric=0.90)

    assert abs(degradation - 0.05) < 1e-8