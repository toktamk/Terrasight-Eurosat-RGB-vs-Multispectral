# Reproducibility Checklist

This document provides a practical checklist for reproducing the main experiments, analyses, and figures reported in the TerraSight project.

## Environment Setup

### Repository

* [ ] Clone repository

```bash
git clone <REPOSITORY_URL>
cd terrasight-eurosat-rgb-vs-multispectral
```

### Python Environment

* [ ] Create virtual environment

```bash
python -m venv .venv
```

* [ ] Activate environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

* [ ] Install dependencies

```bash
pip install -r requirements.txt
```

### Verification

* [ ] Verify installation

```bash
pytest tests/test_imports.py
```

---

## Dataset Preparation

### EuroSAT RGB Dataset

* [ ] Download EuroSAT RGB dataset
* [ ] Place files in:

```text
data/raw/rgb/
```

### EuroSAT Multispectral Dataset

* [ ] Download EuroSAT Sentinel-2 multispectral dataset
* [ ] Place files in:

```text
data/raw/multispectral/
```

### Dataset Validation

* [ ] Verify dataset structure

```bash
python -m terrasight.data.check_dataset_structure
```

---

## Training Experiments

### RGB Baseline

* [ ] Train RGB pretrained ResNet18

```bash
python -m terrasight.training.train --config configs/v1_rgb_resnet18_pretrained_seed42.yaml
```

### Best Multispectral Model

* [ ] Train RGB + RedEdge + NIR + SWIR ResNet18

```bash
python -m terrasight.training.train --config configs/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42.yaml
```

### Multi-Seed Validation

* [ ] Train seed 43

```bash
python -m terrasight.training.train --config configs/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed43.yaml
```

* [ ] Train seed 44

```bash
python -m terrasight.training.train --config configs/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed44.yaml
```

---

## Evaluation

### Evaluate Trained Models

* [ ] Generate evaluation metrics

```bash
python -m terrasight.evaluation.evaluate --run-dir <RUN_DIR>
```

### Update Experiment Registry

* [ ] Register results

```bash
python -m terrasight.reporting.update_registry --runs-dir experiments
```

---

## Reporting

### Model Comparison

* [ ] Generate version comparison figures

```bash
python -m terrasight.reporting.generate_report_figures --version v4 --registry experiments/registry.csv --output-dir reports/figures
```

### Reliability Analysis

* [ ] Generate calibration and confidence analysis

```bash
python -m terrasight.reporting.generate_reliability_analysis --probabilities reports/tables/probabilities/<BEST_MODEL_PROBABILITIES>.csv --output-dir reports/figures/reliability
```

### Explainability Analysis

* [ ] Generate Grad-CAM visualizations

```bash
python -m terrasight.reporting.generate_gradcam_report --run-dir <BEST_RUN_DIR> --output-dir reports/figures/gradcam
```

### Failure Analysis

* [ ] Generate failure-case report

```bash
python -m terrasight.reporting.generate_failure_cases --probabilities reports/tables/probabilities/<BEST_MODEL_PROBABILITIES>.csv --output-dir reports/figures/failure_cases
```

### Robustness Analysis

* [ ] Generate robustness report

```bash
python -m terrasight.reporting.generate_robustness_analysis --run-dir <BEST_RUN_DIR> --output-dir reports/tables/robustness
```

### Statistical Validation

* [ ] Generate bootstrap and McNemar analysis

```bash
python -m terrasight.reporting.statistical_analysis --model-a reports/tables/probabilities/<MODEL_A_PROBABILITIES>.csv --model-b reports/tables/probabilities/<MODEL_B_PROBABILITIES>.csv --model-a-name "<MODEL_A_NAME>" --model-b-name "<MODEL_B_NAME>" --output reports/tables/statistical_tests/statistical_analysis.csv --summary reports/tables/statistical_tests/statistical_summary.md --bootstrap 1000 --seed 42
```

### Spectral Separability Analysis

* [ ] Generate Bhattacharyya Distance and Spectral Angle Mapper analyses

```bash
python -m terrasight.reporting.generate_spectral_separability --data-dir <MULTISPECTRAL_DATASET_DIR> --tables-dir reports/tables/spectral_analysis --figures-dir reports/figures/spectral_analysis
```

---

## Automated Validation

### Unit Tests

* [ ] Execute complete test suite

```bash
pytest
```

### Reproducibility Commands

* [ ] Verify reproducibility commands

```bash
pytest tests/test_reproducibility_commands.py
```

### Report Asset Validation

* [ ] Verify generated report assets

```bash
python -m terrasight.reporting.check_report_assets
```

---

## Expected Outputs

Successful reproduction should generate:

```text
experiments/
reports/figures/
reports/tables/
```

including:

* model comparison figures
* confusion matrices
* reliability diagrams
* Grad-CAM visualizations
* failure analysis reports
* robustness reports
* statistical validation reports
* spectral separability analyses

---

## Reproducibility Status

| Component                      | Verified |
| ------------------------------ | -------- |
| Dataset Loading                | ☐        |
| Training Pipeline              | ☐        |
| Evaluation Pipeline            | ☐        |
| Reporting Pipeline             | ☐        |
| Statistical Validation         | ☐        |
| Spectral Separability Analysis | ☐        |
| Unit Tests                     | ☐        |
| Reproducibility Tests          | ☐        |
| Asset Validation               | ☐        |

Complete all checklist items before creating a final release or submission package.
