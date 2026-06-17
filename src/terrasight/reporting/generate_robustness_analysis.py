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


def add_gaussian_noise(images: torch.Tensor, std: float) -> torch.Tensor:
    return torch.clamp(images + torch.randn_like(images) * std, -5.0, 5.0)


def apply_brightness_shift(images: torch.Tensor, shift: float) -> torch.Tensor:
    return images + shift


def dropout_band(images: torch.Tensor, band_index: int) -> torch.Tensor:
    perturbed = images.clone()
    perturbed[:, band_index, :, :] = 0.0
    return perturbed


@torch.no_grad()
def evaluate_model(
    model: torch.nn.Module,
    dataloader: DataLoader,
    device: torch.device,
    perturbation: str,
    band_index: int | None = None,
    noise_std: float = 0.05,
    brightness_shift: float = 0.10,
) -> dict[str, float]:
    model.eval()

    y_true: list[int] = []
    y_pred: list[int] = []

    for batch in dataloader:
        if len(batch) == 3:
            images, labels, _metadata = batch
        else:
            images, labels = batch

        images = images.to(device)

        if perturbation == "clean":
            pass
        elif perturbation == "gaussian_noise":
            images = add_gaussian_noise(images, std=noise_std)
        elif perturbation == "brightness_plus":
            images = apply_brightness_shift(images, shift=brightness_shift)
        elif perturbation == "brightness_minus":
            images = apply_brightness_shift(images, shift=-brightness_shift)
        elif perturbation == "band_dropout":
            if band_index is None:
                raise ValueError("band_index is required for band_dropout.")
            images = dropout_band(images, band_index=band_index)
        else:
            raise ValueError(f"Unknown perturbation: {perturbation}")

        logits = model(images)
        preds = torch.argmax(logits, dim=1).detach().cpu().tolist()

        y_true.extend([int(x) for x in labels])
        y_pred.extend(preds)

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
    }


def plot_robustness(df: pd.DataFrame, output_path: Path, title: str) -> None:
    plot_df = df[df["perturbation"] != "clean"].copy()

    if plot_df.empty:
        return

    plot_df["label"] = plot_df.apply(
        lambda row: row["band"] if row["perturbation"] == "band_dropout" else row["perturbation"],
        axis=1,
    )

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

    rows: list[dict[str, Any]] = []

    clean_metrics = evaluate_model(
        model=model,
        dataloader=dataloader,
        device=device,
        perturbation="clean",
    )

    rows.append(
        {
            "experiment_id": experiment_id,
            "perturbation": "clean",
            "band": "",
            "accuracy": clean_metrics["accuracy"],
            "macro_f1": clean_metrics["macro_f1"],
            "accuracy_drop": 0.0,
            "macro_f1_drop": 0.0,
        }
    )

    for perturbation in ["gaussian_noise", "brightness_plus", "brightness_minus"]:
        metrics = evaluate_model(
            model=model,
            dataloader=dataloader,
            device=device,
            perturbation=perturbation,
        )

        rows.append(
            {
                "experiment_id": experiment_id,
                "perturbation": perturbation,
                "band": "",
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "accuracy_drop": clean_metrics["accuracy"] - metrics["accuracy"],
                "macro_f1_drop": clean_metrics["macro_f1"] - metrics["macro_f1"],
            }
        )

    selected_bands = config["data"].get("bands", [])

    for band_index, band_name in enumerate(selected_bands):
        metrics = evaluate_model(
            model=model,
            dataloader=dataloader,
            device=device,
            perturbation="band_dropout",
            band_index=band_index,
        )

        rows.append(
            {
                "experiment_id": experiment_id,
                "perturbation": "band_dropout",
                "band": band_name,
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "accuracy_drop": clean_metrics["accuracy"] - metrics["accuracy"],
                "macro_f1_drop": clean_metrics["macro_f1"] - metrics["macro_f1"],
            }
        )

    df = pd.DataFrame(rows)

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