from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
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


class SimpleGradCAM:
    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module) -> None:
        self.model = model
        self.target_layer = target_layer
        self.activations: torch.Tensor | None = None
        self.gradients: torch.Tensor | None = None

        self.forward_hook = target_layer.register_forward_hook(self._save_activation)
        self.backward_hook = target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module: torch.nn.Module, inputs: Any, output: torch.Tensor) -> None:
        self.activations = output.detach()

    def _save_gradient(
        self,
        module: torch.nn.Module,
        grad_input: Any,
        grad_output: tuple[torch.Tensor, ...],
    ) -> None:
        self.gradients = grad_output[0].detach()

    def generate(self, image: torch.Tensor, class_index: int) -> np.ndarray:
        self.model.zero_grad(set_to_none=True)

        logits = self.model(image)
        score = logits[:, class_index].sum()
        score.backward()

        if self.activations is None or self.gradients is None:
            raise RuntimeError("Grad-CAM hooks did not capture activations/gradients.")

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = torch.relu(cam)

        cam = F.interpolate(
            cam,
            size=image.shape[-2:],
            mode="bilinear",
            align_corners=False,
        )

        cam = cam[0, 0].detach().cpu().numpy()
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)

        return cam

    def close(self) -> None:
        self.forward_hook.remove()
        self.backward_hook.remove()


def get_resnet_target_layer(
    model: torch.nn.Module,
    preferred_layer: str = "layer2",
) -> torch.nn.Module:
    candidate = model

    if hasattr(candidate, "model"):
        candidate = candidate.model

    if hasattr(candidate, "backbone"):
        candidate = candidate.backbone

    if hasattr(candidate, "features"):
        candidate = candidate.features

    if preferred_layer == "layer2" and hasattr(candidate, "layer2"):
        return candidate.layer2[-1]

    if preferred_layer == "layer3" and hasattr(candidate, "layer3"):
        return candidate.layer3[-1]

    if preferred_layer == "layer4" and hasattr(candidate, "layer4"):
        return candidate.layer4[-1]

    if hasattr(candidate, "layer2"):
        return candidate.layer2[-1]

    if hasattr(candidate, "layer3"):
        return candidate.layer3[-1]

    if hasattr(candidate, "layer4"):
        return candidate.layer4[-1]

    modules = list(candidate.modules())
    conv_layers = [m for m in modules if isinstance(m, torch.nn.Conv2d)]

    if not conv_layers:
        raise ValueError("Could not find a Conv2d layer for Grad-CAM.")

    return conv_layers[-1]

def tensor_to_display_rgb(image: torch.Tensor) -> np.ndarray:
    x = image.detach().cpu()

    if x.ndim == 4:
        x = x[0]

    if x.shape[0] >= 3:
        rgb = x[:3]
    else:
        rgb = x.repeat(3, 1, 1)[:3]

    rgb = rgb.numpy().transpose(1, 2, 0)
    low, high = np.percentile(rgb, [2, 98])
    rgb = np.clip((rgb - low) / (high - low + 1e-8), 0, 1)

    return rgb


def overlay_heatmap(rgb: np.ndarray, heatmap: np.ndarray) -> np.ndarray:
    cmap = plt.get_cmap("jet")
    heat = cmap(heatmap)[:, :, :3]
    return np.clip((0.55 * rgb) + (0.45 * heat), 0, 1)


def class_to_index(class_name: str | None) -> int | None:
    if class_name is None:
        return None

    normalized = class_name.replace(" ", "").replace("_", "").lower()

    for idx, cls in enumerate(EUROSAT_CLASSES):
        if cls.replace(" ", "").replace("_", "").lower() == normalized:
            return idx

    raise ValueError(f"Unknown class name: {class_name}")


def predict_single(model: torch.nn.Module, image: torch.Tensor, device: torch.device) -> tuple[int, float]:
    model.eval()

    with torch.no_grad():
        logits = model(image.unsqueeze(0).to(device))
        probs = torch.softmax(logits, dim=1)
        pred = int(torch.argmax(probs, dim=1).item())
        confidence = float(probs[0, pred].item())

    return pred, confidence


