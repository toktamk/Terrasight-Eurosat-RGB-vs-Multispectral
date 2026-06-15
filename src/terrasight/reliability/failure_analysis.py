from __future__ import annotations

from collections import Counter

import numpy as np


def extract_failure_indices(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> list[int]:
    """Return indices where prediction is incorrect."""

    return np.where(y_true != y_pred)[0].tolist()


def confusion_pairs(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: list[str],
    top_k: int = 10,
) -> list[dict[str, object]]:
    """Return most frequent true/predicted failure pairs."""

    failures = y_true != y_pred
    pairs = list(zip(y_true[failures], y_pred[failures]))

    counter = Counter(pairs)

    output = []
    for (true_label, pred_label), count in counter.most_common(top_k):
        output.append(
            {
                "true_class": class_names[int(true_label)],
                "predicted_class": class_names[int(pred_label)],
                "count": int(count),
            }
        )

    return output


def worst_classes_by_f1(
    classwise_report: dict,
    top_k: int = 5,
) -> list[dict[str, object]]:
    """Extract worst classes from a sklearn classification_report dictionary."""

    rows = []

    for class_name, values in classwise_report.items():
        if not isinstance(values, dict):
            continue

        if "f1-score" not in values:
            continue

        rows.append(
            {
                "class_name": class_name,
                "f1_score": float(values["f1-score"]),
                "precision": float(values["precision"]),
                "recall": float(values["recall"]),
                "support": int(values["support"]),
            }
        )

    rows.sort(key=lambda item: item["f1_score"])

    return rows[:top_k]