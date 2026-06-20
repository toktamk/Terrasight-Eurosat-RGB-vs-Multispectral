from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score
from torch.utils.data import DataLoader

from terrasight.reporting.generate_confusion_matrices import (
    build_dataset,
    build_model,
    find_checkpoint,
    get_device,
    get_project_root,
    load_checkpoint_into_model,
)
from terrasight.utils.config import load_config
from terrasight.reliability.robustness_testing import run_robustness_suite



def plot_robustness(df: pd.DataFrame, output_path: Path, title: str) -> None:
    plot_df = df[df["perturbation"] != "clean"].copy()

    if plot_df.empty:
        return

    plot_df["label"] = plot_df.apply(
        lambda row: row["band"] if row["perturbation"] == "band_dropout" else row["perturbation"],
        axis=1,
    )
    plot_df["label"] = plot_df["perturbation"].str.replace("dropout_", "", regex=False)
    plot_df = plot_df.sort_values("macro_f1_drop", ascending=True)

    plt.figure(figsize=(10, max(5, 0.35 * len(plot_df))))
    bars = plt.barh(plot_df["label"], plot_df["macro_f1_drop"])

    plt.xlabel("Macro-F1 drop")
    plt.title(title)

    for bar in bars:
        value = bar.get_width()
        plt.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.4f}",
            va="center",
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def process_run(
    run_dir: Path,
    project_root: Path,
    output_table_dir: Path,
    output_figure_dir: Path,
) -> pd.DataFrame:
    config_path = run_dir / "config.yaml"
    checkpoint_path = find_checkpoint(run_dir)

    if not config_path.exists():
        raise FileNotFoundError(config_path)

    if checkpoint_path is None:
        raise FileNotFoundError(f"No checkpoint found in {run_dir}")

    config = load_config(config_path)
    experiment_id = config["experiment"]["id"]

    dataset = build_dataset(config, project_root)
    dataloader = DataLoader(
        dataset,
        batch_size=int(config["training"]["batch_size"]),
        shuffle=False,
        num_workers=0,
    )

    device = get_device()
    model = build_model(config)
    model = load_checkpoint_into_model(model, checkpoint_path, device)
    model = model.to(device)

    selected_bands = config["data"].get("bands", [])

    df = run_robustness_suite(
        model=model,
        dataloader=dataloader,
        output_dir=output_table_dir / experiment_id,
        n_channels=len(selected_bands) if selected_bands else None,
        band_names=selected_bands if selected_bands else None,
        device=device,
    )
    table_path = output_table_dir / f"{experiment_id}_robustness.csv"
    df.to_csv(table_path, index=False)

    output_table_dir.mkdir(parents=True, exist_ok=True)
    output_figure_dir.mkdir(parents=True, exist_ok=True)

    table_path = output_table_dir / f"{experiment_id}_robustness.csv"
    figure_path = output_figure_dir / f"{experiment_id}_robustness_macro_f1_drop.png"

    df.to_csv(table_path, index=False)
    plot_robustness(
        df,
        output_path=figure_path,
        title=f"{experiment_id} robustness analysis",
    )

    print(f"Saved: {table_path}")
    print(f"Saved: {figure_path}")

    return df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate robustness analysis for TerraSight models."
    )

    parser.add_argument(
        "--run-dir",
        required=True,
        help="Run directory, e.g. results/v4/<run_name>.",
    )

    parser.add_argument(
        "--output-table-dir",
        default="reports/tables/robustness",
    )

    parser.add_argument(
        "--output-figure-dir",
        default="reports/figures/robustness",
    )

    args = parser.parse_args()

    project_root = get_project_root()

    process_run(
        run_dir=project_root / args.run_dir,
        project_root=project_root,
        output_table_dir=project_root / args.output_table_dir,
        output_figure_dir=project_root / args.output_figure_dir,
    )


if __name__ == "__main__":
    main()