def get_sample_path(metadata: Any) -> str:
    if isinstance(metadata, dict):
        for key in ["path", "image_path", "filepath", "file_path"]:
            if key in metadata:
                value = metadata[key]
                if isinstance(value, (list, tuple)):
                    return str(value[0])
                return str(value)

    return ""


def collect_candidates(
    model: torch.nn.Module,
    dataset: Any,
    device: torch.device,
    selection_mode: str,
    min_confidence: float,
    true_class: str | None,
    pred_class: str | None,
    failure_csv: Path | None,
) -> list[dict[str, Any]]:
    true_idx = class_to_index(true_class)
    pred_idx = class_to_index(pred_class)

    allowed_paths: set[str] | None = None

    if failure_csv is not None:
        failure_df = pd.read_csv(failure_csv)
        if "path" not in failure_df.columns:
            raise ValueError(f"failure_csv must contain a path column: {failure_csv}")
        allowed_paths = set(failure_df["path"].astype(str).tolist())

    candidates: list[dict[str, Any]] = []

    for idx in range(len(dataset)):
        image, label, metadata = dataset[idx]
        label = int(label)
        sample_path = get_sample_path(metadata)

        if allowed_paths is not None and sample_path not in allowed_paths:
            continue

        pred, confidence = predict_single(model, image, device)
        correct = label == pred

        keep = False

        if selection_mode == "first":
            keep = True

        elif selection_mode == "correct_high_confidence":
            keep = correct and confidence >= min_confidence

        elif selection_mode == "high_confidence_failure":
            keep = (not correct) and confidence >= min_confidence

        elif selection_mode == "confusion_pair":
            if true_idx is None or pred_idx is None:
                raise ValueError(
                    "--true-class and --pred-class are required for confusion_pair mode."
                )
            keep = label == true_idx and pred == pred_idx

        elif selection_mode == "class_examples":
            if true_idx is None:
                raise ValueError("--true-class is required for class_examples mode.")
            keep = label == true_idx

        elif selection_mode == "failure_csv":
            keep = allowed_paths is not None

        else:
            raise ValueError(f"Unknown selection mode: {selection_mode}")

        if keep:
            candidates.append(
                {
                    "dataset_index": idx,
                    "image": image,
                    "true_label": label,
                    "predicted_label": pred,
                    "confidence": confidence,
                    "correct": correct,
                    "path": sample_path,
                }
            )

    if selection_mode in {"correct_high_confidence", "high_confidence_failure", "failure_csv"}:
        candidates = sorted(candidates, key=lambda x: x["confidence"], reverse=True)

    return candidates


