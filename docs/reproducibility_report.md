# Reproducibility Report
## TerraSight: EuroSAT RGB vs Multispectral Land-Cover Classification
**Author**: Toktam Khatibi, PhD  
**Project Version:** Submission Edition
# 1. Purpose
This document describes the reproducibility procedures, experimental controls, configuration management strategy, and execution workflow used in the TerraSight project.

The objective is to ensure that all reported results can be independently reproduced and audited using the provided source code, configuration files, experiment registry, datasets, and generated artifacts.

# 2. Reproducibility Philosophy
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

# 3. Computational Environment
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

# 4. Dataset Reproducibility
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

## Dataset Organization
Raw data must be placed in:
```text
data/raw/rgb/
data/raw/multispectral/
```
according to the repository structure described in the README.

## Fixed Train/Test Split
All experiments use the same stratified train/test split:
```text
80% Training
20% Testing
```

The split is generated once and reused by all experiments.

Generated files:

```text
data/splits/train.csv
data/splits/test.csv
```

This prevents variation caused by repeated random splitting.

# 5. Randomness Control
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

# 6. Configuration Management
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

# 7. Experiment Tracking

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

# 8. Controlled Experimental Design

To isolate the effect of spectral information, all experiments share:

- Identical train/test split
- Fixed random seed
- Identical backbone family (ResNet18)
- Identical evaluation methodology
- Configuration-driven execution
- Registry-based tracking

The primary experimental variable is the spectral input configuration.

## V1 Experiments

The primary comparison consists of four controlled experiments:

| Experiment | Initialization | Input |
|------------|---------------|--------|
| RGB Scratch | Random | RGB |
| RGB Pretrained | ImageNet | RGB |
| Multispectral Scratch | Random | 13-Band Multispectral |
| Multispectral Adapted | Adapted ImageNet | 13-Band Multispectral |

This design isolates the effects of transfer learning and multispectral information.

## V4 Experiments

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

# 9. Result Reproduction
## Generate Dataset Split
```bash
python -m terrasight.data.split --config configs/v1_rgb_baseline.yaml
```
## Train RGB Baseline
```bash
python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_baseline.yaml
```
## Train Multispectral Adapted Model
```bash
python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_pretrained_adapted.yaml
```
## Train Best Spectral Configuration
```bash
python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_rededge_nir_swir.yaml
```
# 10. Generated Artifacts
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
reliability/
gradcam/
robustness/
```
## Reports

```text
reports/figures/
reports/tables/
```
These outputs are stored within the corresponding experiment directory.

# 11. Reproducibility Verification Checklist
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

# 12. Robustness and Stability
To assess training stability, the best-performing spectral configuration was evaluated using multiple random seeds.

| Metric | Mean ± Std |
|----------|------------|
| Accuracy | 95.65 ± 0.18% |
| Macro-F1 | 95.55 ± 0.16% |
| Weighted-F1 | 95.65 ± 0.16% |
| Balanced Accuracy | 95.47 ± 0.07% |

The small standard deviations indicate that the reported performance is stable and not dependent on a favorable random initialization.

# 13. Known Limitations
Current limitations include:

1. Evaluation primarily uses a fixed train/test split.
2. Statistical significance testing remains limited.
3. EuroSAT may contain spatial autocorrelation between image patches.
4. Reproduction assumes access to the original EuroSAT datasets.
5. CPU and GPU execution may produce minor numerical differences.

# 14. Reproducibility Assessment
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
# 15. Reproducibility Statement
All reported results, figures, tables, and scientific conclusions were generated using configuration-controlled experiments, fixed dataset splits, deterministic execution settings, experiment tracking, and automated reporting pipelines.

The repository is designed to enable independent researchers and reviewers to reproduce the complete experimental workflow, verify reported findings, and extend the framework for future remote-sensing research.

