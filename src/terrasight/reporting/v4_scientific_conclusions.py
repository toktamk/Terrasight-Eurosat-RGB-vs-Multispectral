from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

TABLE_DIR = PROJECT_ROOT / "reports" / "tables"

FINAL_MODEL_COMPARISON = TABLE_DIR / "final_model_comparison.csv"
CLASSWISE_COMPARISON = TABLE_DIR / "classwise_comparison.csv"
CONFUSION_PAIR_ANALYSIS = TABLE_DIR / "confusion_pair_analysis.csv"

OUTPUT_CSV = TABLE_DIR / "v4_band_effects.csv"
OUTPUT_MD = TABLE_DIR / "v4_scientific_conclusions.md"


MODEL_ALIASES = {
    "RGB": ["RGB", "RGB ablation", "v4_ablation_rgb_resnet18_pretrained_adapted_seed42"],
    "RGB+NIR": ["RGB+NIR", "RGB + NIR", "v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42"],
    "RGB+RedEdge+NIR": [
        "RGB+RedEdge+NIR",
        "RGB + RedEdge + NIR",
        "v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42",
    ],
    "RGB+RedEdge+NIR+SWIR": [
        "RGB+RedEdge+NIR+SWIR",
        "RGB + RedEdge + NIR + SWIR",
        "v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42",
    ],
    "PhysicalBands": [
        "PhysicalBands",
        "Physical Bands",
        "v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42",
    ],
    "Full13NoB10": [
        "Full13NoB10",
        "Full13 no B10",
        "Full13 No B10",
        "v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42",
    ],
    "Full13": [
        "Full13",
        "Full 13",
        "v4_ablation_full13_resnet18_pretrained_adapted_seed42",
    ],
}


VEGETATION_CLASSES = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Pasture",
    "PermanentCrop",
]

CROP_CLASSES = [
    "AnnualCrop",
    "HerbaceousVegetation",
    "PermanentCrop",
]

URBAN_WATER_CLASSES = [
    "Highway",
    "Industrial",
    "Residential",
    "River",
    "SeaLake",
]

IMPORTANT_CONFUSION_PAIRS = [
    ("AnnualCrop", "PermanentCrop"),
    ("PermanentCrop", "AnnualCrop"),
    ("HerbaceousVegetation", "PermanentCrop"),
    ("PermanentCrop", "HerbaceousVegetation"),
    ("River", "Highway"),
    ("Highway", "River"),
    ("Industrial", "Residential"),
    ("Residential", "Industrial"),
]


def canonical_model_name(value: str) -> str:
    value = str(value).strip()

    for canonical, aliases in MODEL_ALIASES.items():
        if value in aliases:
            return canonical

    return value


def find_column(df: pd.DataFrame, candidates: list[str]) -> str:
    lower_map = {c.lower().strip(): c for c in df.columns}

    for candidate in candidates:
        key = candidate.lower().strip()
        if key in lower_map:
            return lower_map[key]

    raise ValueError(f"Could not find any of these columns: {candidates}")


def load_final_model_comparison() -> pd.DataFrame:
    if not FINAL_MODEL_COMPARISON.exists():
        raise FileNotFoundError(FINAL_MODEL_COMPARISON)

    df = pd.read_csv(FINAL_MODEL_COMPARISON)

    model_col = find_column(
        df,
        [
            "Band Set",
            "model",
            "Model",
            "Experiment ID",
            "experiment_id",
        ],
    )

    macro_f1_col = find_column(
        df,
        [
            "Macro-F1",
            "macro_f1",
            "Macro F1",
        ],
    )

    accuracy_col = find_column(
        df,
        [
            "Accuracy",
            "accuracy",
        ],
    )

    out = df.copy()
    out["canonical_model"] = out[model_col].apply(canonical_model_name)
    out["macro_f1_value"] = out[macro_f1_col].astype(float)
    out["accuracy_value"] = out[accuracy_col].astype(float)

    return out