def save_gradcam_figure(
    model: torch.nn.Module,
    gradcam: SimpleGradCAM,
    candidate: dict[str, Any],
    device: torch.device,
    output_path: Path,
) -> None:
    image = candidate["image"]
    true_label = int(candidate["true_label"])
    pred_label = int(candidate["predicted_label"])
    confidence = float(candidate["confidence"])
    correct = bool(candidate["correct"])

    image_batch = image.unsqueeze(0).to(device)
    heatmap = gradcam.generate(image_batch, class_index=pred_label)

    rgb = tensor_to_display_rgb(image)
    overlay = overlay_heatmap(rgb, heatmap)

    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    axes[0].imshow(rgb)
    axes[0].set_title("RGB composite")

    axes[1].imshow(heatmap)
    axes[1].set_title("Grad-CAM")

    axes[2].imshow(overlay)
    status = "Correct" if correct else "Wrong"
    axes[2].set_title(
        f"{status}\n"
        f"True: {EUROSAT_CLASSES[true_label]}\n"
        f"Pred: {EUROSAT_CLASSES[pred_label]}\n"
        f"Conf: {confidence:.3f}"
    )

    for ax in axes:
        ax.axis("off")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Grad-CAM examples for a saved TerraSight run."
    )

    parser.add_argument(
        "--run-dir",
        required=True,
        help="Path to a saved run directory, for example results/v4/<run_name>.",
    )

    parser.add_argument(
        "--output-dir",
        default="reports/figures/gradcam",
        help="Directory where Grad-CAM figures are saved.",
    )

    parser.add_argument(
        "--metadata-output",
        default="reports/tables/gradcam_examples.csv",
        help="CSV file where Grad-CAM metadata is saved.",
    )

    parser.add_argument(
        "--num-examples",
        type=int,
        default=8,
        help="Maximum number of Grad-CAM examples to save.",
    )

    parser.add_argument(
        "--selection-mode",
        default="correct_high_confidence",
        choices=[
            "first",
            "correct_high_confidence",
            "high_confidence_failure",
            "confusion_pair",
            "class_examples",
            "failure_csv",
        ],
        help="Sample-selection strategy.",
    )

    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.90,
        help="Minimum confidence for high-confidence selection modes.",
    )

    parser.add_argument(
        "--true-class",
        default=None,
        help="True class name for confusion_pair or class_examples mode.",
    )

    parser.add_argument(
        "--pred-class",
        default=None,
        help="Predicted class name for confusion_pair mode.",
    )

    parser.add_argument(
        "--failure-csv",
        default=None,
        help="Optional high-confidence failure CSV generated by generate_failure_cases.py.",
    )
    parser.add_argument(
        "--target-layer",
        default="layer2",
        choices=["layer2", "layer3", "layer4"],
        help="ResNet layer used for Grad-CAM. For 64x64 EuroSAT images, layer2 is recommended.",
    )


    args = parser.parse_args()

    root = get_project_root()
    run_dir = root / args.run_dir
    output_dir = root / args.output_dir
    metadata_output = root / args.metadata_output
    layer_tag = args.target_layer
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_output.parent.mkdir(parents=True, exist_ok=True)

    config_path = run_dir / "config.yaml"
    checkpoint_path = find_checkpoint(run_dir)

    if not config_path.exists():
        raise FileNotFoundError(config_path)

    if checkpoint_path is None:
        raise FileNotFoundError(f"No checkpoint found in: {run_dir}")

    config = load_config(config_path)
    experiment_id = config["experiment"]["id"]

    dataset = build_dataset(config, root)

    device = get_device()
    model = build_model(config)
    model = load_checkpoint_into_model(model, checkpoint_path, device)
    model = model.to(device)
    model.eval()

    target_layer = get_resnet_target_layer(model, preferred_layer=args.target_layer)
    gradcam = SimpleGradCAM(model, target_layer)

    failure_csv = root / args.failure_csv if args.failure_csv else None

    candidates = collect_candidates(
        model=model,
        dataset=dataset,
        device=device,
        selection_mode=args.selection_mode,
        min_confidence=args.min_confidence,
        true_class=args.true_class,
        pred_class=args.pred_class,
        failure_csv=failure_csv,
    )

    if not candidates:
        gradcam.close()
        raise RuntimeError("No Grad-CAM candidates matched the requested selection criteria.")

    rows: list[dict[str, Any]] = []

    for save_idx, candidate in enumerate(candidates[: args.num_examples]):
        true_name = EUROSAT_CLASSES[int(candidate["true_label"])]
        pred_name = EUROSAT_CLASSES[int(candidate["predicted_label"])]

        safe_true = true_name.replace(" ", "")
        safe_pred = pred_name.replace(" ", "")

        output_path = (
            output_dir
            / f"{experiment_id}_{args.selection_mode}_{save_idx:02d}_{safe_true}_to_{safe_pred}.png"
        )

        output_path = (
                output_dir
                / (
                    f"{experiment_id}_"
                    f"{layer_tag}_"
                    f"{args.selection_mode}_"
                    f"{save_idx:02d}_"
                    f"{safe_true}_to_{safe_pred}.png"
                )
        )

        save_gradcam_figure(
            model=model,
            gradcam=gradcam,
            candidate=candidate,
            device=device,
            output_path=output_path,
        )

        rows.append(
            {
                "experiment_id": experiment_id,
                "selection_mode": args.selection_mode,
                "dataset_index": candidate["dataset_index"],
                "path": candidate["path"],
                "true_class": true_name,
                "predicted_class": pred_name,
                "confidence": candidate["confidence"],
                "correct": candidate["correct"],
                "figure_path": str(output_path.relative_to(root)),
            }
        )

    gradcam.close()

    write_header = not metadata_output.exists()

    with metadata_output.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        if write_header:
            writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} Grad-CAM figures to: {output_dir}")
    print(f"Saved metadata to: {metadata_output}")


if __name__ == "__main__":
    main()