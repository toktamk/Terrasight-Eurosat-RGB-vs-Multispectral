import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import numpy as np

from terrasight.evaluation.confusion import compute_confusion_matrix
from terrasight.evaluation.metrics import compute_classification_metrics, compute_classwise_report


def test_compute_classification_metrics() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 1, 0, 2])

    metrics = compute_classification_metrics(y_true, y_pred)

    assert metrics["accuracy"] == 0.75
    assert "macro_f1" in metrics
    assert "weighted_f1" in metrics
    assert "balanced_accuracy" in metrics


def test_compute_classwise_report() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 1, 0, 2])

    report = compute_classwise_report(
        y_true,
        y_pred,
        target_names=["class_0", "class_1", "class_2"],
    )

    assert "class_0" in report
    assert "class_1" in report
    assert "class_2" in report


def test_compute_confusion_matrix() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 1, 0, 2])

    cm = compute_confusion_matrix(y_true, y_pred)

    assert cm.shape == (3, 3)
    assert cm.sum() == 4