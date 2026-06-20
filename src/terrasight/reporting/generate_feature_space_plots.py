from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from torch.utils.data import DataLoader

from terrasight.data.band_registry import EUROSAT_CLASSES
from terrasight.reporting.generate_prediction_probabilities import (
    build_dataset,
    build_model,
    find_checkpoint,
)
from terrasight.reporting.generate_confusion_matrices import (
    get_device,
    get_project_root,
    load_checkpoint_into_model,
)
from terrasight.utils.config import load_config


def get_sample_path(metadata: Any) -> str:
    if isinstance(metadata, dict):
        for key in ("path", "image_path", "filepath", "file_path"):
            value = metadata.get(key)
            if value is not None:
                if isinstance(value, (list, tuple)):
                    return str(value[0])
                return str(value)
    return ""


def resolve_feature_module(model: nn.Module) -> nn.Module:
    candidate = model

    if hasattr(candidate, "model"):
        candidate = candidate.model

    if hasattr(candidate, "backbone"):
        candidate = candidate.backbone

    # ResNet-style models
    if hasattr(candidate, "avgpool"):
        return candidate.avgpool

    # EfficientNet-style torchvision models
    if hasattr(candidate, "features"):
        return candidate.features

    # Generic fallback: last convolutional block
    conv_layers = [m for m in candidate.modules() if isinstance(m, nn.Conv2d)]
    if conv_layers:
        return conv_layers[-1]

    raise ValueError("Could not identify a suitable feature extraction layer.")


class FeatureExtractor:
    def __init__(self, model: nn.Module, module: nn.Module) -> None:
        self.model = model
        self.module = module
        self.features: torch.Tensor | None = None
        self.hook = module.register_forward_hook(self._hook_fn)

    def _hook_fn(
        self,
        _module: nn.Module,
        _inputs: tuple[torch.Tensor, ...],
        output: torch.Tensor,
    ) -> None:
        self.features = output.detach()

    def close(self) -> None:
        self.hook.remove()


def flatten_features(features: torch.Tensor) -> torch.Tensor:
    if features.ndim == 4:
        features = torch.flatten(features, start_dim=1)
    elif features.ndim > 2:
        features = features.reshape(features.shape[0], -1)
    return features


@torch.no_grad()
def extract_features(
    model: nn.Module,
    dataloader: DataLoader,
    device: torch.device,
    max_samples: int | None,
) -> pd.DataFrame:
    model.eval()

    feature_module = resolve_feature_module(model)
    extractor = FeatureExtractor(model, feature_module)

    rows: list[dict[str, Any]] = []
    feature_chunks: list[np.ndarray] = []

    seen = 0

    try:
        for images, labels, metadata in dataloader:
            images = images.to(device)
            labels = labels.to(device)

            logits = model(images)
            probabilities = torch.softmax(logits, dim=1)
            predictions = torch.argmax(probabilities, dim=1)
            confidences = probabilities.max(dim=1).values

            if extractor.features is None:
                raise RuntimeError("Feature hook did not capture activations.")

            features = flatten_features(extractor.features).cpu().numpy()

            batch_size = images.size(0)

            for i in range(batch_size):
                if max_samples is not None and seen >= max_samples:
                    break

                true_label = int(labels[i].detach().cpu().item())
                predicted_label = int(predictions[i].detach().cpu().item())

                sample_metadata: Any = metadata
                if isinstance(metadata, dict):
                    sample_metadata = {
                        key: value[i] if isinstance(value, (list, tuple)) else value
                        for key, value in metadata.items()
                    }

                rows.append(
                    {
                        "sample_index": seen,
                        "path": get_sample_path(sample_metadata),
                        "true_label": true_label,
                        "true_class": EUROSAT_CLASSES[true_label],
                        "predicted_label": predicted_label,
                        "predicted_class": EUROSAT_CLASSES[predicted_label],
                        "confidence": float(confidences[i].detach().cpu().item()),
                        "correct": bool(true_label == predicted_label),
                    }
                )

                feature_chunks.append(features[i : i + 1])
                seen += 1

            if max_samples is not None and seen >= max_samples:
                break

    finally:
        extractor.close()

    if not feature_chunks:
        raise RuntimeError("No features were extracted.")

    feature_matrix = np.concatenate(feature_chunks, axis=0)

    df = pd.DataFrame(rows)
    feature_columns = [f"feature_{i:04d}" for i in range(feature_matrix.shape[1])]
    feature_df = pd.DataFrame(feature_matrix, columns=feature_columns)

    return pd.concat([df, feature_df], axis=1)


def reduce_features(
    features: np.ndarray,
    method: str,
    random_state: int,
    pca_dim: int,
    perplexity: float,
    n_neighbors: int,
    min_dist: float,
) -> np.ndarray:
    if features.shape[1] > pca_dim:
        features = PCA(
            n_components=pca_dim,
            random_state=random_state,
        ).fit_transform(features)

    if method == "tsne":
        effective_perplexity = min(perplexity, max(5, (features.shape[0] - 1) / 3))
        return TSNE(
            n_components=2,
            perplexity=effective_perplexity,
            init="pca",
            learning_rate="auto",
            random_state=random_state,
        ).fit_transform(features)

    if method == "umap":
        try:
            import umap
        except ImportError as exc:
            raise ImportError(
                "UMAP is not installed. Install it with: pip install umap-learn"
            ) from exc

        return umap.UMAP(
            n_components=2,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            metric="euclidean",
            random_state=random_state,
        ).fit_transform(features)

    raise ValueError(f"Unsupported method: {method}")


