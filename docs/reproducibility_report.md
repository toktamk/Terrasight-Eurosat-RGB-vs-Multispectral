# Reproducibility Report
## TerraSight: EuroSAT RGB vs Multispectral Land-Cover Classification
**Author**: Toktam Khatibi, PhD  
**Project Version:** Submission Edition
# Purpose
This document describes the reproducibility procedures, experimental controls, configuration management strategy, and execution workflow used in the TerraSight project.

The objective is to ensure that all reported results can be independently reproduced and audited using the provided source code, configuration files, experiment registry, datasets, and generated artifacts.

# Reproducibility Philosophy
The project was designed according to the following principles:
1. Configuration-driven experimentation
2. Fixed dataset split generation
3. Fixed random seed
4. Version-controlled source code
5. Automated experiment tracking
6. Automated figure generation
7. Persistent storage of metrics and checkpoints
8. Separation of configuration from implementation

All reported experiments are defined through YAML configuration files rather than hard-coded parameters.

# Computational Environment
## Hardware Environment
Experiments were executed on CPU-only hardware.
| Component | Value |
|------------|---------|
| Execution Mode | CPU |
| GPU | Not Used |
| CUDA | Not Available |
| Random Seed | 42 |

The framework remains compatible with CUDA-enabled systems without requiring code modifications.

## Software Environment
| Component | Version |
|------------|------------|
| Python | 3.12+ |
| PyTorch | 2.12.0 |
| NumPy | Refer to `requirements.txt` |
| Pandas | Refer to `requirements.txt` |
| Scikit-Learn | Refer to `requirements.txt` |

The complete dependency list is provided in:

```text
requirements.txt
```

# Repository Execution Model



The project is organized as a Python package.



Core source code is located in:



```text

src/terrasight/

```



Executable workflows are exposed through Python module entry points:



```bash

python -m terrasight.<module>

```



Main executable groups:



```text

terrasight.data

terrasight.pipelines

terrasight.experiments

terrasight.reporting

terrasight.explainability

```



Core library modules (`data`, `models`, `training`, `evaluation`,

`reliability`, `explainability`) are generally imported by executable

modules rather than executed directly.



---



# Environment Setup



## Create Virtual Environment



### Linux / macOS



```bash

python -m venv .venv

source .venv/bin/activate

```



### Windows PowerShell



```powershell

python -m venv .venv

.venv\Scripts\Activate.ps1

```



## Install Dependencies



```bash

pip install -e .

pip install -r requirements.txt

```



## Verify Installation



```bash

python -c "import terrasight; print('TerraSight import successful')"

```



## Run Unit Tests



```bash

pytest

```



---



# Dataset Reproducibility
## Dataset
The experiments use the EuroSAT Sentinel-2 dataset.
| Property | Value |
|-----------|-----------|
| Classes | 10 |
| Samples | ~27,000 |
| Sensor | Sentinel-2 |
| Patch Size | 64 × 64 |
| RGB Dataset | Yes |
| Multispectral Dataset | Yes |


## Dataset Layout

### RGB Dataset

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

### Multispectral Dataset
Raw data must be placed in:

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

according to the repository structure described in the README.

## Fixed Train/Test Split
All experiments use the same stratified train/test split:
```text
80% Training
20% Testing
```

The split is generated once and reused by all experiments.

Generate the fixed stratified split:



```bash

python -m terrasight.data.split --config configs/v1_rgb_baseline.yaml

```



Expected outputs:



```text

data/splits/train.csv

data/splits/test.csv

```



The split files are reused by RGB and multispectral experiments to ensure fair comparison.
This prevents variation caused by repeated random splitting.

# Randomness Control
The project uses a fixed random seed:

```text
Seed = 42
```

The seed is applied consistently across:
- Python random module
- NumPy
- PyTorch
- Data loading
- Dataset splitting

This ensures deterministic experiment execution under the same software environment.

# Configuration Management
Every experiment is defined through a dedicated YAML configuration file.

Examples:
```text
configs/v1_rgb_baseline.yaml
configs/v1_rgb_scratch.yaml
configs/v1_multispectral_scratch.yaml
configs/v1_multispectral_pretrained_adapted.yaml
configs/v4_ablation_rgb_rededge_nir_swir.yaml
```

