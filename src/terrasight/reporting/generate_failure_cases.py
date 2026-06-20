from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from terrasight.reliability.high_confidence_failures import extract_high_confidence_failures

def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_image(path: str):
    p = Path(path)

    if not p.exists():
        return None

    try:
        if p.suffix.lower() in [".tif", ".tiff"]:
            import tifffile
            import numpy as np

            arr = tifffile.imread(p)

            if arr.ndim == 3:
                if arr.shape[0] == 13:
                    arr = np.transpose(arr, (1, 2, 0))

                if arr.shape[-1] >= 4:
                    # EuroSAT MS common order:
                    # B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B10,B11,B12
                    rgb = arr[:, :, [3, 2, 1]]
                else:
                    rgb = arr[:, :, :3]

                rgb = rgb.astype("float32")
                low, high = np.percentile(rgb, [2, 98])
                rgb = np.clip((rgb - low) / (high - low + 1e-8), 0, 1)

                return rgb

        return Image.open(p).convert("RGB")

    except Exception as error:
        print(f"Could not load image: {p} ({error})")
        return None

def create_failure_grid(df: pd.DataFrame, output_path: Path, max_examples: int = 16, min_confidence: float = 0.90,) -> None:
    #failures = df[df["correct"] == 0].sort_values("confidence", ascending=False).head(max_examples)
    # ensure compatibility with failure module
    if "confidence_margin" not in df.columns:
        df["confidence_margin"] = 0.0
    failures = extract_high_confidence_failures(
        prediction_df=df,
        min_confidence=min_confidence,
    ).head(max_examples)

    if failures.empty:
        print("No failures found.")
        return

    n = len(failures)
    cols = 4
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes = axes.flatten()

    for ax in axes:
        ax.axis("off")

    for ax, (_, row) in zip(axes, failures.iterrows()):
        img = load_image(row["path"])

        if img is not None:
            ax.imshow(img)

        ax.set_title(
            f"True: {row['true_name']}\nPred: {row['pred_name']}\nConf: {row['confidence']:.2f}",
            fontsize=9,
        )
        ax.axis("off")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probabilities", required=True)
    parser.add_argument("--output-dir", default="reports/figures/failure_cases")
    parser.add_argument("--max-examples", type=int, default=16)
    args = parser.parse_args()

    project_root = get_project_root()
    input_path = project_root / args.probabilities
    output_dir = project_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    df = df.rename(
        columns={
            "predicted_label": "pred_label",
            "true_class": "true_name",
            "predicted_class": "pred_name",
        }
    )

    if "confidence_margin" not in df.columns:
        df["confidence_margin"] = 0.0



    model_name = input_path.stem.replace("_probabilities", "")

    output_path = output_dir / f"{model_name}_high_confidence_failure_cases.png"

    create_failure_grid(df, output_path, max_examples=args.max_examples)

    failure_csv = output_dir / f"{model_name}_high_confidence_failures.csv"
    df[df["correct"] == 0].sort_values("confidence", ascending=False).to_csv(failure_csv,index=False )
    failures = extract_high_confidence_failures(
        prediction_df=df,
        min_confidence=0.90,
    )

    failures.to_csv(
        failure_csv,
        index=False,
    )
    print(f"Saved: {output_path}")
    print(f"Saved: {failure_csv}")


if __name__ == "__main__":
    main()