def load_classwise_comparison() -> pd.DataFrame:
    if not CLASSWISE_COMPARISON.exists():
        raise FileNotFoundError(CLASSWISE_COMPARISON)

    df = pd.read_csv(CLASSWISE_COMPARISON)

    model_col = find_column(df, ["model", "Model"])
    class_col = find_column(df, ["class", "Class"])
    f1_col = find_column(df, ["f1", "F1", "f1-score", "F1 Score"])
    precision_col = find_column(df, ["precision", "Precision"])
    recall_col = find_column(df, ["recall", "Recall"])

    out = df.copy()
    out["canonical_model"] = out[model_col].apply(canonical_model_name)
    out["class_name"] = out[class_col].astype(str)
    out["f1_value"] = out[f1_col].astype(float)
    out["precision_value"] = out[precision_col].astype(float)
    out["recall_value"] = out[recall_col].astype(float)

    return out


def load_confusion_pair_analysis() -> pd.DataFrame | None:
    if not CONFUSION_PAIR_ANALYSIS.exists():
        return None

    df = pd.read_csv(CONFUSION_PAIR_ANALYSIS)

    if "true_class" not in df.columns or "predicted_class" not in df.columns:
        return None

    rename_map = {}
    for col in df.columns:
        canonical = canonical_model_name(col)
        if canonical != col:
            rename_map[col] = canonical

    return df.rename(columns=rename_map)


def metric_for_model(final_df: pd.DataFrame, model: str, metric: str) -> float:
    row = final_df[final_df["canonical_model"] == model]

    if row.empty:
        raise ValueError(f"Missing model in final comparison table: {model}")

    if metric == "macro_f1":
        return float(row.iloc[0]["macro_f1_value"])

    if metric == "accuracy":
        return float(row.iloc[0]["accuracy_value"])

    raise ValueError(metric)


def class_f1(classwise_df: pd.DataFrame, model: str, class_name: str) -> float:
    row = classwise_df[
        (classwise_df["canonical_model"] == model)
        & (classwise_df["class_name"] == class_name)
    ]

    if row.empty:
        raise ValueError(f"Missing {model} / {class_name} in classwise table")

    return float(row.iloc[0]["f1_value"])


def mean_class_gain(
    classwise_df: pd.DataFrame,
    before_model: str,
    after_model: str,
    classes: list[str],
) -> tuple[float, pd.DataFrame]:
    rows = []

    for class_name in classes:
        before_f1 = class_f1(classwise_df, before_model, class_name)
        after_f1 = class_f1(classwise_df, after_model, class_name)

        rows.append(
            {
                "class": class_name,
                "before_model": before_model,
                "after_model": after_model,
                "before_f1": before_f1,
                "after_f1": after_f1,
                "gain": after_f1 - before_f1,
            }
        )

    gain_df = pd.DataFrame(rows)
    return float(gain_df["gain"].mean()), gain_df


def confusion_value(
    confusion_df: pd.DataFrame | None,
    true_class: str,
    predicted_class: str,
    model: str,
) -> int | None:
    if confusion_df is None:
        return None

    if model not in confusion_df.columns:
        return None

    row = confusion_df[
        (confusion_df["true_class"] == true_class)
        & (confusion_df["predicted_class"] == predicted_class)
    ]

    if row.empty:
        return 0

    return int(row.iloc[0][model])


def confusion_delta_summary(
    confusion_df: pd.DataFrame | None,
    before_model: str,
    after_model: str,
    pairs: list[tuple[str, str]],
) -> pd.DataFrame:
    rows = []

    for true_class, predicted_class in pairs:
        before_count = confusion_value(
            confusion_df,
            true_class=true_class,
            predicted_class=predicted_class,
            model=before_model,
        )

        after_count = confusion_value(
            confusion_df,
            true_class=true_class,
            predicted_class=predicted_class,
            model=after_model,
        )

        if before_count is None or after_count is None:
            continue

        rows.append(
            {
                "true_class": true_class,
                "predicted_class": predicted_class,
                "before_model": before_model,
                "after_model": after_model,
                "before_errors": before_count,
                "after_errors": after_count,
                "error_reduction": before_count - after_count,
            }
        )

    return pd.DataFrame(rows)


def conclusion_from_gain(gain: float, positive: str, marginal: str, negative: str) -> str:
    if gain >= 0.005:
        return positive

    if gain > 0:
        return marginal

    return negative


