from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def load_registry() -> pd.DataFrame:
    registry_path = PROJECT_ROOT / "experiments" / "registry.csv"

    if not registry_path.exists():
        registry_path = PROJECT_ROOT / "registry.csv"

    if not registry_path.exists():
        raise FileNotFoundError("registry.csv not found")

    return pd.read_csv(registry_path)


def create_v1_comparison(df: pd.DataFrame, output_dir: Path) -> None:
    models = {
        "RGB Pretrained":
            "v1_rgb_resnet18_seed42",
        "RGB Scratch":
            "v1_rgb_resnet18_scratch_seed42",
        "MS Scratch":
            "v1_multispectral_resnet18_scratch_seed42",
        "MS Adapted":
            "v1_multispectral_resnet18_adapted_seed42",
    }

    rows = []

    for display_name, experiment_id in models.items():
        row = df[df["experiment_id"] == experiment_id]

        if row.empty:
            continue

        rows.append(
            {
                "Model": display_name,
                "Macro-F1": float(row.iloc[0]["macro_f1"]),
            }
        )

    plot_df = pd.DataFrame(rows)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(plot_df["Model"], plot_df["Macro-F1"])

    plt.ylabel("Macro-F1")
    plt.title("RGB vs Multispectral Comparison")
    plt.ylim(
        plot_df["Macro-F1"].min() - 0.01,
        plot_df["Macro-F1"].max() + 0.01,
    )

    for bar in bars:
        value = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:.4f}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig(
        output_dir / "v1_model_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def create_v4_ablation(df: pd.DataFrame, output_dir: Path) -> None:
    models = {
        "RGB":
            "v4_ablation_rgb_resnet18_pretrained_adapted_seed42",
        "RGB and NIR":
            "v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42",
        "RGB, RE and NIR":
            "v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42",
        "RGB, RE, NIR and SWIR":
            "v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42",
        "Physical bands":
            "v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42",
        "Full 13 spectral bands excluding B10":
            "v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42",
        "Full 13 spectral bands":
            "v4_ablation_full13_resnet18_pretrained_adapted_seed42",
    }

    rows = []

    for display_name, experiment_id in models.items():
        row = df[df["experiment_id"] == experiment_id]

        if row.empty:
            continue

        rows.append(
            {
                "Model": display_name,
                "Macro-F1": float(row.iloc[0]["macro_f1"]),
            }
        )

    plot_df = pd.DataFrame(rows)

    plot_df = plot_df.sort_values(
        "Macro-F1",
        ascending=True,
    )

    plt.figure(figsize=(10, 6))

    bars = plt.barh(
        plot_df["Model"],
        plot_df["Macro-F1"],
    )
    plt.xlim(
        plot_df["Macro-F1"].min() - 0.01,
        plot_df["Macro-F1"].max() + 0.01,
    )

    plt.xlabel("Macro-F1")
    plt.title("V4 Band Ablation Study")

    for bar in bars:
        value = bar.get_width()
        plt.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.4f}",
            va="center",
        )

    plt.tight_layout()

    plt.savefig(
        output_dir / "v4_band_ablation_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def main() -> None:
    output_dir = PROJECT_ROOT / "reports" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_registry()

    create_v1_comparison(df, output_dir)
    create_v4_ablation(df, output_dir)

    print("Saved:")
    print(output_dir / "v1_model_comparison.png")
    print(output_dir / "v4_band_ablation_comparison.png")


if __name__ == "__main__":
    main()