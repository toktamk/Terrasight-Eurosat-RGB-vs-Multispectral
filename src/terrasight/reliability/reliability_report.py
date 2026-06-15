from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from terrasight.reliability.calibration import (
    expected_calibration_error,
    maximum_calibration_error,
)
from terrasight.reliability.failure_analysis import (
    confusion_pairs,
    extract_failure_indices,
)


def build_reliability_summary(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    class_names: list[str],
) -> dict:
    """Build reliability summary dictionary."""

    failures = extract_failure_indices(y_true, y_pred)

    return {
        "ece": expected_calibration_error(y_true, y_pred, confidences),
        "mce": maximum_calibration_error(y_true, y_pred, confidences),
        "num_samples": int(len(y_true)),
        "num_failures": int(len(failures)),
        "failure_rate": float(len(failures) / len(y_true)),
        "top_confusion_pairs": confusion_pairs(
            y_true=y_true,
            y_pred=y_pred,
            class_names=class_names,
        ),
    }


def save_reliability_summary(
    summary: dict,
    output_path: str | Path,
) -> None:
    """Save reliability summary as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)