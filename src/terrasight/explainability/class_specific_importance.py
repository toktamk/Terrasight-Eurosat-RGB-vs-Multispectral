"""
Class-specific spectral importance analysis for TerraSight V5.

This module converts per-sample band-occlusion outputs into class-level
importance tables. It is useful for statements such as:

- NIR is most important for vegetation classes.
- SWIR contributes to built-up or water-related classes.
- RedEdge is most useful for crop-related confusions.

Input can be either:
1. a DataFrame returned by run_band_occlusion/run_spectral_attribution, or
2. a CSV path to that detail table.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Mapping, Optional, Sequence, Union

import numpy as np
import pandas as pd


def _load_details(details: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
    if isinstance(details, pd.DataFrame):
        return details.copy()
    return pd.read_csv(details)


def compute_class_specific_band_importance(
    details: Union[str, Path, pd.DataFrame],
    class_names: Optional[Sequence[str]] = None,
    class_column: str = "true_label",
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Aggregate band attribution by class.

    Parameters
    ----------
    details:
        Detail table from spectral attribution / band occlusion.
    class_names:
        Optional label names indexed by integer class ID.
    class_column:
        Usually "true_label". Use "baseline_pred" to analyze model-predicted
        class groups instead.
    output_csv:
        Optional output path.

    Returns
    -------
    DataFrame
        Per-class, per-band importance summary.
    """
    df = _load_details(details)
    required = {class_column, "band_index", "band_name", "confidence_drop", "prediction_changed"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = (
        df.groupby([class_column, "band_index", "band_name"], as_index=False)
        .agg(
            mean_confidence_drop=("confidence_drop", "mean"),
            median_confidence_drop=("confidence_drop", "median"),
            std_confidence_drop=("confidence_drop", "std"),
            positive_support_rate=("confidence_drop", lambda x: float((x > 0).mean())),
            prediction_change_rate=("prediction_changed", "mean"),
            n_samples=("confidence_drop", "size"),
        )
        .sort_values([class_column, "mean_confidence_drop"], ascending=[True, False])
        .reset_index(drop=True)
    )

    result["class_rank"] = (
        result.groupby(class_column)["mean_confidence_drop"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    if class_names is not None:
        result["class_name"] = result[class_column].apply(
            lambda idx: class_names[int(idx)] if 0 <= int(idx) < len(class_names) else str(idx)
        )
        ordered_cols = ["class_name", class_column, "class_rank"]
        result = result[ordered_cols + [c for c in result.columns if c not in ordered_cols]]

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(output_path, index=False)

    return result


def top_bands_per_class(
    class_importance: pd.DataFrame,
    top_k: int = 3,
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Return the top-k bands for each class."""
    class_label_col = "class_name" if "class_name" in class_importance.columns else "true_label"
    top = (
        class_importance[class_importance["class_rank"] <= top_k]
        .sort_values([class_label_col, "class_rank"])
        .reset_index(drop=True)
    )

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        top.to_csv(output_path, index=False)

    return top


def class_band_importance_matrix(
    class_importance: pd.DataFrame,
    value_column: str = "mean_confidence_drop",
    output_csv: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Create a class x band matrix for heatmap plotting."""
    class_label_col = "class_name" if "class_name" in class_importance.columns else "true_label"

    matrix = class_importance.pivot_table(
        index=class_label_col,
        columns="band_name",
        values=value_column,
        aggfunc="mean",
    )

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        matrix.to_csv(output_path)

    return matrix


def summarize_class_specific_importance(
    details: Union[str, Path, pd.DataFrame],
    output_dir: Union[str, Path],
    class_names: Optional[Sequence[str]] = None,
    top_k: int = 3,
) -> Dict[str, pd.DataFrame]:
    """Generate all class-specific band-importance outputs."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    class_importance = compute_class_specific_band_importance(
        details=details,
        class_names=class_names,
        output_csv=out / "class_specific_band_importance.csv",
    )
    top = top_bands_per_class(
        class_importance,
        top_k=top_k,
        output_csv=out / f"top_{top_k}_bands_per_class.csv",
    )
    matrix = class_band_importance_matrix(
        class_importance,
        output_csv=out / "class_band_importance_matrix.csv",
    )

    return {
        "class_importance": class_importance,
        "top_bands": top,
        "matrix": matrix,
    }