Configuration files define:

- Dataset paths
- Spectral band selection
- Model architecture
- Optimization settings
- Training parameters
- Evaluation settings
- Output locations

No experiment-specific settings are hard-coded in the training scripts.

# Experiment Tracking

All completed experiments are recorded in:

```text
experiments/registry.csv
```

The registry stores:

- Experiment identifier
- Timestamp
- Configuration file
- Spectral configuration
- Random seed
- Evaluation metrics
- Checkpoint location
- Output directory

This registry provides an auditable record of all reported results.

# Controlled Experimental Design

To isolate the effect of spectral information, all experiments share:

- Identical train/test split
- Fixed random seed
- Identical backbone family (ResNet18)
- Identical evaluation methodology
- Configuration-driven execution
- Registry-based tracking

The primary experimental variable is the spectral input configuration.

## V1 Baseline Experiments

The primary comparison consists of four controlled experiments:

| Experiment | Initialization | Input |
|------------|---------------|--------|
| RGB Scratch | Random | RGB |
| RGB Pretrained | ImageNet | RGB |
| Multispectral Scratch | Random | 13-Band Multispectral |
| Multispectral Adapted | Adapted ImageNet | 13-Band Multispectral |

This design isolates the effects of transfer learning and multispectral information.

## V1 Baseline Experiments



### RGB Pretrained



```bash

python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_baseline.yaml

```



### RGB Scratch



```bash

python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_scratch.yaml

```



### Multispectral Scratch



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_scratch.yaml

```



### Adapted Pretrained Multispectral



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_pretrained_adapted.yaml

```


## V4 Band-Ablation Experiments

The spectral-ablation study evaluates:

| Configuration |
|---------------|
| RGB |
| RGB + NIR |
| RGB + RedEdge + NIR |
| RGB + RedEdge + NIR + SWIR |
| Physical Surface Bands |
| Full13 |
| Full13 without B10 |

This design isolates the contribution of individual spectral groups.


### RGB Only



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb.yaml

```



### RGB + NIR



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_nir.yaml

```



### RGB + RedEdge + NIR



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_rededge_nir.yaml

```



### RGB + RedEdge + NIR + SWIR



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_rededge_nir_swir.yaml

```



### Physical-Band Groups



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_physical_bands.yaml

```



### Full 13 Bands (without B10)



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_full13_no_b10.yaml

```



### Full 13 Bands



```bash

python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_full13.yaml

```



Expected outputs:



```text

results/<experiment_id>/

├── config.yaml

├── history.json

├── metrics.json

└── best_model.pt

```



Experiment registry:



```text

experiments/registry.csv

```


# Minimal Reproduction Workflow
- Generate Dataset Split
```bash
python -m terrasight.data.split --config configs/v1_rgb_baseline.yaml
```
- Train RGB Baseline
```bash
python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_baseline.yaml
```
- Train Multispectral Adapted Model
```bash
python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_pretrained_adapted.yaml
```
- Train Best Spectral Configuration
```bash
python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_rededge_nir_swir.yaml
```
# Generated Artifacts
Each experiment automatically produces:
## Metrics
```text
metrics.json
classification_report.json
```
## Model Checkpoints

```text

best_model.pt
last_model.pt
```
## Visualizations

```text
loss_curves/
confusion_matrices/
per_class F1/
reliability/
gradcam/
robustness/
```
# Multi-Seed Reproduction



```bash

python -m terrasight.experiments.run_multiseed --config configs/v4_ablation_rgb_rededge_nir_swir.yaml --seeds 42 43 44 --continue-on-error

```


Expected outputs:



```text

experiments/generated_multiseed/

results/multiseed/

reports/tables/multiseed_summary.csv

reports/tables/multiseed_summary.json

```



---




## Reports

```text
reports/figures/
reports/tables/
```
These outputs are stored within the corresponding experiment directory.


## Predictions and Confusion Matrices

