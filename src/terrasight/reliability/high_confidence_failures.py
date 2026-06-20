"""
High-confidence failure analysis for TerraSight V5.

This module identifies cases where the model is confidently wrong. These are
important for assessment reporting because they show limitations, ambiguity,
and calibration risk beyond aggregate accuracy.

The module supports:
- collecting predictions from model + dataloader
- filtering high-confidence errors
- summarizing failure pairs
- exporting report-ready CSV files
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union

import pandas as pd
import torch
from torch import Tensor, nn

from terrasight.explainability.band_occlusion import unpack_batch, predict_probabilities


def _metadata_to_columns(metadata: Optional[Any], row_idx: int) -> Dict[str, Any]:
    if metadata is None:
        return {}

    if isinstance(metadata, Mapping):
        out: Dict[str, Any] = {}
        for key, value in metadata.items():
            try:
                if isinstance(value, Tensor):
                    out[f"meta_{key}"] = value[row_idx].item() if value.ndim > 0 else value.item()
                elif hasattr(value, "__len__") and not isinstance(value, str):
                    out[f"meta_{key}"] = value[row_idx]
                else:
                    out[f"meta_{key}"] = value
            except Exception:
                out[f"meta_{key}"] = str(value)
        return out

    try:
        return {"metadata": metadata[row_idx]}
    except Exception:
        return {"metadata": str(metadata)}


@torch.no_grad()
def collect_prediction_table(
    model: nn.Module,
    dataloader: Iterable[Any],
    class_names: Optional[Sequence[str]] = None,
    device: Optional[Union[str, torch.device]] = None,
    max_batches: Optional[int] = None,
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Collect prediction, confidence, entropy, and correctness for each sample."""
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

        probs = predict_probabilities(model, images)
        conf, pred = probs.max(dim=1)
        true_conf = probs[torch.arange(images.shape[0]), labels]
        entropy = -(probs.clamp_min(1e-12) * probs.clamp_min(1e-12).log()).sum(dim=1)

        top2 = torch.topk(probs, k=min(2, probs.shape[1]), dim=1)
        if probs.shape[1] >= 2:
            margin = top2.values[:, 0] - top2.values[:, 1]
        else:
            margin = torch.ones_like(conf)

        for i in range(images.shape[0]):
            true_id = int(labels[i].item())
            pred_id = int(pred[i].item())

            row: Dict[str, Any] = {
                "sample_index": sample_offset + i,
                "batch_index": batch_idx,
                "true_label": true_id,
                "pred_label": pred_id,
                "true_name": class_names[true_id] if class_names is not None else str(true_id),
                "pred_name": class_names[pred_id] if class_names is not None else str(pred_id),
                "confidence": float(conf[i].item()),
                "true_class_confidence": float(true_conf[i].item()),
                "confidence_margin": float(margin[i].item()),
                "predictive_entropy": float(entropy[i].item()),
                "correct": bool(pred_id == true_id),
            }
            row.update(_metadata_to_columns(batch.metadata, i))
            records.append(row)

        sample_offset += images.shape[0]

    df = pd.DataFrame.from_records(records)

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

    return df


def extract_high_confidence_failures(
    prediction_df: pd.DataFrame,
    min_confidence: float = 0.90,
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Filter the prediction table to high-confidence incorrect predictions."""
    required = {"confidence", "correct", "true_label", "pred_label"}
    missing = required - set(prediction_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    failures = prediction_df[
        (~prediction_df["correct"].astype(bool))
        & (prediction_df["confidence"].astype(float) >= float(min_confidence))
    ].copy()

    failures = failures.sort_values(
        ["confidence", "confidence_margin"],
        ascending=[False, False],
    ).reset_index(drop=True)

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        failures.to_csv(output_path, index=False)

    return failures


def summarize_failure_pairs(
    failures_df: pd.DataFrame,
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Summarize high-confidence failures by true -> predicted class pair."""
    true_col = "true_name" if "true_name" in failures_df.columns else "true_label"
    pred_col = "pred_name" if "pred_name" in failures_df.columns else "pred_label"

    if failures_df.empty:
        summary = pd.DataFrame(
            columns=[true_col, pred_col, "n_failures", "mean_confidence", "max_confidence"]
        )
    else:
        summary = (
            failures_df.groupby([true_col, pred_col], as_index=False)
            .agg(
                n_failures=("confidence", "size"),
                mean_confidence=("confidence", "mean"),
                max_confidence=("confidence", "max"),
                mean_margin=("confidence_margin", "mean"),
                mean_entropy=("predictive_entropy", "mean"),
            )
            .sort_values(["n_failures", "mean_confidence"], ascending=False)
            .reset_index(drop=True)
        )

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(output_path, index=False)

    return summary


def run_high_confidence_failure_analysis(
    model: nn.Module,
    dataloader: Iterable[Any],
    output_dir: Union[str, Path],
    class_names: Optional[Sequence[str]] = None,
    min_confidence: float = 0.90,
    device: Optional[Union[str, torch.device]] = None,
    max_batches: Optional[int] = None,
) -> Dict[str, pd.DataFrame]:
    """Run full high-confidence failure analysis and export CSV files."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    predictions = collect_prediction_table(
        model=model,
        dataloader=dataloader,
        class_names=class_names,
        device=device,
        max_batches=max_batches,
        output_csv=out / "prediction_table.csv",
    )
    failures = extract_high_confidence_failures(
        predictions,
        min_confidence=min_confidence,
        output_csv=out / f"high_confidence_failures_{min_confidence:.2f}.csv",
    )
    pairs = summarize_failure_pairs(
        failures,
        output_csv=out / f"high_confidence_failure_pairs_{min_confidence:.2f}.csv",
    )

    return {
        "predictions": predictions,
        "failures": failures,
        "failure_pairs": pairs,
    }
