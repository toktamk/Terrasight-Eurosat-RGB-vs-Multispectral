from __future__ import annotations

from pathlib import Path

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


def compute_confusion_matrix(
    y_true: list[int] | np.ndarray,
    y_pred: list[int] | np.ndarray,
) -> np.ndarray:
    """Compute confusion matrix."""

    return confusion_matrix(y_true, y_pred)


def save_confusion_matrix_plot(
    y_true: list[int] | np.ndarray,
    y_pred: list[int] | np.ndarray,
    class_names: list[str],
    output_path: str | Path,
    normalize: str | None = None,
) -> None:
    """Save confusion matrix figure."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cm = confusion_matrix(y_true, y_pred, normalize=normalize)

    fig, ax = plt.subplots(figsize=(10, 10))
    display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    display.plot(ax=ax, xticks_rotation=45, colorbar=True)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)