```bash
python -m terrasight.reporting.generate_confusion_matrices --results-root results --versions v1 v4 --output-figures reports/figures/confusion_matrices --output-tables reports/tables/predictions
```
Expected outputs:


```text

reports/tables/predictions/

reports/figures/confusion_matrices/

```

## Model Comparison



```bash

python -m terrasight.reporting.generate_comparison_figures

```

```bash
python -m terrasight.reporting.plot_per_class_f1
```

```bash
python -m terrasight.reporting.comparison --registry experiments/registry.csv --output reports/tables/comparison_table.csv
```

```bash

python -m terrasight.reporting.final_model_comparison

```
```bash
python -m terrasight.reporting.generate_class_level_analysis
```

```bash
python -m terrasight.reporting.generate_class_specific_importance --input reports/tables/band_occlusion/<EXPERIMENT_ID>_band_occlusion_details.csv --output-dir reports/tables/class_specific_importance --top-k 3
Expected outputs:
```

```text

reports/figures/v1_model_comparison.png

reports/figures/v4_band_ablation_comparison.png

reports/tables/final_model_comparison.csv

```

---
# Failure Cases
```bash
python -m terrasight.reporting.generate_failure_cases --probabilities reports/tables/probabilities/<EXPERIMENT_ID>_probabilities.csv --output-dir reports/figures/failure_cases --max-examples 16
```
# Reliability Analysis


```bash

python -m terrasight.reporting.generate_prediction_probabilities --results-root results --versions v1 v4 --output-dir reports/tables/probabilities

```

```bash

python -m terrasight.reporting.generate_reliability_analysis --input-dir reports/tables/probabilities --output-dir reports

```



Expected outputs:



```text

reports/tables/probabilities/

reports/tables/reliability/

reports/figures/reliability/

```



---

# Explainability Analysis



## Band Occlusion



```bash

python -m terrasight.reporting.generate_band_occlusion --run-dir results/v4/<BEST_RUN_DIR> --output-dir reports/tables/band_occlusion

```



## Grad-CAM



```bash

python -m terrasight.reporting.generate_gradcam_examples --run-dir results/v4/<BEST_RUN_DIR> --selection-mode correct_high_confidence --target-layer layer3 --num-examples 8
```

```bash
python -m terrasight.reporting.generate_gradcam_examples --run-dir results/v4/<BEST_RUN_DIR> --selection-mode high_confidence_failure --target-layer layer3 --num-examples 8
```
## Feature Space Analysis

```bash
python -m terrasight.reporting.generate_feature_space_plots --run-dir results/v4/<BEST_RUN_DIR> --method both --max-samples 3000
```

## Spectral Signatures

```bash

python -m terrasight.explainability.spectral_signatures --data-dir data/raw/multispectral --output-dir reports/figures/spectral_signatures

```

Expected outputs:

```text

reports/figures/spectral_signatures/

reports/figures/gradcam/

reports/tables/band_occlusion/

```

## Architecture Sensitivity

```bash
python -m terrasight.reporting.generate_architecture_sensitivity
```

---

## Model Profile

```bash
python -m terrasight.reporting.generate_model_profile
```
# Statistical Analysis

```bash
python -m terrasight.reporting.statistical_analysis --model-a reports/tables/probabilities/<RGB_PROBABILITIES>.csv --model-b reports/tables/probabilities/<BEST_MULTISPECTRAL_PROBABILITIES>.csv --model-a-name "<RGB_MODEL_NAME>" --model-b-name "<BEST_MULTISPECTRAL_MODEL_NAME>" --output reports/tables/statistical_tests/statistical_analysis.csv --summary reports/tables/statistical_tests/statistical_summary.md --bootstrap 1000 --seed 42
```
# Spectral Separability Analysis
```bash
python -m terrasight.reporting.generate_spectral_separability --data-dir <MULTISPECTRAL_DATASET_DIR> --tables-dir reports/tables/spectral_analysis --figures-dir reports/figures/spectral_analysis
```
# Final Validation



```bash

python -m terrasight.reporting.check_report_assets --show-discovered --strict

```



---

# Reproducibility Verification Checklist
The following items should be verified when reproducing results:

