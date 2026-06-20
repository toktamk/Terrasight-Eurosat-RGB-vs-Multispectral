from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

REQUIRED_COLUMNS = {"path", "true_label", "rgb_pred", "ms_pred"}

def load_predictions(rgb_csv: Path, ms_csv: Path) -> pd.DataFrame:
    rgb = pd.read_csv(rgb_csv)
    ms = pd.read_csv(ms_csv)
    if "path" in rgb.columns and "path" in ms.columns:
        return rgb.merge(ms, on=["path", "true_label"], suffixes=("_rgb", "_ms"))
    rgb = rgb.reset_index().rename(columns={"prediction": "rgb_pred"})
    ms = ms.reset_index().rename(columns={"prediction": "ms_pred"})
    return rgb.merge(ms, on="index", suffixes=("_rgb", "_ms"))

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename = {}
    for col in df.columns:
        low = col.lower()
        if low in {"y_true", "label", "true", "true_label_rgb"}:
            rename[col] = "true_label"
        if low in {"y_pred_rgb", "prediction_rgb", "pred_rgb"}:
            rename[col] = "rgb_pred"
        if low in {"y_pred_ms", "prediction_ms", "pred_ms"}:
            rename[col] = "ms_pred"
    df = df.rename(columns=rename)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns after normalization: {sorted(missing)}")
    return df

def select_cases(df: pd.DataFrame, max_examples: int) -> pd.DataFrame:
    cases = df[(df["rgb_pred"] != df["true_label"]) & (df["ms_pred"] == df["true_label"])].copy()
    if "ms_confidence" in cases.columns:
        cases = cases.sort_values("ms_confidence", ascending=False)
    return cases.head(max_examples)

def save_gallery(cases: pd.DataFrame, output_png: Path) -> None:
    n = len(cases)
    if n == 0:
        raise RuntimeError("No RGB-failure / multispectral-success cases found.")
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    axes = [axes] if n == 1 else axes.flatten()
    for ax, (_, row) in zip(axes, cases.iterrows()):
        img = Image.open(row["path"]).convert("RGB")
        ax.imshow(img)
        ax.set_title(f"True: {row['true_label']}\nRGB: {row['rgb_pred']} | MS: {row['ms_pred']}", fontsize=9)
        ax.axis("off")
    for ax in axes[n:]:
        ax.axis("off")
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_png, dpi=300)
    plt.close(fig)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate RGB-failure / multispectral-success case-study gallery.")
    parser.add_argument("--rgb-predictions", required=True)
    parser.add_argument("--ms-predictions", required=True)
    parser.add_argument("--output-csv", default="reports/tables/case_studies/rgb_failure_ms_success.csv")
    parser.add_argument("--output-png", default="reports/figures/case_studies/rgb_failure_ms_success.png")
    parser.add_argument("--max-examples", type=int, default=12)
    args = parser.parse_args()

    df = load_predictions(Path(args.rgb_predictions), Path(args.ms_predictions))
    df = normalize_columns(df)
    cases = select_cases(df, args.max_examples)
    out_csv = Path(args.output_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    cases.to_csv(out_csv, index=False)
    save_gallery(cases, Path(args.output_png))
    print(f"Saved table: {out_csv}")
    print(f"Saved gallery: {args.output_png}")

if __name__ == "__main__":
    main()
