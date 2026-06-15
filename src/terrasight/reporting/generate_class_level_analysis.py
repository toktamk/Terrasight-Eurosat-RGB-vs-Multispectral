from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

from terrasight.data.band_registry import EUROSAT_CLASSES


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PREDICTION_DIR = PROJECT_ROOT / "reports" / "tables" / "predictions"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "tables"


EXPERIMENTS = {
    "RGB": "v4_ablation_rgb_resnet18_pretrained_adapted_seed42_predictions.csv",
    "RGB+NIR": "v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42_predictions.csv",
    "RGB+RedEdge+NIR": "v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42_predictions.csv",
    "RGB+RedEdge+NIR+SWIR": "v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_predictions.csv",
    "PhysicalBands": "v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42_predictions.csv",
    "Full13NoB10": "v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42_predictions.csv",
    "Full13": "v4_ablation_full13_resnet18_pretrained_adapted_seed42_predictions.csv",
}


def load_predictions(model_name: str, filename: str) -> pd.DataFrame:
    path = PREDICTION_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing prediction file for {model_name}: {path}")

    df = pd.read_csv(path)

    required = {"true_label", "predicted_label", "true_class", "predicted_class"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"{path} missing columns: {missing}")

    return df


def compute_classwise_metrics(model_name: str, df: pd.DataFrame) -> pd.DataFrame:
    report = classification_report(
        df["true_label"],
        df["predicted_label"],
        labels=list(range(len(EUROSAT_CLASSES))),
        target_names=EUROSAT_CLASSES,
        output_dict=True,
        zero_division=0,
    )

    rows = []

    for class_name in EUROSAT_CLASSES:
        rows.append(
            {
                "model": model_name,
                "class": class_name,
                "precision": report[class_name]["precision"],
                "recall": report[class_name]["recall"],
                "f1": report[class_name]["f1-score"],
                "support": report[class_name]["support"],
            }
        )

    return pd.DataFrame(rows)


def compute_improvement_summary(classwise_df: pd.DataFrame) -> pd.DataFrame:
    pivot = classwise_df.pivot(
        index="class",
        columns="model",
        values="f1",
    ).reset_index()

    comparisons = {
        "nir_gain_vs_rgb": ("RGB+NIR", "RGB"),
        "rededge_gain_vs_rgb_nir": ("RGB+RedEdge+NIR", "RGB+NIR"),
        "swir_gain_vs_rgb_rededge_nir": (
            "RGB+RedEdge+NIR+SWIR",
            "RGB+RedEdge+NIR",
        ),
        "full13_gain_vs_best_selective": (
            "Full13",
            "RGB+RedEdge+NIR+SWIR",
        ),
        "full13_degradation_vs_best_selective": (
            "RGB+RedEdge+NIR+SWIR",
            "Full13",
        ),
    }

    for output_col, (better_model, baseline_model) in comparisons.items():
        if better_model in pivot.columns and baseline_model in pivot.columns:
            pivot[output_col] = pivot[better_model] - pivot[baseline_model]

    return pivot


def compute_confusion_pairs(model_name: str, df: pd.DataFrame) -> pd.DataFrame:
    cm = confusion_matrix(
        df["true_label"],
        df["predicted_label"],
        labels=list(range(len(EUROSAT_CLASSES))),
    )

    rows = []

    for true_idx, true_class in enumerate(EUROSAT_CLASSES):
        for pred_idx, pred_class in enumerate(EUROSAT_CLASSES):
            if true_idx == pred_idx:
                continue

            count = int(cm[true_idx, pred_idx])

            if count > 0:
                rows.append(
                    {
                        "model": model_name,
                        "true_class": true_class,
                        "predicted_class": pred_class,
                        "confusion_count": count,
                    }
                )

    return pd.DataFrame(rows)


def compare_confusion_pairs(confusion_df: pd.DataFrame) -> pd.DataFrame:
    pivot = confusion_df.pivot_table(
        index=["true_class", "predicted_class"],
        columns="model",
        values="confusion_count",
        fill_value=0,
        aggfunc="sum",
    ).reset_index()

    if "RGB" in pivot.columns and "RGB+RedEdge+NIR+SWIR" in pivot.columns:
        pivot["resolved_by_best_ms"] = (
            pivot["RGB"] - pivot["RGB+RedEdge+NIR+SWIR"]
        )

    if "RGB+RedEdge+NIR+SWIR" in pivot.columns and "Full13" in pivot.columns:
        pivot["full13_degradation"] = (
            pivot["Full13"] - pivot["RGB+RedEdge+NIR+SWIR"]
        )

    return pivot.sort_values(
        by=[c for c in ["resolved_by_best_ms", "full13_degradation"] if c in pivot.columns],
        ascending=False,
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    classwise_frames = []
    confusion_frames = []

    for model_name, filename in EXPERIMENTS.items():
        df = load_predictions(model_name, filename)

        classwise_frames.append(
            compute_classwise_metrics(model_name, df)
        )

        confusion_frames.append(
            compute_confusion_pairs(model_name, df)
        )

    classwise_df = pd.concat(classwise_frames, ignore_index=True)
    classwise_path = OUTPUT_DIR / "classwise_comparison.csv"
    classwise_df.to_csv(classwise_path, index=False)

    improvement_df = compute_improvement_summary(classwise_df)
    improvement_path = OUTPUT_DIR / "classwise_improvement_summary.csv"
    improvement_df.to_csv(improvement_path, index=False)

    confusion_df = pd.concat(confusion_frames, ignore_index=True)
    confusion_summary = compare_confusion_pairs(confusion_df)
    confusion_path = OUTPUT_DIR / "confusion_pair_analysis.csv"
    confusion_summary.to_csv(confusion_path, index=False)

    print(f"Saved: {classwise_path}")
    print(f"Saved: {improvement_path}")
    print(f"Saved: {confusion_path}")

    print("\nClasses improved by NIR:")
    print(
        improvement_df.loc[
            improvement_df["nir_gain_vs_rgb"] > 0,
            ["class", "nir_gain_vs_rgb"],
        ].sort_values("nir_gain_vs_rgb", ascending=False)
    )

    print("\nClasses improved by RedEdge:")
    print(
        improvement_df.loc[
            improvement_df["rededge_gain_vs_rgb_nir"] > 0,
            ["class", "rededge_gain_vs_rgb_nir"],
        ].sort_values("rededge_gain_vs_rgb_nir", ascending=False)
    )

    print("\nClasses improved by SWIR:")
    print(
        improvement_df.loc[
            improvement_df["swir_gain_vs_rgb_rededge_nir"] > 0,
            ["class", "swir_gain_vs_rgb_rededge_nir"],
        ].sort_values("swir_gain_vs_rgb_rededge_nir", ascending=False)
    )

    print("\nClasses degraded with Full13 compared with best selective multispectral:")
    print(
        improvement_df.loc[
            improvement_df["full13_gain_vs_best_selective"] < 0,
            ["class", "full13_gain_vs_best_selective"],
        ].sort_values("full13_gain_vs_best_selective")
    )


if __name__ == "__main__":
    main()