| Verification Item | Expected Outcome |
|------------------|------------------|
| Dataset split identical | Yes |
| Random seed identical | Yes |
| Configuration identical | Yes |
| Metrics reproduced within tolerance | Yes |
| Figures regenerated successfully | Yes |
| Registry entry generated | Yes |
| Checkpoints saved | Yes |

Minor numerical differences may occur across operating systems, hardware platforms, and PyTorch versions due to floating-point implementation differences.

# Robustness and Stability
To assess training stability, the best-performing spectral configuration was evaluated using multiple random seeds.

| Metric | Mean ± Std |
|----------|------------|
| Accuracy | 95.65 ± 0.18% |
| Macro-F1 | 95.55 ± 0.16% |
| Weighted-F1 | 95.65 ± 0.16% |
| Balanced Accuracy | 95.47 ± 0.07% |

The small standard deviations indicate that the reported performance is stable and not dependent on a favorable random initialization.
robustness analysis is generated using:
```bash
python -m terrasight.reporting.generate_robustness_analysis --run-dir results/v4/<BEST_RUN_DIR> --output-table-dir reports/tables/robustness --output-figure-dir reports/figures/robustness
```
# Scientific Conclusion
```bash
python -m terrasight.reporting.v4_scientific_conclusions
```
# Industrial Discussion

```bash
python -m terrasight.reporting.generate_industrial_discussion
```

# Statistical Validation
```bash
python -m terrasight.reporting.statistical_analysis --model-a reports/tables/probabilities/v4_ablation_rgb_resnet18_pretrained_adapted_seed42_probabilities.csv --model-b reports/tables/probabilities/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_probabilities.csv --model-a-name "RGB ResNet18" --model-b-name "RGB+RedEdge+NIR+SWIR ResNet18" --output reports/tables/statistical_tests/statistical_analysis.csv --summary reports/tables/statistical_tests/statistical_summary.md --bootstrap 1000 --seed 42
```

# Command Validation

All commands documented in this report were validated using:

```bash
pytest tests/test_reproducibility_commands.py
```
Result:

166 tests passed

# Known Limitations
Current limitations include:

1. Evaluation primarily uses a fixed train/test split.
2. Statistical significance testing remains limited.
3. EuroSAT may contain spatial autocorrelation between image patches.
4. Reproduction assumes access to the original EuroSAT datasets.
5. CPU and GPU execution may produce minor numerical differences.

# Reproducibility Assessment
The project satisfies the key requirements of a reproducible machine-learning workflow:

- Fixed train/test split
- Fixed random seed
- Configuration-driven experiments
- Version-controlled source code
- Experiment registry
- Saved checkpoints
- Saved metrics
- Automated report generation
- Reproducible evaluation pipeline
- Reproducible figure generation

The repository therefore supports independent verification of all reported experimental results and scientific conclusions.
# Reproducibility Statement
All reported results, figures, tables, and scientific conclusions were generated using configuration-controlled experiments, fixed dataset splits, deterministic execution settings, experiment tracking, and automated reporting pipelines.

The repository is designed to enable independent researchers and reviewers to reproduce the complete experimental workflow, verify reported findings, and extend the framework for future remote-sensing research.

# Reproducibility Conclusion



The TerraSight project is reproducible at the code, experiment, and reporting levels.



The workflow starts from dataset preparation and split generation, proceeds through configuration-driven training, and concludes with automated generation of metrics, figures, tables, robustness analyses, reliability analyses, explainability outputs, and scientific reporting artifacts.



Key reproducibility mechanisms include:



- Fixed train/test splits

- YAML configuration files

- Timestamped experiment directories

- Saved checkpoints

- Saved metrics

- Experiment registry tracking

- Automated reporting pipelines



Together, these components enable independent verification of the reported RGB-versus-multispectral experimental results.

## Reproducibility Status

The full reproducibility verification was executed before submission.

Summary:

- Unit tests: 211 passed
- Reproducibility command tests: 170 passed
- Report asset validation: READY
- Missing required assets: 0
- Overall reproducibility status: PASSED

The generated verification report is available at:

```text
docs/reproducibility_status.md
```