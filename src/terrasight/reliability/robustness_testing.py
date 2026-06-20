"""
Robustness testing utilities for TerraSight V5.

Supported perturbations:
- Gaussian noise
- brightness shift
- band dropout / band occlusion
- random spectral dropout

The core output is a report-ready table showing metric degradation relative to
the clean baseline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from torch import Tensor, nn

from terrasight.explainability.band_occlusion import unpack_batch, predict_probabilities


PerturbationFn = Callable[[Tensor], Tensor]


@dataclass(frozen=True)
class Perturbation:
    """Named perturbation used in robustness testing."""

    name: str
    function: PerturbationFn
    description: str


def gaussian_noise(std: float = 0.05, clamp: Optional[Tuple[float, float]] = None) -> Perturbation:
    """Create a Gaussian noise perturbation."""
    def apply(images: Tensor) -> Tensor:
        noisy = images + torch.randn_like(images) * float(std)
        if clamp is not None:
            noisy = noisy.clamp(float(clamp[0]), float(clamp[1]))
        return noisy

    return Perturbation(
        name=f"gaussian_noise_std_{std:g}",
        function=apply,
        description=f"Add Gaussian noise with std={std}.",
    )


def brightness_shift(delta: float = 0.10, clamp: Optional[Tuple[float, float]] = None) -> Perturbation:
    """Create a brightness-shift perturbation."""
    def apply(images: Tensor) -> Tensor:
        shifted = images + float(delta)
        if clamp is not None:
            shifted = shifted.clamp(float(clamp[0]), float(clamp[1]))
        return shifted

    sign = "plus" if delta >= 0 else "minus"
    return Perturbation(
        name=f"brightness_{sign}_{abs(delta):g}",
        function=apply,
        description=f"Add brightness delta={delta}.",
    )


def dropout_band(
    band_index: int,
    fill_value: float = 0.0,
    band_name: Optional[str] = None,
) -> Perturbation:
    """Create a perturbation that replaces one channel with a constant."""
    label = band_name if band_name is not None else f"band_{band_index}"

    def apply(images: Tensor) -> Tensor:
        if images.ndim != 4:
            raise ValueError(f"Expected [B, C, H, W], got {tuple(images.shape)}.")
        if band_index < 0 or band_index >= images.shape[1]:
            raise IndexError(f"Band index {band_index} out of range for {images.shape[1]} channels.")
        out = images.clone()
        out[:, band_index, :, :] = float(fill_value)
        return out

    return Perturbation(
        name=f"dropout_{label}",
        function=apply,
        description=f"Replace {label} with {fill_value}.",
    )


def random_band_dropout(
    probability: float = 0.10,
    fill_value: float = 0.0,
) -> Perturbation:
    """Create a perturbation that randomly drops channels per sample."""
    def apply(images: Tensor) -> Tensor:
        if images.ndim != 4:
            raise ValueError(f"Expected [B, C, H, W], got {tuple(images.shape)}.")
        mask = torch.rand(images.shape[0], images.shape[1], 1, 1, device=images.device) > float(probability)
        return images * mask.to(images.dtype) + float(fill_value) * (~mask).to(images.dtype)

    return Perturbation(
        name=f"random_band_dropout_p_{probability:g}",
        function=apply,
        description=f"Randomly drop each band with probability={probability}.",
    )


@torch.no_grad()
def evaluate_predictions(
    model: nn.Module,
    dataloader: Iterable[Any],
    perturbation: Optional[Perturbation] = None,
    device: Optional[Union[str, torch.device]] = None,
    max_batches: Optional[int] = None,
) -> pd.DataFrame:
    """Return a prediction table for clean or perturbed inputs."""
    run_device = torch.device(device) if device is not None else next(model.parameters()).device
    model = model.to(run_device)
    model.eval()

    records: List[Dict[str, Any]] = []
    sample_offset = 0

    for batch_idx, raw_batch in enumerate(dataloader):
        if max_batches is not None and batch_idx >= max_batches:
            break

        batch = unpack_batch(raw_batch)
        images = batch.images.to(run_device)
        labels = batch.labels.to(run_device).long()

        if perturbation is not None:
            images = perturbation.function(images)

        probs = predict_probabilities(model, images)
        conf, pred = probs.max(dim=1)

        for i in range(images.shape[0]):
            records.append(
                {
                    "sample_index": sample_offset + i,
                    "batch_index": batch_idx,
                    "true_label": int(labels[i].item()),
                    "pred_label": int(pred[i].item()),
                    "confidence": float(conf[i].item()),
                    "correct": bool(pred[i].item() == labels[i].item()),
                }
            )

        sample_offset += images.shape[0]

    return pd.DataFrame.from_records(records)


def compute_classification_metrics(prediction_df: pd.DataFrame) -> Dict[str, float]:
    """Compute accuracy, macro-F1, weighted-F1, and balanced accuracy."""
    y_true = prediction_df["true_label"].to_numpy()
    y_pred = prediction_df["pred_label"].to_numpy()

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "mean_confidence": float(prediction_df["confidence"].mean()),
        "n_samples": float(len(prediction_df)),
    }


def default_robustness_suite(
    n_channels: int,
    band_names: Optional[Sequence[str]] = None,
) -> List[Perturbation]:
    """Create a practical default suite for multispectral image classification."""
    suite: List[Perturbation] = [
        gaussian_noise(std=0.02),
        gaussian_noise(std=0.05),
        brightness_shift(delta=0.05),
        brightness_shift(delta=-0.05),
        random_band_dropout(probability=0.10),
    ]

    names = list(band_names) if band_names is not None else [f"band_{i}" for i in range(n_channels)]
    for idx in range(n_channels):
        suite.append(dropout_band(idx, band_name=names[idx]))

    return suite


def run_robustness_suite(
    model: nn.Module,
    dataloader: Iterable[Any],
    output_dir: Union[str, Path],
    perturbations: Optional[Sequence[Perturbation]] = None,
    n_channels: Optional[int] = None,
    band_names: Optional[Sequence[str]] = None,
    device: Optional[Union[str, torch.device]] = None,
    max_batches: Optional[int] = None,
) -> pd.DataFrame:
    """Run clean and perturbed evaluations, then report metric degradation."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    clean_predictions = evaluate_predictions(
        model=model,
        dataloader=dataloader,
        perturbation=None,
        device=device,
        max_batches=max_batches,
    )
    clean_predictions.to_csv(out / "robustness_predictions_clean.csv", index=False)
    clean_metrics = compute_classification_metrics(clean_predictions)

    if perturbations is None:
        if n_channels is None:
            # Infer channels from first batch without consuming the original iterator if it is a list.
            if not hasattr(dataloader, "__iter__"):
                raise ValueError("Cannot infer channels from non-iterable dataloader.")
            first_batch = next(iter(dataloader))
            n_channels = unpack_batch(first_batch).images.shape[1]
        perturbations = default_robustness_suite(n_channels=n_channels, band_names=band_names)

    records: List[Dict[str, float]] = []
    records.append({
        "perturbation": "clean",
        "description": "No perturbation.",
        **clean_metrics,
        "accuracy_drop": 0.0,
        "macro_f1_drop": 0.0,
        "balanced_accuracy_drop": 0.0,
    })

    for perturbation in perturbations:
        pred_df = evaluate_predictions(
            model=model,
            dataloader=dataloader,
            perturbation=perturbation,
            device=device,
            max_batches=max_batches,
        )
        pred_df.to_csv(out / f"robustness_predictions_{perturbation.name}.csv", index=False)

        metrics = compute_classification_metrics(pred_df)
        records.append({
            "perturbation": perturbation.name,
            "description": perturbation.description,
            **metrics,
            "accuracy_drop": clean_metrics["accuracy"] - metrics["accuracy"],
            "macro_f1_drop": clean_metrics["macro_f1"] - metrics["macro_f1"],
            "balanced_accuracy_drop": clean_metrics["balanced_accuracy"] - metrics["balanced_accuracy"],
        })

    summary = pd.DataFrame.from_records(records)
    summary = summary.sort_values("macro_f1_drop", ascending=False).reset_index(drop=True)
    summary.to_csv(out / "robustness_summary.csv", index=False)

    return summary