def generate_band_effects(
    final_df: pd.DataFrame,
    classwise_df: pd.DataFrame,
    confusion_df: pd.DataFrame | None,
) -> pd.DataFrame:
    effects = []

    nir_gain, nir_df = mean_class_gain(
        classwise_df,
        before_model="RGB",
        after_model="RGB+NIR",
        classes=VEGETATION_CLASSES,
    )

    rededge_gain, rededge_df = mean_class_gain(
        classwise_df,
        before_model="RGB+NIR",
        after_model="RGB+RedEdge+NIR",
        classes=CROP_CLASSES,
    )

    swir_gain, swir_df = mean_class_gain(
        classwise_df,
        before_model="RGB+RedEdge+NIR",
        after_model="RGB+RedEdge+NIR+SWIR",
        classes=URBAN_WATER_CLASSES,
    )

    b10_gain = (
        metric_for_model(final_df, "Full13NoB10", "macro_f1")
        - metric_for_model(final_df, "Full13", "macro_f1")
    )

    atmospheric_gain = (
        metric_for_model(final_df, "PhysicalBands", "macro_f1")
        - metric_for_model(final_df, "Full13", "macro_f1")
    )

    effects.append(
        {
            "question": "Does NIR help vegetation classes?",
            "comparison": "RGB+NIR minus RGB",
            "target_classes": ", ".join(VEGETATION_CLASSES),
            "mean_f1_gain": nir_gain,
            "conclusion": conclusion_from_gain(
                nir_gain,
                "Yes. NIR improves vegetation-class F1 on average.",
                "NIR provides a small positive vegetation-class gain.",
                "No. The current evidence does not show vegetation improvement from NIR alone.",
            ),
        }
    )

    effects.append(
        {
            "question": "Does RedEdge improve crop discrimination?",
            "comparison": "RGB+RedEdge+NIR minus RGB+NIR",
            "target_classes": ", ".join(CROP_CLASSES),
            "mean_f1_gain": rededge_gain,
            "conclusion": conclusion_from_gain(
                rededge_gain,
                "Yes. RedEdge improves crop-related class discrimination.",
                "RedEdge provides a small positive crop-discrimination gain.",
                "No. RedEdge does not improve crop discrimination in this run.",
            ),
        }
    )

    effects.append(
        {
            "question": "Does SWIR improve urban/water separation?",
            "comparison": "RGB+RedEdge+NIR+SWIR minus RGB+RedEdge+NIR",
            "target_classes": ", ".join(URBAN_WATER_CLASSES),
            "mean_f1_gain": swir_gain,
            "conclusion": conclusion_from_gain(
                swir_gain,
                "Yes. SWIR improves urban/water-related class separation.",
                "SWIR provides a small positive gain for urban/water-related classes.",
                "No. SWIR does not improve urban/water-related classes in this run.",
            ),
        }
    )

    effects.append(
        {
            "question": "Does removing B10 help?",
            "comparison": "Full13NoB10 minus Full13",
            "target_classes": "All classes",
            "mean_f1_gain": b10_gain,
            "conclusion": conclusion_from_gain(
                b10_gain,
                "Yes. Removing B10 improves Macro-F1.",
                "Removing B10 gives a small positive Macro-F1 gain.",
                "No. Removing B10 does not improve Macro-F1 in this run.",
            ),
        }
    )

    effects.append(
        {
            "question": "Do atmospheric bands reduce performance?",
            "comparison": "PhysicalBands minus Full13",
            "target_classes": "All classes",
            "mean_f1_gain": atmospheric_gain,
            "conclusion": conclusion_from_gain(
                atmospheric_gain,
                "Yes. Surface-focused physical bands outperform Full13, suggesting atmospheric bands reduce performance.",
                "Physical bands slightly outperform Full13, suggesting limited value from atmospheric bands.",
                "No. The current evidence does not show atmospheric-band degradation.",
            ),
        }
    )

    effect_df = pd.DataFrame(effects)

    detailed_frames = []

    for label, df in [
        ("NIR vegetation effect", nir_df),
        ("RedEdge crop effect", rededge_df),
        ("SWIR urban/water effect", swir_df),
    ]:
        temp = df.copy()
        temp.insert(0, "analysis", label)
        detailed_frames.append(temp)

    detailed_df = pd.concat(detailed_frames, ignore_index=True)

    detail_path = TABLE_DIR / "v4_class_level_band_effects.csv"
    detailed_df.to_csv(detail_path, index=False)

    confusion_summaries = []

    for before, after, label in [
        ("RGB", "RGB+NIR", "NIR confusion change"),
        ("RGB+NIR", "RGB+RedEdge+NIR", "RedEdge confusion change"),
        ("RGB+RedEdge+NIR", "RGB+RedEdge+NIR+SWIR", "SWIR confusion change"),
        ("Full13", "Full13NoB10", "B10 removal confusion change"),
        ("Full13", "PhysicalBands", "Atmospheric-band confusion change"),
    ]:
        temp = confusion_delta_summary(
            confusion_df=confusion_df,
            before_model=before,
            after_model=after,
            pairs=IMPORTANT_CONFUSION_PAIRS,
        )

        if not temp.empty:
            temp.insert(0, "analysis", label)
            confusion_summaries.append(temp)

    if confusion_summaries:
        confusion_out = pd.concat(confusion_summaries, ignore_index=True)
        confusion_out.to_csv(TABLE_DIR / "v4_confusion_change_summary.csv", index=False)

    return effect_df


