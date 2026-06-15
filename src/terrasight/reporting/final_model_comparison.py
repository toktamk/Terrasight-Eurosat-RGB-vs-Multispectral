from __future__ import annotations

from pathlib import Path

import pandas as pd


EXPERIMENT_ORDER = [
    "v1_rgb_resnet18_seed42",
    "v1_rgb_resnet18_scratch_seed42",
    "v1_multispectral_resnet18_scratch_seed42",
    "v1_multispectral_resnet18_adapted_seed42",
    "v4_ablation_rgb_resnet18_pretrained_adapted_seed42",
    "v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42",
    "v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42",
    "v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42",
    "v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42",
    "v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42",
    "v4_ablation_full13_resnet18_pretrained_adapted_seed42",
]


BANDSET_NAMES = {
    "v1_rgb_resnet18_seed42": "RGB pretrained",
    "v1_rgb_resnet18_scratch_seed42": "RGB scratch",
    "v1_multispectral_resnet18_scratch_seed42": "Multispectral scratch",
    "v1_multispectral_resnet18_adapted_seed42": "Multispectral pretrained adapted",
    "v4_ablation_rgb_resnet18_pretrained_adapted_seed42": "RGB ablation",
    "v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42": "RGB + NIR",
    "v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42": "RGB + RedEdge + NIR",
    "v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42": "RGB + RedEdge + NIR + SWIR",
    "v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42": "Physical Bands",
    "v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42": "Full13 no B10",
    "v4_ablation_full13_resnet18_pretrained_adapted_seed42": "Full13",
}


def main() -> None:
    registry_path = Path("././experiments/registry.csv")

    if not registry_path.exists():
        raise FileNotFoundError(registry_path)

    df = pd.read_csv(registry_path)

    experiment_column = None

    for candidate in [
        "experiment_id",
        "id",
        "experiment",
    ]:
        if candidate in df.columns:
            experiment_column = candidate
            break

    if experiment_column is None:
        raise ValueError(
            "Could not find experiment identifier column in registry.csv"
        )

    df = df[df[experiment_column].isin(EXPERIMENT_ORDER)].copy()

    df["Band Set"] = df[experiment_column].map(BANDSET_NAMES)

    desired_columns = [
        experiment_column,
        "Band Set",
        "input_channels",
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
        "loss",
        "epoch",
    ]

    available_columns = [
        c for c in desired_columns if c in df.columns
    ]

    output = df[available_columns].copy()

    output = output.rename(
        columns={
            experiment_column: "Experiment ID",
            "input_channels": "Number of Channels",
            "accuracy": "Accuracy",
            "macro_f1": "Macro-F1",
            "weighted_f1": "Weighted-F1",
            "balanced_accuracy": "Balanced Accuracy",
            "loss": "Loss",
            "epoch": "Best Epoch",
        }
    )

    output["sort_order"] = output["Experiment ID"].apply(
        lambda x: EXPERIMENT_ORDER.index(x)
    )

    output = output.sort_values("sort_order")
    output = output.drop(columns="sort_order")

    output_dir = Path("reports/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "final_model_comparison.csv"

    output.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()