def plot_embedding(
    df: pd.DataFrame,
    output_path: Path,
    title: str,
    color_by: str,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 7))

    if color_by == "true_class":
        classes = list(EUROSAT_CLASSES)
        for cls in classes:
            subset = df[df["true_class"] == cls]
            ax.scatter(
                subset["dim1"],
                subset["dim2"],
                s=14,
                alpha=0.75,
                label=cls,
            )

        ax.legend(
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=False,
            fontsize=8,
        )

    elif color_by == "correct":
        correct = df[df["correct"] == True]
        incorrect = df[df["correct"] == False]

        ax.scatter(
            correct["dim1"],
            correct["dim2"],
            s=12,
            alpha=0.65,
            label="Correct",
        )
        ax.scatter(
            incorrect["dim1"],
            incorrect["dim2"],
            s=28,
            alpha=0.9,
            marker="x",
            label="Incorrect",
        )
        ax.legend(frameon=False)

    else:
        raise ValueError("color_by must be either 'true_class' or 'correct'.")

    ax.set_title(title)
    ax.set_xlabel("Dimension 1")
    ax.set_ylabel("Dimension 2")
    ax.grid(True, linewidth=0.3, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate t-SNE/UMAP feature-space plots for a trained TerraSight run."
    )

    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--method", choices=["tsne", "umap", "both"], default="both")
    parser.add_argument("--output-dir", default="reports/figures/feature_space")
    parser.add_argument("--table-output-dir", default="reports/tables/feature_space")
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--max-samples", type=int, default=3000)
    parser.add_argument("--pca-dim", type=int, default=50)
    parser.add_argument("--perplexity", type=float, default=30.0)
    parser.add_argument("--n-neighbors", type=int, default=15)
    parser.add_argument("--min-dist", type=float, default=0.1)
    parser.add_argument("--random-state", type=int, default=42)

    args = parser.parse_args()

    root = get_project_root()
    run_dir = root / args.run_dir
    output_dir = root / args.output_dir
    table_output_dir = root / args.table_output_dir

    output_dir.mkdir(parents=True, exist_ok=True)
    table_output_dir.mkdir(parents=True, exist_ok=True)

    config_path = run_dir / "config.yaml"
    checkpoint_path = find_checkpoint(run_dir)

    if not config_path.exists():
        raise FileNotFoundError(config_path)

    if checkpoint_path is None:
        raise FileNotFoundError(f"No checkpoint found in: {run_dir}")

    config = load_config(config_path)
    experiment_id = config["experiment"]["id"]

    dataset = build_dataset(config, root)

    batch_size = args.batch_size
    if batch_size is None:
        batch_size = int(config.get("training", {}).get("batch_size", 32))

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
    )

    device = get_device()

    model = build_model(config)
    model = load_checkpoint_into_model(model, checkpoint_path, device)
    model = model.to(device)
    model.eval()

    feature_df = extract_features(
        model=model,
        dataloader=dataloader,
        device=device,
        max_samples=args.max_samples,
    )

    feature_path = table_output_dir / f"{experiment_id}_features.csv"
    feature_df.to_csv(feature_path, index=False)

    feature_cols = [c for c in feature_df.columns if c.startswith("feature_")]
    feature_matrix = feature_df[feature_cols].to_numpy(dtype=np.float32)

    methods = ["tsne", "umap"] if args.method == "both" else [args.method]

    summary: dict[str, Any] = {
        "experiment_id": experiment_id,
        "run_dir": str(run_dir.relative_to(root)),
        "checkpoint": str(checkpoint_path.relative_to(root)),
        "n_samples": int(len(feature_df)),
        "n_features": int(len(feature_cols)),
        "methods": methods,
    }

    for method in methods:
        embedding = reduce_features(
            features=feature_matrix,
            method=method,
            random_state=args.random_state,
            pca_dim=args.pca_dim,
            perplexity=args.perplexity,
            n_neighbors=args.n_neighbors,
            min_dist=args.min_dist,
        )

        embed_df = feature_df[
            [
                "sample_index",
                "path",
                "true_label",
                "true_class",
                "predicted_label",
                "predicted_class",
                "confidence",
                "correct",
            ]
        ].copy()

        embed_df["dim1"] = embedding[:, 0]
        embed_df["dim2"] = embedding[:, 1]

        embedding_path = table_output_dir / f"{experiment_id}_{method}_embedding.csv"
        embed_df.to_csv(embedding_path, index=False)

        class_plot_path = output_dir / f"{experiment_id}_{method}_by_class.png"
        correctness_plot_path = output_dir / f"{experiment_id}_{method}_by_correctness.png"

        plot_embedding(
            df=embed_df,
            output_path=class_plot_path,
            title=f"{experiment_id}: {method.upper()} feature space by class",
            color_by="true_class",
        )

        plot_embedding(
            df=embed_df,
            output_path=correctness_plot_path,
            title=f"{experiment_id}: {method.upper()} feature space by correctness",
            color_by="correct",
        )

        summary[f"{method}_embedding_csv"] = str(embedding_path.relative_to(root))
        summary[f"{method}_class_plot"] = str(class_plot_path.relative_to(root))
        summary[f"{method}_correctness_plot"] = str(correctness_plot_path.relative_to(root))

        print(f"Saved {method.upper()} embedding: {embedding_path}")
        print(f"Saved {method.upper()} class plot: {class_plot_path}")
        print(f"Saved {method.upper()} correctness plot: {correctness_plot_path}")

    summary_path = table_output_dir / f"{experiment_id}_feature_space_summary.json"
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print(f"Saved feature table: {feature_path}")
    print(f"Saved summary: {summary_path}")


if __name__ == "__main__":
    main()