def markdown_table(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False, floatfmt=".4f")


def generate_markdown_report(effect_df: pd.DataFrame, final_df: pd.DataFrame) -> str:
    model_rows = []

    for model in [
        "RGB",
        "RGB+NIR",
        "RGB+RedEdge+NIR",
        "RGB+RedEdge+NIR+SWIR",
        "PhysicalBands",
        "Full13NoB10",
        "Full13",
    ]:
        model_rows.append(
            {
                "Model": model,
                "Accuracy": metric_for_model(final_df, model, "accuracy"),
                "Macro-F1": metric_for_model(final_df, model, "macro_f1"),
            }
        )

    model_table = pd.DataFrame(model_rows)

    lines = []
    lines.append("# V4 Band-Ablation Scientific Conclusions")
    lines.append("")
    lines.append("## Overall V4 model comparison")
    lines.append("")
    lines.append(markdown_table(model_table))
    lines.append("")
    lines.append("## Scientific questions")
    lines.append("")
    lines.append(markdown_table(effect_df))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")

    for _, row in effect_df.iterrows():
        lines.append(f"### {row['question']}")
        lines.append("")
        lines.append(f"**Comparison:** {row['comparison']}")
        lines.append("")
        lines.append(f"**Target classes:** {row['target_classes']}")
        lines.append("")
        lines.append(f"**Mean F1 gain:** {row['mean_f1_gain']:.4f}")
        lines.append("")
        lines.append(f"**Conclusion:** {row['conclusion']}")
        lines.append("")

    lines.append("## Main scientific conclusion")
    lines.append("")
    lines.append(
        "The V4 ablation results should be interpreted as a controlled spectral-input study. "
        "The key question is not whether adding more bands always improves performance, "
        "but whether physically meaningful bands improve class separability. "
        "If selected multispectral subsets outperform Full13, the defensible conclusion is that "
        "spectral selection is more important than simply maximizing the number of input channels."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    final_df = load_final_model_comparison()
    classwise_df = load_classwise_comparison()
    confusion_df = load_confusion_pair_analysis()

    effect_df = generate_band_effects(
        final_df=final_df,
        classwise_df=classwise_df,
        confusion_df=confusion_df,
    )

    effect_df.to_csv(OUTPUT_CSV, index=False)

    markdown_report = generate_markdown_report(effect_df, final_df)
    OUTPUT_MD.write_text(markdown_report, encoding="utf-8")

    print(f"Saved: {OUTPUT_CSV}")
    print(f"Saved: {OUTPUT_MD}")
    print(f"Saved: {TABLE_DIR / 'v4_class_level_band_effects.csv'}")

    if (TABLE_DIR / "v4_confusion_change_summary.csv").exists():
        print(f"Saved: {TABLE_DIR / 'v4_confusion_change_summary.csv'}")

    print("\nScientific conclusions:")
    for _, row in effect_df.iterrows():
        print(f"- {row['question']} {row['conclusion']} Gain={row['mean_f1_gain']:.4f}")


if __name__ == "__main__":
    main()