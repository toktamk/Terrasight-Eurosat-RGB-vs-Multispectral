"""
Band-occlusion analysis utilities for TerraSight V5.

Purpose
-------
Estimate the contribution of each Sentinel-2 band by occluding one band at a
time and measuring the change in model confidence and correctness.

This module is intentionally independent from the training pipeline. It accepts
any PyTorch model and any dataloader that returns one of:

1. (images, labels)
2. (images, labels, metadata)
3. {"image": images, "label": labels, ...}

Images must be shaped [B, C, H, W].
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import torch
from torch import Tensor, nn


DEFAULT_SENTINEL2_BANDS: List[str] = [
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8A", "B9", "B10", "B11", "B12"
]


@dataclass(frozen=True)
class Batch:
    """Normalized representation of a dataloader batch."""

    images: Tensor
    labels: Tensor
    metadata: Optional[Any] = None


def unpack_batch(batch: Any) -> Batch:
    """Extract image tensor, label tensor, and optional metadata from a batch."""
    if isinstance(batch, Mapping):
        image_key = "image" if "image" in batch else "images"
        label_key = "label" if "label" in batch else "labels"
        metadata = batch.get("metadata", batch.get("meta", None))
        return Batch(images=batch[image_key], labels=batch[label_key], metadata=metadata)

    if isinstance(batch, (tuple, list)):
        if len(batch) == 2:
            images, labels = batch
            return Batch(images=images, labels=labels)
        if len(batch) >= 3:
            images, labels, metadata = batch[0], batch[1], batch[2]
            return Batch(images=images, labels=labels, metadata=metadata)

    raise TypeError(
        "Unsupported batch format. Expected dict, (images, labels), or "
        "(images, labels, metadata)."
    )


def _as_device_tensor(x: Union[float, int, Tensor], reference: Tensor) -> Tensor:
    if isinstance(x, Tensor):
        return x.to(device=reference.device, dtype=reference.dtype)
    return torch.tensor(float(x), device=reference.device, dtype=reference.dtype)


def occlude_bands(
    images: Tensor,
    band_indices: Sequence[int],
    strategy: str = "zero",
    fill_values: Optional[Union[Tensor, Sequence[float], float]] = None,
) -> Tensor:
    """Return a copy of images with selected channels occluded.

    Parameters
    ----------
    images:
        Input tensor of shape [B, C, H, W].
    band_indices:
        Channel indices to occlude.
    strategy:
        One of {"zero", "mean", "constant"}.
    fill_values:
        Required for strategy="mean" or "constant" if custom values are needed.
        For per-band means, pass a vector of shape [C] or [len(band_indices)].

    Returns
    -------
    Tensor
        Occluded image tensor with the same shape as input.
    """
    if images.ndim != 4:
        raise ValueError(f"Expected images with shape [B, C, H, W], got {tuple(images.shape)}.")

    occluded = images.clone()
    channels = images.shape[1]

    for band_idx in band_indices:
        if band_idx < 0 or band_idx >= channels:
            raise IndexError(f"Band index {band_idx} out of range for {channels} channels.")

    if strategy == "zero":
        occluded[:, list(band_indices), :, :] = 0.0
        return occluded

    if strategy not in {"mean", "constant"}:
        raise ValueError("strategy must be one of {'zero', 'mean', 'constant'}.")

    if fill_values is None:
        raise ValueError(f"fill_values is required for strategy='{strategy}'.")

    fill_tensor = _as_device_tensor(fill_values, images)

    if fill_tensor.ndim == 0:
        for band_idx in band_indices:
            occluded[:, band_idx, :, :] = fill_tensor
        return occluded

    if fill_tensor.numel() == channels:
        for band_idx in band_indices:
            occluded[:, band_idx, :, :] = fill_tensor[band_idx]
        return occluded

    if fill_tensor.numel() == len(band_indices):
        for local_idx, band_idx in enumerate(band_indices):
            occluded[:, band_idx, :, :] = fill_tensor[local_idx]
        return occluded

    raise ValueError(
        "fill_values must be scalar, length C, or length equal to len(band_indices)."
    )


@torch.no_grad()
def predict_probabilities(model: nn.Module, images: Tensor) -> Tensor:
    """Run model inference and return softmax probabilities."""
    logits = model(images)
    if isinstance(logits, (tuple, list)):
        logits = logits[0]
    return torch.softmax(logits, dim=1)


def _safe_metadata_value(metadata: Optional[Any], row_idx: int) -> Optional[Any]:
    if metadata is None:
        return None
    try:
        if isinstance(metadata, Mapping):
            return {key: value[row_idx] if hasattr(value, "__len__") else value for key, value in metadata.items()}
        return metadata[row_idx]
    except Exception:
        return None


@torch.no_grad()
def run_band_occlusion(
    model: nn.Module,
    dataloader: Iterable[Any],
    band_names: Optional[Sequence[str]] = None,
    occlusion_strategy: str = "zero",
    fill_values: Optional[Union[Tensor, Sequence[float], float]] = None,
    target_mode: str = "predicted",
    device: Optional[Union[str, torch.device]] = None,
    max_batches: Optional[int] = None,
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Run one-band-at-a-time occlusion and return a per-sample detail table.

    target_mode:
        "predicted": measure confidence drop for the original predicted class.
        "true": measure confidence drop for the ground-truth class.
    """
    if target_mode not in {"predicted", "true"}:
        raise ValueError("target_mode must be 'predicted' or 'true'.")

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

        base_probs = predict_probabilities(model, images)
        base_conf, base_pred = base_probs.max(dim=1)

        channels = images.shape[1]
        names = list(band_names) if band_names is not None else [f"band_{i}" for i in range(channels)]
        if len(names) != channels:
            raise ValueError(f"Expected {channels} band names, got {len(names)}.")

        target_class = base_pred if target_mode == "predicted" else labels
        base_target_conf = base_probs[torch.arange(images.shape[0]), target_class]

        for band_idx, band_name in enumerate(names):
            occluded_images = occlude_bands(
                images=images,
                band_indices=[band_idx],
                strategy=occlusion_strategy,
                fill_values=fill_values,
            )
            occ_probs = predict_probabilities(model, occluded_images)
            occ_conf, occ_pred = occ_probs.max(dim=1)
            occ_target_conf = occ_probs[torch.arange(images.shape[0]), target_class]

            confidence_drop = base_target_conf - occ_target_conf
            prediction_changed = occ_pred != base_pred

            for i in range(images.shape[0]):
                records.append(
                    {
                        "sample_index": sample_offset + i,
                        "batch_index": batch_idx,
                        "band_index": band_idx,
                        "band_name": band_name,
                        "true_label": int(labels[i].item()),
                        "baseline_pred": int(base_pred[i].item()),
                        "baseline_confidence": float(base_conf[i].item()),
                        "target_class": int(target_class[i].item()),
                        "baseline_target_confidence": float(base_target_conf[i].item()),
                        "occluded_pred": int(occ_pred[i].item()),
                        "occluded_confidence": float(occ_conf[i].item()),
                        "occluded_target_confidence": float(occ_target_conf[i].item()),
                        "confidence_drop": float(confidence_drop[i].item()),
                        "prediction_changed": bool(prediction_changed[i].item()),
                        "metadata": _safe_metadata_value(batch.metadata, i),
                    }
                )

        sample_offset += images.shape[0]

    df = pd.DataFrame.from_records(records)

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

    return df


def summarize_band_occlusion(
    occlusion_df: pd.DataFrame,
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Aggregate per-sample band occlusion results into a band-importance table."""
    required = {"band_index", "band_name", "confidence_drop", "prediction_changed"}
    missing = required - set(occlusion_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    summary = (
        occlusion_df.groupby(["band_index", "band_name"], as_index=False)
        .agg(
            mean_confidence_drop=("confidence_drop", "mean"),
            median_confidence_drop=("confidence_drop", "median"),
            std_confidence_drop=("confidence_drop", "std"),
            prediction_change_rate=("prediction_changed", "mean"),
            n_samples=("confidence_drop", "size"),
        )
        .sort_values(["mean_confidence_drop", "prediction_change_rate"], ascending=False)
        .reset_index(drop=True)
    )
    summary.insert(0, "rank", np.arange(1, len(summary) + 1))

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(output_path, index=False)

    return summary
