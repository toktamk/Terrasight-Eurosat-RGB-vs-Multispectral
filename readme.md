# TerraSight: EuroSAT RGB vs Multispectral Classification

## Toktam Khatibi
### AI and Machine Learning Researcher 

## Overview

TerraSight is a research-grade machine learning framework for investigating the value of multispectral Sentinel-2 imagery for land-use and land-cover (LULC) classification using the EuroSAT dataset.

The project was developed as part of a systematic, evidence-based workflow that emphasizes:

* Scientific rigor
* Reproducibility
* Reliability
* Explainability
* Comparative evaluation
* Industrial applicability

The primary research question is:

> Does multispectral information beyond standard RGB imagery improve land-use classification performance, reliability, and interpretability?



# Research Objectives

The project evaluates and compares:

### RGB Baseline

Using Sentinel-2 visible bands:

* B4 (Red)
* B3 (Green)
* B2 (Blue)

### Multispectral Models

Using all available Sentinel-2 bands:

* Coastal Aerosol (B1)
* Blue (B2)
* Green (B3)
* Red (B4)
* Red Edge 1 (B5)
* Red Edge 2 (B6)
* Red Edge 3 (B7)
* Near Infrared (B8)
* Narrow NIR (B8A)
* Water Vapour (B9)
* Cirrus (B10)
* SWIR1 (B11)
* SWIR2 (B12)

### Advanced Evaluation Areas

* Band-ablation analysis
* Spectral-index augmentation
* Reliability analysis
* Calibration assessment
* Explainability and attribution
* Error analysis
* Reproducibility tracking



# Dataset

## EuroSAT RGB

```text
data/raw/rgb/
├── AnnualCrop/
├── Forest/
├── HerbaceousVegetation/
├── Highway/
├── Industrial/
├── Pasture/
├── PermanentCrop/
├── Residential/
├── River/
└── SeaLake/
```

## EuroSAT Multispectral

```text
data/raw/multispectral/
├── AnnualCrop/
├── Forest/
├── HerbaceousVegetation/
├── Highway/
├── Industrial/
├── Pasture/
├── PermanentCrop/
├── Residential/
├── River/
└── SeaLake/
```

Each TIFF file contains:

```text
64 × 64 × 13
```

multispectral Sentinel-2 observations.



# Repository Structure

```text
terrasight-eurosat-rgb-vs-multispectral/

├── configs/
├── data/
├── experiments/
├── reports/
├── results/
├── scripts/
├── src/
│   └── terrasight/
│       ├── data/
│       ├── features/
│       ├── models/
│       ├── training/
│       ├── evaluation/
│       ├── reliability/
│       ├── explainability/
│       ├── experiments/
│       ├── reporting/
│       ├── pipelines/
│       └── utils/
├── tests/
├── pyproject.toml
└── README.md
```



# Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install project:

```powershell
pip install -e .
```

Install dependencies:

```powershell
pip install torch torchvision
pip install pandas numpy scikit-learn matplotlib pyyaml tifffile pytest
```

Verify installation:

```powershell
python -c "import terrasight; print('OK')"
```



# Create Train/Test Split

Generate a stratified split:

```powershell
python -m terrasight.data.split --config configs\v1_rgb_baseline.yaml
```

Expected outputs:

```text
data/splits/
├── train.csv
└── test.csv
```



# RGB Baseline Training

Run:

```powershell
$env:KMP_DUPLICATE_LIB_OK="TRUE"

python -m terrasight.pipelines.train_rgb `
    --config configs\v1_rgb_baseline.yaml
```

Output:

```text
results/v1/<timestamp>_<experiment_id>/
```



# Multispectral Training

Run:

```powershell
$env:KMP_DUPLICATE_LIB_OK="TRUE"

python -m terrasight.pipelines.train_multispectral `
    --config configs\v1_multispectral.yaml
```

Output:

```text
results/v1/<timestamp>_<experiment_id>/
```



# Spectral Indices

Implemented:

## NDVI

```text
(NIR - Red) / (NIR + Red)
```

## NDWI

```text
(Green - NIR) / (Green + NIR)
```

## NDBI

```text
(SWIR - NIR) / (SWIR + NIR)
```

Purpose:

* vegetation discrimination
* water detection
* built-up area detection



# Band Ablation Framework

Available predefined band sets:

| Band Set             | Bands                      |
| -- |-|
| rgb                  | B4,B3,B2                   |
| rgb_nir              | RGB and B8                 |
| rgb_rededge_nir      | RGB, RedEdge and NIR       |
| rgb_rededge_nir_swir | RGB, RedEdge, NIR and SWIR |
| full_13              | All Sentinel-2 bands       |

Purpose:

* quantify contribution of spectral information
* identify useful bands
* support scientific interpretation



# Reliability Framework

Implemented metrics:

## Calibration

* Expected Calibration Error (ECE)
* Maximum Calibration Error (MCE)
* Brier Score

## Uncertainty

* Predictive Entropy
* Confidence Margin
* Confidence Error Analysis

## Failure Analysis

* Failure extraction
* Confusion pair analysis
* Worst-class identification

## Robustness

* Gaussian noise
* Brightness perturbation
* Spectral-band dropout



# Explainability Framework

Implemented:

## Grad-CAM

Spatial explanation maps for CNN models.

## Spectral Attribution

Band-occlusion analysis:

```text
Remove one band
↓
Measure confidence drop
↓
Estimate band importance
```

Outputs:

* ranked band importance
* class-level spectral explanations



# Experiment Tracking

Every run is automatically tracked.

Registry:

```text
experiments/registry.csv
```

Tracks:

* experiment id
* version
* model
* bands
* metrics
* output directory

Purpose:

* reproducibility
* experiment comparison
* benchmark tracking



# Reporting

Generate report assets:

```powershell
python -m terrasight.reporting.report_assets `
    --run-dir results\v1\<RUN_FOLDER> `
    --experiment-name rgb_resnet18
```

Outputs:

```text
reports/
├── tables/
└── figures/
```

Generated assets:

* metrics tables
* training curves
* comparison charts



# Experiment Comparison

Generate comparison table:

```powershell
python -m terrasight.reporting.comparison `
    --registry experiments\registry.csv `
    --output reports\tables\comparison_table.csv
```

Output:

```text
reports/tables/comparison_table.csv
```



# Testing

Run all tests:

```powershell
pytest tests
```

Current framework coverage:

* configuration
* reproducibility
* dataset handling
* spectral indices
* metrics
* training
* experiment tracking
* reliability
* explainability
* reporting
* band selection



# Reproducibility

The framework supports:

* fixed random seeds
* saved train/test splits
* configuration versioning
* experiment registry
* metrics persistence
* checkpoint storage
* reproducible reporting

Every experiment can be reproduced using:

```powershell
.\scripts\run_all_v1.ps1
```



# Current Development Roadmap

## Implemented

* Configuration system
* Dataset handling
* RGB pipeline
* Multispectral pipeline
* Experiment registry
* Reliability framework
* Explainability framework
* Reporting framework
* Band ablation framework

## Planned

* Reliability diagrams
* Cross-validation engine
* Statistical significance testing
* Segmentation support
* Self-supervised learning
* SatMAE integration
* Prithvi integration
* Foundation-model benchmarking
* Automated final report generation



# Scientific Focus

The project evaluates the trade-offs between:

* RGB vs Multispectral information
* Accuracy vs Reliability
* Performance vs Explainability
* Simplicity vs Model Complexity
* Classical CNNs vs Foundation Models

The ultimate goal is to establish an evidence-based understanding of when multispectral information provides measurable value for remote-sensing classification tasks.
