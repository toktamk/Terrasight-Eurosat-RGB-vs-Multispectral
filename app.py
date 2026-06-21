from pathlib import Path
import json
import shutil
import subprocess

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import tifffile
import torch
from PIL import Image
from torchvision import transforms

from terrasight.data.band_registry import EUROSAT_CLASSES
from terrasight.data.preprocessing import normalize_multispectral_tensor
from terrasight.explainability.gradcam import GradCAM
from terrasight.features.band_selection import select_bands
from terrasight.models.multispectral_model import build_multispectral_model
from terrasight.models.rgb_model import build_rgb_model


PROJECT_ROOT = Path(__file__).resolve().parent


rgb_transform = transforms.Compose(
    [
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


# ============================================================
# SESSION STATE
# ============================================================

def init_session_state() -> None:
    defaults = {
        "rgb_source": "",
        "ms_source": "",
        "inference_done": False,
        "prediction": None,
        "confidence": None,
        "prob_table": None,
        "gradcam_fig": None,
        "last_model_label": None,
        "last_uploaded_name": None,
        "last_show_option": "Class probabilities",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_inference_state() -> None:
    st.session_state.inference_done = False
    st.session_state.prediction = None
    st.session_state.confidence = None
    st.session_state.prob_table = None
    st.session_state.gradcam_fig = None


# ============================================================
# MODEL DISCOVERY AND LOADING
# ============================================================

def discover_model_runs() -> list[dict]:
    runs = []

    for version in ["v1", "v4", "v5"]:
        version_dir = PROJECT_ROOT / "results" / version

        if not version_dir.exists():
            continue

        for run_dir in sorted(version_dir.iterdir()):
            if not run_dir.is_dir():
                continue

            checkpoint = run_dir / "best_model.pt"
            config_path = run_dir / "config.yaml"
            metrics_path = run_dir / "metrics.json"

            if not checkpoint.exists() or not config_path.exists():
                continue

            accuracy = None
            macro_f1 = None

            if metrics_path.exists():
                try:
                    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
                    accuracy = metrics.get("accuracy")
                    macro_f1 = metrics.get("macro_f1")
                except Exception:
                    pass

            label = f"{version} | {run_dir.name}"

            if accuracy is not None:
                label += f" | acc={accuracy:.4f}"

            if macro_f1 is not None:
                label += f" | macroF1={macro_f1:.4f}"

            runs.append(
                {
                    "label": label,
                    "version": version,
                    "run_dir": run_dir,
                    "checkpoint": checkpoint,
                    "config": config_path,
                    "metrics": metrics_path,
                    "accuracy": accuracy,
                    "macro_f1": macro_f1,
                }
            )

    runs = sorted(
        runs,
        key=lambda x: -1 if x["accuracy"] is None else float(x["accuracy"]),
        reverse=True,
    )

    return runs


def load_yaml_config(config_path: Path) -> dict:
    import yaml

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def infer_model_type(config: dict) -> str:
    return config.get("data", {}).get("input_type", "rgb")


@st.cache_resource
def load_any_model(checkpoint_path: str, config_path: str):
    config = load_yaml_config(Path(config_path))

    model_name = config["model"]["name"]
    input_channels = int(config["model"]["input_channels"])
    num_classes = int(config["model"]["num_classes"])
    input_type = infer_model_type(config)

    if input_type == "rgb":
        model = build_rgb_model(
            model_name=model_name,
            num_classes=num_classes,
            pretrained=False,
        )
    else:
        model = build_multispectral_model(
            model_name=model_name,
            input_channels=input_channels,
            num_classes=num_classes,
            pretrained=False,
        )

    state = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()

    return model, config


# ============================================================
# IMAGE LOADING
# ============================================================

def load_rgb_image(uploaded_file) -> tuple[torch.Tensor, Image.Image]:
    image = Image.open(uploaded_file).convert("RGB")
    image_tensor = rgb_transform(image).unsqueeze(0)
    return image_tensor, image


def load_multispectral_image(uploaded_file, config: dict) -> torch.Tensor:
    image_np = tifffile.imread(uploaded_file)
    image = torch.tensor(image_np, dtype=torch.float32)

    if image.ndim != 3:
        raise ValueError(
            f"Expected multispectral image with 3 dimensions, got {tuple(image.shape)}"
        )

    if image.shape[-1] == 13:
        image = image.permute(2, 0, 1)

    selected_bands = config["data"].get("bands")
    source_bands = config["data"].get("source_bands")

    if selected_bands is not None:
        image = select_bands(
            image=image,
            source_bands=source_bands,
            selected_bands=selected_bands,
        )

    image = normalize_multispectral_tensor(image)

    return image.unsqueeze(0)


# ============================================================
# INFERENCE AND GRAD-CAM
# ============================================================

def predict(model, image_tensor: torch.Tensor) -> tuple[int, float, dict]:
    with torch.no_grad():
        logits = model(image_tensor)
        probs = torch.softmax(logits, dim=1)[0]
        pred_idx = int(torch.argmax(probs))
        confidence = float(probs[pred_idx])

    prob_table = {
        EUROSAT_CLASSES[i]: float(probs[i])
        for i in range(len(EUROSAT_CLASSES))
    }

    return pred_idx, confidence, prob_table


def get_gradcam_target_layer(model):
    if hasattr(model, "layer4"):
        return model.layer4[-1]

    if hasattr(model, "features"):
        return model.features[-1]

    raise ValueError("Grad-CAM target layer could not be inferred for this model.")


def generate_gradcam_overlay(
    model,
    image_tensor: torch.Tensor,
    pil_image: Image.Image,
    class_index: int,
):
    target_layer = get_gradcam_target_layer(model)
    gradcam = GradCAM(model=model, target_layer=target_layer)

    cam = gradcam.generate(image_tensor, class_index=class_index)

    if isinstance(cam, torch.Tensor):
        cam = cam.detach().cpu().numpy()

    gradcam.close()

    if cam.ndim == 3:
        cam = np.squeeze(cam)

    image = pil_image.resize((64, 64))
    image_np = np.array(image).astype(np.float32) / 255.0

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(image_np)
    ax.imshow(cam, alpha=0.45, cmap="jet")
    ax.axis("off")

    return fig


def run_inference(
    model,
    image_tensor: torch.Tensor,
    input_type: str,
    pil_image: Image.Image | None,
    show_option: str,
) -> None:
    pred_idx, confidence, prob_table = predict(model, image_tensor)

    st.session_state.prediction = pred_idx
    st.session_state.confidence = confidence
    st.session_state.prob_table = prob_table
    st.session_state.gradcam_fig = None

    if show_option in ["Grad-CAM", "Both"]:
        if input_type == "rgb" and pil_image is not None:
            st.session_state.gradcam_fig = generate_gradcam_overlay(
                model=model,
                image_tensor=image_tensor,
                pil_image=pil_image,
                class_index=pred_idx,
            )

    st.session_state.inference_done = True


def render_inference_results(input_type: str, show_option: str) -> None:
    if not st.session_state.inference_done:
        return

    pred_idx = st.session_state.prediction
    confidence = st.session_state.confidence
    prob_table = st.session_state.prob_table

    if pred_idx is None or confidence is None or prob_table is None:
        return

    st.subheader("Prediction")
    st.metric("Predicted class", EUROSAT_CLASSES[pred_idx])
    st.metric("Confidence", f"{confidence:.3f}")

    if show_option in ["Class probabilities", "Both"]:
        st.subheader("Class Probabilities")

        prob_df = (
            pd.DataFrame(
                {
                    "class": list(prob_table.keys()),
                    "probability": list(prob_table.values()),
                }
            )
            .sort_values("probability", ascending=False)
            .reset_index(drop=True)
        )

        st.bar_chart(prob_df.set_index("class"))
        st.dataframe(prob_df, use_container_width=True)

    if show_option in ["Grad-CAM", "Both"]:
        st.subheader("Grad-CAM")

        if input_type != "rgb":
            st.warning(
                "Grad-CAM preview is currently enabled only for RGB image display in this lightweight UI."
            )
        elif st.session_state.gradcam_fig is not None:
            st.pyplot(st.session_state.gradcam_fig)
        else:
            st.warning("Grad-CAM was not generated. Please run inference again.")


# ============================================================
# WORKFLOW HELPERS
# ============================================================

def run_command(command: str) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True,
        text=True,
        capture_output=True,
    )

    return result.returncode, result.stdout + "\n" + result.stderr


def browse_folder() -> str:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory()
    root.destroy()

    return folder


def copy_dataset(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source folder not found: {source}")

    target.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        destination = target / item.name

        if item.is_dir():
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)


# ============================================================
# APP
# ============================================================

st.set_page_config(page_title="TerraSight Workflow and Inference UI", layout="wide")
init_session_state()

st.title("TerraSight: Workflow Launcher and Inference Demo")
st.caption(
    "Optional Streamlit interface. The official reproducibility path remains the command-line workflow."
)

left, right = st.columns([1, 1], gap="large")


# ============================================================
# LEFT COLUMN: PROJECT WORKFLOW
# ============================================================

with left:
    st.header("Project Workflow")

    st.subheader("1. Dataset Preparation")

    rgb_col1, rgb_col2 = st.columns([4, 1])

    with rgb_col1:
        rgb_source = st.text_input(
            "Source RGB dataset folder",
            value=st.session_state.rgb_source,
            key="rgb_source_input",
        )

    with rgb_col2:
        st.write("")
        st.write("")
        if st.button("Browse RGB"):
            selected = browse_folder()
            if selected:
                st.session_state.rgb_source = selected
                st.rerun()

    ms_col1, ms_col2 = st.columns([4, 1])

    with ms_col1:
        ms_source = st.text_input(
            "Source multispectral dataset folder",
            value=st.session_state.ms_source,
            key="ms_source_input",
        )

    with ms_col2:
        st.write("")
        st.write("")
        if st.button("Browse MS"):
            selected = browse_folder()
            if selected:
                st.session_state.ms_source = selected
                st.rerun()

    rgb_source = rgb_source or st.session_state.rgb_source
    ms_source = ms_source or st.session_state.ms_source

    if st.button("Copy datasets into data/raw"):
        try:
            if rgb_source:
                copy_dataset(Path(rgb_source), PROJECT_ROOT / "data/raw/rgb")
                st.success("RGB dataset copied to data/raw/rgb")

            if ms_source:
                copy_dataset(Path(ms_source), PROJECT_ROOT / "data/raw/multispectral")
                st.success("Multispectral dataset copied to data/raw/multispectral")

            if not rgb_source and not ms_source:
                st.warning("Please provide at least one source folder.")

        except Exception as exc:
            st.error(str(exc))

    st.subheader("2. Dataset Validation")

    if st.button("Validate dataset structure"):
        code, output = run_command("python -m terrasight.data.check_dataset_structure")
        st.code(output)
        st.success("Dataset validation completed") if code == 0 else st.error("Dataset validation failed")

    st.subheader("3. Train/Test Split")

    if st.button("Create 80/20 split"):
        code, output = run_command(
            "python -m terrasight.data.split --config configs/v1_rgb_baseline.yaml"
        )
        st.code(output)
        st.success("Split created") if code == 0 else st.error("Split creation failed")

    st.subheader("4. Training")

    train_option = st.selectbox(
        "Select training run",
        [
            "RGB baseline",
            "RGB scratch",
            "Multispectral scratch",
            "Multispectral adapted",
            "Best multispectral: RGB + RedEdge + NIR + SWIR",
        ],
        key="train_option",
    )

    train_commands = {
        "RGB baseline": "python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_baseline.yaml",
        "RGB scratch": "python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_scratch.yaml",
        "Multispectral scratch": "python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_scratch.yaml",
        "Multispectral adapted": "python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_pretrained_adapted.yaml",
        "Best multispectral: RGB + RedEdge + NIR + SWIR": "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_rededge_nir_swir.yaml",
    }

    if st.button("Run selected training"):
        code, output = run_command(train_commands[train_option])
        st.code(output)
        st.success("Training completed") if code == 0 else st.error("Training failed")

    st.subheader("5. Reporting and Analysis")

    report_option = st.selectbox(
        "Select report command",
        [
            "Prediction probabilities",
            "Comparison figures",
            "Per-class F1",
            "Reliability analysis",
            "Statistical validation",
            "Spectral separability",
            "Report asset check",
        ],
        key="report_option",
    )

    report_commands = {
        "Prediction probabilities": "python -m terrasight.reporting.generate_prediction_probabilities --results-root results --versions v1 v4 --output-dir reports/tables/probabilities",
        "Comparison figures": "python -m terrasight.reporting.generate_comparison_figures",
        "Per-class F1": "python -m terrasight.reporting.plot_per_class_f1",
        "Reliability analysis": "python -m terrasight.reporting.generate_reliability_analysis --input-dir reports/tables/probabilities --output-dir reports",
        "Statistical validation": 'python -m terrasight.reporting.statistical_analysis --model-a reports/tables/probabilities/v4_ablation_rgb_resnet18_pretrained_adapted_seed42_probabilities.csv --model-b reports/tables/probabilities/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_probabilities.csv --model-a-name "RGB ResNet18" --model-b-name "RGB+RedEdge+NIR+SWIR ResNet18" --output reports/tables/statistical_tests/statistical_analysis.csv --summary reports/tables/statistical_tests/statistical_summary.md --bootstrap 1000 --seed 42',
        "Spectral separability": "python -m terrasight.reporting.generate_spectral_separability --data-dir data/raw/multispectral --tables-dir reports/tables/spectral_analysis --figures-dir reports/figures/spectral_analysis",
        "Report asset check": "python -m terrasight.reporting.check_report_assets --show-discovered --strict",
    }

    if st.button("Run selected report command"):
        code, output = run_command(report_commands[report_option])
        st.code(output)
        st.success("Command completed") if code == 0 else st.error("Command failed")

    st.subheader("6. Reproducibility Checks")

    if st.button("Run reproducibility command tests"):
        code, output = run_command("pytest tests/test_reproducibility_commands.py")
        st.code(output)
        st.success("Reproducibility tests passed") if code == 0 else st.error("Reproducibility tests failed")

    if st.button("Run full test suite"):
        code, output = run_command("pytest")
        st.code(output)
        st.success("All tests passed") if code == 0 else st.error("Some tests failed")


# ============================================================
# RIGHT COLUMN: INFERENCE DEMO
# ============================================================

with right:
    st.header("Inference Demo")

    st.write(
        "Select a trained model from results/v1, results/v4, or results/v5, then upload an RGB or multispectral image."
    )

    model_runs = discover_model_runs()

    if not model_runs:
        st.warning("No trained runs found in results/v1, results/v4, or results/v5.")
    else:
        labels = [item["label"] for item in model_runs]

        selected_label = st.selectbox(
            "Select trained model",
            labels,
            index=0,
            key="selected_model_label",
        )

        selected_run = next(item for item in model_runs if item["label"] == selected_label)

        if st.session_state.last_model_label != selected_label:
            reset_inference_state()
            st.session_state.last_model_label = selected_label

        st.caption(f"Run directory: `{selected_run['run_dir']}`")
        st.caption(f"Checkpoint: `{selected_run['checkpoint']}`")
        st.caption(f"Config: `{selected_run['config']}`")

        config_preview = load_yaml_config(selected_run["config"])
        input_type = infer_model_type(config_preview)
        selected_bands = config_preview.get("data", {}).get("bands", [])

        st.write(f"**Model input type:** `{input_type}`")
        st.write(f"**Input channels:** `{config_preview['model']['input_channels']}`")

        if input_type == "multispectral":
            st.write(f"**Selected bands:** `{selected_bands}`")

        show_option = st.radio(
            "Show inference output",
            [
                "Class probabilities",
                "Grad-CAM",
                "Both",
            ],
            horizontal=True,
            key="show_option",
        )

        if st.session_state.last_show_option != show_option:
            st.session_state.last_show_option = show_option

        upload_types = ["jpg", "jpeg", "png"] if input_type == "rgb" else ["tif", "tiff"]

        uploaded_file = st.file_uploader(
            "Upload image",
            type=upload_types,
            key=f"uploaded_file_{input_type}",
        )

        if uploaded_file is not None:
            if st.session_state.last_uploaded_name != uploaded_file.name:
                reset_inference_state()
                st.session_state.last_uploaded_name = uploaded_file.name

            try:
                model, config = load_any_model(
                    str(selected_run["checkpoint"]),
                    str(selected_run["config"]),
                )

                pil_image = None

                if input_type == "rgb":
                    image_tensor, pil_image = load_rgb_image(uploaded_file)
                    st.image(
                        pil_image,
                        caption="Uploaded RGB image",
                        use_container_width=True,
                    )
                else:
                    image_tensor = load_multispectral_image(uploaded_file, config)
                    st.info(
                        "Multispectral TIFF uploaded. Display preview is omitted because the image has multiple spectral bands."
                    )

                if st.button("Run inference", key="run_inference_button"):
                    run_inference(
                        model=model,
                        image_tensor=image_tensor,
                        input_type=input_type,
                        pil_image=pil_image,
                        show_option=show_option,
                    )

                render_inference_results(
                    input_type=input_type,
                    show_option=show_option,
                )

            except Exception as exc:
                st.error(str(exc))

    st.divider()

    st.subheader("Useful Notes")

    st.markdown(
        """
        - Models are automatically discovered from `results/v1`, `results/v4`, and `results/v5`.
        - RGB models accept `.jpg`, `.jpeg`, or `.png`.
        - Multispectral models accept `.tif` or `.tiff`.
        - The selected model configuration determines whether RGB or multispectral input is expected.
        - Grad-CAM display is enabled only for RGB models in this lightweight UI.
        - This UI is optional; command-line reproduction remains the official workflow.
        """
    )