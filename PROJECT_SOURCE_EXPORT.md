# TerraSight Project Source Export

Generated: 2026-06-15 06:47:54

Project Root: C:\Users\DELL Precision 5550\Documents\GitHub\terrasight-eurosat-rgb-vs-multispectral

Total Files: 92

---


========================================================================================================================
FILE: v1_multispectral.yaml
PATH: configs/v1_multispectral.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_seed42
  version: v1
  description: Multispectral baseline using Sentinel-2 13-band input.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: false

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_multispectral_pretrained_adapted.yaml
PATH: configs/v1_multispectral_pretrained_adapted.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_adapted_seed42
  version: v1
  description: Multispectral model using ImageNet pretrained RGB weight adaptation.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: true

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_multispectral_scratch.yaml
PATH: configs/v1_multispectral_scratch.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_scratch_seed42
  version: v1
  description: Multispectral baseline trained from scratch.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: false

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_rgb_baseline.yaml
PATH: configs/v1_rgb_baseline.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_rgb_resnet18_seed42
  version: v1
  description: RGB baseline using Sentinel-2 visible bands.

seed: 42

data:
  dataset: eurosat
  input_type: rgb
  data_root: data/raw/rgb
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: true

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_rgb_scratch.yaml
PATH: configs/v1_rgb_scratch.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_rgb_resnet18_scratch_seed42
  version: v1
  description: RGB baseline trained from scratch.

seed: 42

data:
  dataset: eurosat
  input_type: rgb
  data_root: data/raw/rgb
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: false

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_full13.yaml
PATH: configs/v4_ablation_full13.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_full13_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using all 13 Sentinel-2 bands.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_full13_no_b10.yaml
PATH: configs/v4_ablation_full13_no_b10.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using all Sentinel-2 bands except B10 cirrus.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 12
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_physical_bands.yaml
PATH: configs/v4_ablation_physical_bands.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using physically meaningful surface bands only, excluding atmospheric bands B1, B9, and B10.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 10
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_rgb.yaml
PATH: configs/v4_ablation_rgb.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB Sentinel-2 visible bands only.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_rgb_nir.yaml
PATH: configs/v4_ablation_rgb_nir.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB plus NIR band B8.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
    - B8
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 4
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_rgb_rededge_nir.yaml
PATH: configs/v4_ablation_rgb_rededge_nir.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB, red-edge, NIR, and narrow NIR bands.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
    - B5
    - B6
    - B7
    - B8
    - B8A
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 8
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_rgb_rededge_nir_swir.yaml
PATH: configs/v4_ablation_rgb_rededge_nir_swir.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB, red-edge, NIR, narrow NIR, and SWIR bands.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 10
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: README.md
PATH: data/README.md
========================================================================================================================

```yaml

```


========================================================================================================================
FILE: environment.yml
PATH: environment.yml
========================================================================================================================

```yaml

```


========================================================================================================================
FILE: PROJECT_SOURCE_EXPORT.md
PATH: PROJECT_SOURCE_EXPORT.md
========================================================================================================================

```yaml
# TerraSight Project Source Export

Generated: 2026-06-15 06:47:54

Project Root: C:\Users\DELL Precision 5550\Documents\GitHub\terrasight-eurosat-rgb-vs-multispectral

Total Files: 92

---


========================================================================================================================
FILE: v1_multispectral.yaml
PATH: configs/v1_multispectral.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_seed42
  version: v1
  description: Multispectral baseline using Sentinel-2 13-band input.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: false

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_multispectral_pretrained_adapted.yaml
PATH: configs/v1_multispectral_pretrained_adapted.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_adapted_seed42
  version: v1
  description: Multispectral model using ImageNet pretrained RGB weight adaptation.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: true

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_multispectral_scratch.yaml
PATH: configs/v1_multispectral_scratch.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_scratch_seed42
  version: v1
  description: Multispectral baseline trained from scratch.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: false

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_rgb_baseline.yaml
PATH: configs/v1_rgb_baseline.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_rgb_resnet18_seed42
  version: v1
  description: RGB baseline using Sentinel-2 visible bands.

seed: 42

data:
  dataset: eurosat
  input_type: rgb
  data_root: data/raw/rgb
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: true

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v1_rgb_scratch.yaml
PATH: configs/v1_rgb_scratch.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_rgb_resnet18_scratch_seed42
  version: v1
  description: RGB baseline trained from scratch.

seed: 42

data:
  dataset: eurosat
  input_type: rgb
  data_root: data/raw/rgb
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: false

training:
  epochs: 50
  early_stopping:
      enabled: true
      monitor: macro_f1
      patience: 7
      min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_full13.yaml
PATH: configs/v4_ablation_full13.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_full13_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using all 13 Sentinel-2 bands.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: v4_ablation_full13_no_b10.yaml
PATH: configs/v4_ablation_full13_no_b10.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using all Sentinel-2 bands except B10 cirrus.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 12
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: pyproject.toml
PATH: pyproject.toml
========================================================================================================================

```yaml
[project]
name = "terrasight"
version = "0.1.0"
description = "EuroSAT RGB vs Multispectral Classification"
requires-python = ">=3.10"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"
```


========================================================================================================================
FILE: readme.md
PATH: readme.md
========================================================================================================================

```yaml
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

```


========================================================================================================================
FILE: final_report_template.md
PATH: reports/final_report_template.md
========================================================================================================================

```yaml
# Investigating the Value of Multispectral Information for EuroSAT Land-Use Classification: A Controlled Comparison of RGB and Sentinel-2 Multispectral Models

**Author:** Toktam Khatibi, PhD
**Repository:** TerraSight: EuroSAT RGB vs Multispectral Classification
**Date:** [Submission Date]



# Abstract

This study investigates whether multispectral Sentinel-2 imagery provides measurable benefits over standard RGB imagery for land-use and land-cover (LULC) classification using the EuroSAT benchmark dataset. A controlled experimental framework was developed to compare RGB and multispectral models under identical training conditions, enabling differences in performance to be attributed primarily to spectral information rather than architectural variations.

The project extends beyond conventional accuracy-based evaluation by incorporating reliability analysis, calibration assessment, explainability techniques, and reproducibility mechanisms. Experiments were conducted using deep learning models trained on EuroSAT imagery, and additional analyses examined spectral-band importance and model behaviour.

Results indicate that [INSERT KEY RESULT], demonstrating that [INSERT MAIN FINDING].

The project establishes a reproducible framework for evaluating multispectral computer vision systems and provides insights relevant to future remote-sensing and industrial image-analysis applications.

**Keywords:** EuroSAT, Sentinel-2, Multispectral Imaging, Remote Sensing, Deep Learning, Reliability, Explainable AI



# 1. Introduction

Land-use and land-cover (LULC) classification is a fundamental task in remote sensing with applications in environmental monitoring, agricultural assessment, urban planning, infrastructure management, and sustainability analysis. Recent advances in deep learning have enabled highly accurate image classification systems; however, the contribution of multispectral information beyond conventional RGB imagery remains an active area of investigation.

Sentinel-2 satellites provide imagery across thirteen spectral bands covering visible, near-infrared (NIR), red-edge, and short-wave infrared (SWIR) wavelengths. These additional spectral channels may contain information unavailable in RGB imagery and therefore have the potential to improve classification performance and interpretability.

The EuroSAT dataset is a widely used benchmark consisting of Sentinel-2 image patches covering ten land-use classes. Importantly, EuroSAT supports both RGB and multispectral variants, making it an ideal benchmark for evaluating the impact of spectral information.

This project addresses the following research question:

> **Does information beyond RGB imagery improve land-use classification performance, reliability, and interpretability?**

The contributions of this work are:

1. Development of a reproducible RGB baseline.
2. Controlled comparison between RGB and multispectral inputs.
3. Reliability and calibration analysis.
4. Explainability through spatial and spectral attribution methods.
5. Assessment of industrial relevance and future deployment considerations.



# 2. Methodology

## 2.1 Dataset

The EuroSAT dataset consists of Sentinel-2 image patches representing ten land-use classes.

### Table 1. Dataset Summary

| Property              | Value      |
|  | - |
| Dataset               | EuroSAT    |
| Number of Classes     | 10         |
| Total Samples         | 27,000     |
| Sensor                | Sentinel-2 |
| RGB Version           | Yes        |
| Multispectral Version | Yes        |
| Spectral Bands        | 13         |
| Image Size            | 64 × 64    |
| Train/Test Split      | 80% / 20%  |

The ten classes include:

* Annual Crop
* Forest
* Herbaceous Vegetation
* Highway
* Industrial
* Pasture
* Permanent Crop
* Residential
* River
* Sea/Lake



## 2.2 Data Preparation

Data preparation followed a reproducible workflow.

The process included:

* Stratified train/test splitting
* Fixed random seed initialization
* Tensor conversion
* Input normalization
* Metadata tracking

The train/test split was generated once and reused across all experiments to ensure fair comparison.



## 2.3 RGB Baseline

The RGB baseline used Sentinel-2 visible bands:

* B4 (Red)
* B3 (Green)
* B2 (Blue)

### Configuration

| Component      | Setting       |
| -- | - |
| Architecture   | ResNet18      |
| Input Channels | 3             |
| Optimizer      | AdamW         |
| Loss Function  | Cross Entropy |
| Learning Rate  | [INSERT]      |
| Batch Size     | [INSERT]      |
| Epochs         | [INSERT]      |

This baseline establishes a lower-bound reference performance using only information available in conventional RGB imagery.



## 2.4 Multispectral Model

The multispectral model used all available Sentinel-2 spectral bands.

### Sentinel-2 Bands

| Band | Description     |
| - |  |
| B1   | Coastal Aerosol |
| B2   | Blue            |
| B3   | Green           |
| B4   | Red             |
| B5   | Red Edge 1      |
| B6   | Red Edge 2      |
| B7   | Red Edge 3      |
| B8   | NIR             |
| B8A  | Narrow NIR      |
| B9   | Water Vapour    |
| B10  | Cirrus          |
| B11  | SWIR1           |
| B12  | SWIR2           |

The same network architecture, optimization strategy, and training protocol were used as in the RGB baseline.

> This design ensures that any observed performance differences can be attributed primarily to additional spectral information rather than architectural changes.



## 2.5 Reliability Framework

Beyond classification accuracy, model trustworthiness was evaluated through:

### Calibration

* Expected Calibration Error (ECE)
* Maximum Calibration Error (MCE)
* Brier Score

### Uncertainty

* Predictive Entropy
* Confidence Margin

### Robustness

* Gaussian Noise Perturbation
* Brightness Perturbation
* Spectral Band Dropout

### Failure Analysis

* Class confusion analysis
* Failure extraction
* Worst-performing class identification



## 2.6 Explainability Framework

Two complementary explainability approaches were employed.

### Spatial Attribution

Grad-CAM visualizations were used to identify image regions contributing to model predictions.

### Spectral Attribution

Band-occlusion analysis was used to estimate the importance of individual spectral bands.

The procedure involved:

1. Removing one spectral band.
2. Recomputing prediction confidence.
3. Measuring confidence degradation.

Higher confidence degradation indicates greater spectral importance.



# 3. Experimental Design

## Hypothesis

**H1:** Multispectral information improves classification performance relative to RGB-only imagery.



## Experiment E1 — RGB Baseline

Objective:

Evaluate performance using only visible Sentinel-2 bands.



## Experiment E2 — Full Multispectral Model

Objective:

Evaluate performance using all available Sentinel-2 bands.



## Experiment E3 — Band Ablation Analysis

Objective:

Quantify the contribution of specific spectral groups.

Band sets evaluated:

* RGB
* RGB + NIR
* RGB + NIR + Red Edge
* RGB + NIR + Red Edge + SWIR
* Full 13 Bands



## Evaluation Metrics

### Classification

* Accuracy
* Macro-F1
* Weighted-F1
* Balanced Accuracy

### Reliability

* ECE
* MCE
* Brier Score

### Explainability

* Band Importance Ranking
* Grad-CAM Visualizations



# 4. Results

## 4.1 Classification Performance

### Table 2. RGB vs Multispectral Comparison

| Model         | Accuracy | Macro-F1 | Weighted-F1 | Balanced Accuracy |
| - | -- | -- | -- | -- |
| RGB           | [INSERT] | [INSERT] | [INSERT]    | [INSERT]          |
| Multispectral | [INSERT] | [INSERT] | [INSERT]    | [INSERT]          |

### Key Finding

The multispectral model achieved a Macro-F1 improvement of **[INSERT]** relative to the RGB baseline.



## 4.2 Reliability Analysis

### Table 3. Reliability Metrics

| Model         | ECE      | MCE      | Brier Score |
| - | -- | -- | -- |
| RGB           | [INSERT] | [INSERT] | [INSERT]    |
| Multispectral | [INSERT] | [INSERT] | [INSERT]    |

Interpretation:

[INSERT DISCUSSION]



## 4.3 Band Ablation Results

### Figure 1. Band Ablation Performance

[INSERT FIGURE]

### Interpretation

[INSERT DISCUSSION]



## 4.4 Explainability Results

### Figure 2. Grad-CAM Examples

[INSERT FIGURE]

### Figure 3. Spectral Importance Ranking

[INSERT FIGURE]

Top influential bands:

1. [INSERT]
2. [INSERT]
3. [INSERT]



# 5. Discussion

## Main Findings

The experiments demonstrate that:

[INSERT MAIN FINDINGS]



## Spectral Interpretation

The strongest gains were associated with:

* NIR information
* Red-edge information
* SWIR information

These bands provide additional information related to:

* Vegetation health
* Water content
* Surface materials
* Land-cover separability



## Failure Analysis

The most common misclassifications occurred between:

* [INSERT]
* [INSERT]
* [INSERT]

Potential causes include:

* Spectral similarity
* Mixed land-cover regions
* Limited spatial resolution



## Reliability Discussion

Reliability analysis revealed:

[INSERT DISCUSSION]

Particular attention should be given to calibration quality because high classification accuracy does not necessarily imply trustworthy confidence estimates.



# 6. Industrial Relevance

Although EuroSAT differs from electrical infrastructure imagery, the methodology developed in this project reflects capabilities required for real-world industrial AI systems.

These include:

* Reproducible machine-learning pipelines
* Controlled experimentation
* Explainable predictions
* Reliability assessment
* Confidence-aware decision support

The framework can be extended to infrastructure monitoring, asset inspection, environmental management, and other industrial computer vision applications.



# 7. Limitations

Several limitations should be acknowledged.

* Single train/test split
* Limited hyperparameter optimization
* No cross-validation
* Limited foundation-model benchmarking
* EuroSAT differs from infrastructure-specific imagery

These limitations provide opportunities for future work.



# 8. Future Work

Future extensions include:

* SatMAE integration
* Prithvi foundation model evaluation
* DINO-based self-supervised learning
* Cross-validation
* Statistical significance testing
* Semantic segmentation
* Few-shot adaptation
* Deployment benchmarking



# 9. Conclusion

This study conducted a controlled comparison between RGB and Sentinel-2 multispectral imagery using the EuroSAT dataset.

The results demonstrated that **[INSERT FINAL RESULT]**.

The findings indicate that **[INSERT FINAL INTERPRETATION]**.

Beyond classification performance, the project established a reproducible framework supporting reliability analysis, explainability, experiment tracking, and future multispectral research.

The resulting methodology provides a transferable foundation for developing trustworthy image-analysis systems in industrial environments.



# References

[Insert Harvard-style references]

1. Helber, P., Bischke, B., Dengel, A. and Borth, D. (2019). EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification.
2. Cong, Y. et al. (2022). SatMAE.
3. Reed, C.J. et al. (2022). Scale-MAE.
4. Liu, F. et al. (2023). RemoteCLIP.
5. Additional references used in the literature review.

```


========================================================================================================================
FILE: requirements.txt
PATH: requirements.txt
========================================================================================================================

```yaml
pyyaml
numpy
pandas
scikit-learn
pillow
tifffile
torch
torchvision
pytest
matplotlib
```


========================================================================================================================
FILE: config.yaml
PATH: results/v1/20260613_113317_v1_rgb_resnet18_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_rgb_resnet18_seed42
  version: v1
  description: RGB baseline using Sentinel-2 visible bands.

seed: 42

data:
  dataset: eurosat
  input_type: rgb
  data_root: data/raw/rgb
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: true

training:
  epochs: 30
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v1/20260613_193704_v1_rgb_resnet18_scratch_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_rgb_resnet18_scratch_seed42
  version: v1
  description: RGB baseline trained from scratch.

seed: 42

data:
  dataset: eurosat
  input_type: rgb
  data_root: data/raw/rgb
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: false

training:
  epochs: 30
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v1/20260613_220058_v1_multispectral_resnet18_scratch_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_scratch_seed42
  version: v1
  description: Multispectral baseline trained from scratch.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: false

training:
  epochs: 30
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v1/20260614_061742_v1_multispectral_resnet18_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v1_multispectral_resnet18_adapted_seed42
  version: v1
  description: Multispectral model using ImageNet pretrained RGB weight adaptation.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: true

training:
  epochs: 30
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v4/20260614_133355_v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB plus NIR band B8.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
    - B8
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 4
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v4/20260614_145249_v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB, red-edge, NIR, and narrow NIR bands.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
    - B5
    - B6
    - B7
    - B8
    - B8A
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 8
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v4/20260614_165954_v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB, red-edge, NIR, narrow NIR, and SWIR bands.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 10
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v4/20260614_175940_v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using physically meaningful surface bands only, excluding atmospheric bands B1, B9, and B10.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 10
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v4/20260614_204858_v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using all Sentinel-2 bands except B10 cirrus.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 12
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v4/20260614_221844_v4_ablation_full13_resnet18_pretrained_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_full13_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using all 13 Sentinel-2 bands.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B1
    - B2
    - B3
    - B4
    - B5
    - B6
    - B7
    - B8
    - B8A
    - B9
    - B10
    - B11
    - B12
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 13
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: config.yaml
PATH: results/v4/20260615_052619_v4_ablation_rgb_resnet18_pretrained_adapted_seed42/config.yaml
========================================================================================================================

```yaml
experiment:
  id: v4_ablation_rgb_resnet18_pretrained_adapted_seed42
  version: v4
  description: Band ablation study using RGB Sentinel-2 visible bands only.

seed: 42

data:
  dataset: eurosat
  input_type: multispectral
  data_root: data/raw/multispectral
  split_dir: data/splits
  bands:
    - B4
    - B3
    - B2
  split:
    strategy: stratified
    train_ratio: 0.8
    test_ratio: 0.2

model:
  name: resnet18
  num_classes: 10
  input_channels: 3
  pretrained: true

training:
  epochs: 50
  early_stopping:
    enabled: true
    monitor: macro_f1
    patience: 7
    min_delta: 0.001
  batch_size: 32
  optimizer: adamw
  learning_rate: 0.0003
  weight_decay: 0.0001
  scheduler: none

evaluation:
  metrics:
    - accuracy
    - macro_f1
    - weighted_f1
    - balanced_accuracy
    - confusion_matrix

```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/data/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: band_registry.py
PATH: src/terrasight/data/band_registry.py
========================================================================================================================

```python
from __future__ import annotations

EUROSAT_CLASSES = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake",
]

CLASS_TO_INDEX = {class_name: index for index, class_name in enumerate(EUROSAT_CLASSES)}
INDEX_TO_CLASS = {index: class_name for class_name, index in CLASS_TO_INDEX.items()}

SENTINEL2_BANDS = [
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "B7",
    "B8",
    "B8A",
    "B9",
    "B10",
    "B11",
    "B12",
]

RGB_BANDS = ["B4", "B3", "B2"]

BAND_DESCRIPTIONS = {
    "B1": "Coastal aerosol",
    "B2": "Blue",
    "B3": "Green",
    "B4": "Red",
    "B5": "Red Edge 1",
    "B6": "Red Edge 2",
    "B7": "Red Edge 3",
    "B8": "NIR",
    "B8A": "Narrow NIR",
    "B9": "Water vapour",
    "B10": "Cirrus",
    "B11": "SWIR 1",
    "B12": "SWIR 2",
}
```


========================================================================================================================
FILE: dataset.py
PATH: src/terrasight/data/dataset.py
========================================================================================================================

```python
from __future__ import annotations

from pathlib import Path
from typing import Callable

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pandas as pd
from PIL import Image

from terrasight.data.band_registry import CLASS_TO_INDEX


class EuroSATRGBDataset:
    """EuroSAT RGB dataset using image paths from a split CSV."""

    def __init__(
        self,
        split_csv: str | Path,
        transform: Callable | None = None,
    ) -> None:
        self.split_csv = Path(split_csv)
        self.transform = transform

        if not self.split_csv.exists():
            raise FileNotFoundError(f"Split CSV not found: {self.split_csv}")

        self.samples = pd.read_csv(self.split_csv)

        required_columns = {"path", "label", "class_name"}
        missing = required_columns - set(self.samples.columns)
        if missing:
            raise ValueError(f"Missing columns in split CSV: {missing}")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        row = self.samples.iloc[index]
        image_path = Path(row["path"])

        image = Image.open(image_path).convert("RGB")
        label = int(row["label"])

        if self.transform is not None:
            image = self.transform(image)

        metadata = {
            "path": str(image_path),
            "class_name": row["class_name"],
        }

        return image, label, metadata


class EuroSATMSDataset:
    """EuroSAT multispectral dataset using RGB split CSV mapped to TIFF files."""

    def __init__(
        self,
        split_csv: str | Path,
        multispectral_root: str | Path,
        transform: Callable | None = None,
        source_bands: list[str] | None = None,
        selected_bands: list[str] | None = None,
    ) -> None:
        from terrasight.data.band_registry import SENTINEL2_BANDS

        self.source_bands = source_bands or SENTINEL2_BANDS
        self.selected_bands = selected_bands
        self.split_csv = Path(split_csv)
        self.multispectral_root = Path(multispectral_root)
        self.transform = transform

        if not self.split_csv.exists():
            raise FileNotFoundError(f"Split CSV not found: {self.split_csv}")

        if not self.multispectral_root.exists():
            raise FileNotFoundError(f"Multispectral root not found: {self.multispectral_root}")

        self.samples = pd.read_csv(self.split_csv)

        required_columns = {"path", "label", "class_name"}
        missing = required_columns - set(self.samples.columns)
        if missing:
            raise ValueError(f"Missing columns in split CSV: {missing}")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        import torch
        import tifffile

        row = self.samples.iloc[index]

        rgb_path = Path(row["path"])
        class_name = row["class_name"]
        tif_name = rgb_path.with_suffix(".tif").name
        tif_path = self.multispectral_root / class_name / tif_name

        if not tif_path.exists():
            raise FileNotFoundError(f"Multispectral TIFF not found: {tif_path}")

        image = tifffile.imread(tif_path)

        if image.ndim != 3:
            raise ValueError(f"Expected multispectral image with 3 dimensions, got {image.shape}")

        image = torch.tensor(image, dtype=torch.float32)

        if image.shape[-1] == 13:
            image = image.permute(2, 0, 1)

        if self.selected_bands is not None:
            from terrasight.features.band_selection import select_bands

            image = select_bands(
                image=image,
                source_bands=self.source_bands,
                selected_bands=self.selected_bands,
            )
            
        label = int(row["label"])

        if self.transform is not None:
            image = self.transform(image)

        metadata = {
            "path": str(tif_path),
            "class_name": class_name,
        }

        return image, label, metadata

def class_name_to_label(class_name: str) -> int:
    if class_name not in CLASS_TO_INDEX:
        raise ValueError(f"Unknown EuroSAT class name: {class_name}")
    return CLASS_TO_INDEX[class_name]
```


========================================================================================================================
FILE: preprocessing.py
PATH: src/terrasight/data/preprocessing.py
========================================================================================================================

```python
from __future__ import annotations

from typing import Callable

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
from torchvision import transforms


RGB_MEAN = [0.485, 0.456, 0.406]
RGB_STD = [0.229, 0.224, 0.225]


def get_rgb_transform(train: bool = False) -> Callable:
    """Return RGB preprocessing transform."""

    transform_steps = []

    if train:
        transform_steps.extend(
            [
                transforms.RandomHorizontalFlip(),
                transforms.RandomVerticalFlip(),
            ]
        )

    transform_steps.extend(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=RGB_MEAN, std=RGB_STD),
        ]
    )

    return transforms.Compose(transform_steps)


def normalize_multispectral_tensor(
    image: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Channel-wise normalize a multispectral tensor.

    Expected shape:
        [C, H, W]
    """

    if image.ndim != 3:
        raise ValueError(f"Expected tensor shape [C, H, W], got {tuple(image.shape)}")

    mean = image.mean(dim=(1, 2), keepdim=True)
    std = image.std(dim=(1, 2), keepdim=True)

    return (image - mean) / (std + eps)


def minmax_scale_tensor(
    image: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Scale tensor values to [0, 1]."""

    min_value = image.amin(dim=(-2, -1), keepdim=True)
    max_value = image.amax(dim=(-2, -1), keepdim=True)

    return (image - min_value) / (max_value - min_value + eps)
```


========================================================================================================================
FILE: split.py
PATH: src/terrasight/data/split.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
from pathlib import Path

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pandas as pd
from sklearn.model_selection import train_test_split

from terrasight.data.band_registry import CLASS_TO_INDEX, EUROSAT_CLASSES
from terrasight.utils.config import load_config


VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def find_samples(data_root: str | Path) -> pd.DataFrame:
    """Find EuroSAT samples in class-subfolder format."""

    root = Path(data_root)

    if not root.exists():
        raise FileNotFoundError(
            f"Data root not found: {root}. "
            "Place EuroSAT files under data/raw or update data.data_root in the config."
        )

    records: list[dict] = []

    for class_name in EUROSAT_CLASSES:
        class_dir = root / class_name

        if not class_dir.exists():
            continue

        for file_path in class_dir.rglob("*"):
            if file_path.suffix.lower() in VALID_IMAGE_EXTENSIONS:
                records.append(
                    {
                        "path": str(file_path),
                        "class_name": class_name,
                        "label": CLASS_TO_INDEX[class_name],
                    }
                )

    if not records:
        raise ValueError(
            f"No image files found under {root}. Expected class folders such as "
            f"{root / EUROSAT_CLASSES[0]}"
        )

    return pd.DataFrame(records)


def create_stratified_split(
    samples: pd.DataFrame,
    train_ratio: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create stratified train/test split."""

    train_df, test_df = train_test_split(
        samples,
        train_size=train_ratio,
        random_state=seed,
        stratify=samples["label"],
        shuffle=True,
    )

    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def save_split_files(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    split_dir: str | Path,
) -> None:
    split_path = Path(split_dir)
    split_path.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(split_path / "train.csv", index=False)
    test_df.to_csv(split_path / "test.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create EuroSAT stratified train/test split.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)

    data_root = config["data"]["data_root"]
    split_dir = config["data"]["split_dir"]
    train_ratio = float(config["data"]["split"]["train_ratio"])
    seed = int(config["seed"])

    samples = find_samples(data_root)
    train_df, test_df = create_stratified_split(samples, train_ratio, seed)
    save_split_files(train_df, test_df, split_dir)

    print("Split creation complete")
    print(f"Total samples: {len(samples)}")
    print(f"Train samples: {len(train_df)}")
    print(f"Test samples: {len(test_df)}")
    print(f"Split directory: {split_dir}")


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/evaluation/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: confusion.py
PATH: src/terrasight/evaluation/confusion.py
========================================================================================================================

```python
from __future__ import annotations

from pathlib import Path

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


def compute_confusion_matrix(
    y_true: list[int] | np.ndarray,
    y_pred: list[int] | np.ndarray,
) -> np.ndarray:
    """Compute confusion matrix."""

    return confusion_matrix(y_true, y_pred)


def save_confusion_matrix_plot(
    y_true: list[int] | np.ndarray,
    y_pred: list[int] | np.ndarray,
    class_names: list[str],
    output_path: str | Path,
    normalize: str | None = None,
) -> None:
    """Save confusion matrix figure."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cm = confusion_matrix(y_true, y_pred, normalize=normalize)

    fig, ax = plt.subplots(figsize=(10, 10))
    display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    display.plot(ax=ax, xticks_rotation=45, colorbar=True)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
```


========================================================================================================================
FILE: metrics.py
PATH: src/terrasight/evaluation/metrics.py
========================================================================================================================

```python
from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)


def compute_classification_metrics(
    y_true: list[int] | np.ndarray,
    y_pred: list[int] | np.ndarray,
) -> dict[str, float]:
    """Compute core classification metrics."""

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_precision": float(precision_score(y_true, y_pred, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
    }


def compute_classwise_report(
    y_true: list[int] | np.ndarray,
    y_pred: list[int] | np.ndarray,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    """Return class-wise precision, recall, and F1."""

    return classification_report(
        y_true,
        y_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )
```


========================================================================================================================
FILE: experiment_tracker.py
PATH: src/terrasight/experiments/experiment_tracker.py
========================================================================================================================

```python
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import pandas as pd

from terrasight.experiments.registry import (
    create_registry_if_missing,
    load_registry,
    save_registry,
)


def register_experiment(
    config: dict,
    metrics_file: str | Path,
    run_dir: str | Path,
    registry_path: str | Path = "experiments/registry.csv",
) -> None:

    create_registry_if_missing(registry_path)

    metrics_file = Path(metrics_file)

    with metrics_file.open("r", encoding="utf-8") as file:
        metrics = json.load(file)

    row = {
        "timestamp": datetime.now().isoformat(),
        "experiment_id": config["experiment"]["id"],
        "version": config["experiment"]["version"],
        "input_type": config["data"]["input_type"],
        "model": config["model"]["name"],
        "input_channels": config["model"]["input_channels"],
        "bands": ",".join(config["data"]["bands"]),
        "epochs": config["training"]["epochs"],
        "accuracy": metrics.get("accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "weighted_f1": metrics.get("weighted_f1"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "run_directory": str(run_dir),
    }

    registry = load_registry(registry_path)

    new_row = pd.DataFrame([row])

    if registry.empty:
        registry = new_row
    else:
        registry = pd.concat(
            [registry, new_row],
            ignore_index=True,
        )

    save_registry(registry, registry_path)
```


========================================================================================================================
FILE: registry.py
PATH: src/terrasight/experiments/registry.py
========================================================================================================================

```python
from __future__ import annotations

from pathlib import Path
import pandas as pd


REGISTRY_COLUMNS = [
    "timestamp",
    "experiment_id",
    "version",
    "input_type",
    "model",
    "input_channels",
    "bands",
    "epochs",
    "accuracy",
    "macro_f1",
    "weighted_f1",
    "balanced_accuracy",
    "run_directory",
]


def create_registry_if_missing(
    registry_path: str | Path,
) -> None:
    registry_path = Path(registry_path)

    if registry_path.exists():
        return

    df = pd.DataFrame(columns=REGISTRY_COLUMNS)
    df.to_csv(registry_path, index=False)


def load_registry(
    registry_path: str | Path,
) -> pd.DataFrame:
    create_registry_if_missing(registry_path)
    return pd.read_csv(registry_path)


def save_registry(
    dataframe: pd.DataFrame,
    registry_path: str | Path,
) -> None:
    dataframe.to_csv(registry_path, index=False)
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/explainability/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: explainability_report.py
PATH: src/terrasight/explainability/explainability_report.py
========================================================================================================================

```python
from __future__ import annotations

import json
from pathlib import Path


def save_band_attribution(
    scores: dict[str, float],
    output_path: str | Path,
) -> None:
    """Save band attribution scores as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(scores, file, indent=2)


def build_explainability_summary(
    predicted_class: str,
    target_class: str,
    band_scores: dict[str, float],
) -> dict:
    """Create compact explainability summary."""

    ranked = sorted(band_scores.items(), key=lambda item: item[1], reverse=True)

    return {
        "predicted_class": predicted_class,
        "target_class": target_class,
        "top_bands": [
            {"band": band, "score": float(score)}
            for band, score in ranked[:5]
        ],
    }
```


========================================================================================================================
FILE: gradcam.py
PATH: src/terrasight/explainability/gradcam.py
========================================================================================================================

```python
from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn


class GradCAM:
    """Minimal Grad-CAM implementation for CNN models."""

    def __init__(self, model: nn.Module, target_layer: nn.Module) -> None:
        self.model = model
        self.target_layer = target_layer
        self.activations: torch.Tensor | None = None
        self.gradients: torch.Tensor | None = None

        self.forward_hook = target_layer.register_forward_hook(self._save_activations)
        self.backward_hook = target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, inputs, output) -> None:
        self.activations = output.detach()

    def _save_gradients(self, module, grad_input, grad_output) -> None:
        self.gradients = grad_output[0].detach()

    def generate(
        self,
        image: torch.Tensor,
        class_index: int | None = None,
    ) -> torch.Tensor:
        """Generate Grad-CAM heatmap.

        Args:
            image: Tensor with shape [1, C, H, W].
            class_index: Target class. If None, uses predicted class.

        Returns:
            Heatmap tensor with shape [H, W].
        """

        self.model.eval()
        self.model.zero_grad(set_to_none=True)

        logits = self.model(image)

        if class_index is None:
            class_index = int(torch.argmax(logits, dim=1).item())

        score = logits[:, class_index].sum()
        score.backward()

        if self.activations is None or self.gradients is None:
            raise RuntimeError("Grad-CAM hooks did not capture activations/gradients.")

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True)
        cam = F.relu(cam)

        cam = F.interpolate(
            cam,
            size=image.shape[-2:],
            mode="bilinear",
            align_corners=False,
        )

        cam = cam.squeeze()

        cam_min = cam.min()
        cam_max = cam.max()

        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)

        return cam.detach().cpu()

    def close(self) -> None:
        """Remove hooks."""

        self.forward_hook.remove()
        self.backward_hook.remove()


def get_resnet_target_layer(model: nn.Module) -> nn.Module:
    """Return default Grad-CAM target layer for torchvision ResNet."""

    if not hasattr(model, "layer4"):
        raise ValueError("Model does not have layer4. Provide target layer manually.")

    return model.layer4[-1]
```


========================================================================================================================
FILE: spectral_attribution.py
PATH: src/terrasight/explainability/spectral_attribution.py
========================================================================================================================

```python
from __future__ import annotations

from typing import Callable

import torch
from torch import nn


@torch.no_grad()
def band_occlusion_scores(
    model: nn.Module,
    image: torch.Tensor,
    target_class: int,
    band_names: list[str],
    score_fn: Callable[[torch.Tensor, int], float] | None = None,
) -> dict[str, float]:
    """Compute band-occlusion attribution scores.

    Args:
        model: Classification model.
        image: Input tensor with shape [1, C, H, W].
        target_class: Class index to explain.
        band_names: Names of input bands.
        score_fn: Optional scoring function.

    Returns:
        Mapping from band name to drop in target-class probability.
    """

    if image.ndim != 4:
        raise ValueError(f"Expected image shape [1, C, H, W], got {tuple(image.shape)}")

    if image.shape[1] != len(band_names):
        raise ValueError(
            f"Number of bands ({image.shape[1]}) does not match band_names ({len(band_names)})."
        )

    model.eval()

    def default_score_fn(logits: torch.Tensor, cls: int) -> float:
        probs = torch.softmax(logits, dim=1)
        return float(probs[0, cls].item())

    score_function = score_fn or default_score_fn

    baseline_logits = model(image)
    baseline_score = score_function(baseline_logits, target_class)

    scores: dict[str, float] = {}

    for band_index, band_name in enumerate(band_names):
        occluded = image.clone()
        occluded[:, band_index, :, :] = 0.0

        logits = model(occluded)
        occluded_score = score_function(logits, target_class)

        scores[band_name] = float(baseline_score - occluded_score)

    return scores


def rank_band_importance(scores: dict[str, float]) -> list[tuple[str, float]]:
    """Rank bands by descending occlusion score."""

    return sorted(scores.items(), key=lambda item: item[1], reverse=True)
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/features/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: band_selection.py
PATH: src/terrasight/features/band_selection.py
========================================================================================================================

```python
from __future__ import annotations

import torch


def select_bands(
    image: torch.Tensor,
    source_bands: list[str],
    selected_bands: list[str],
) -> torch.Tensor:
    """Select specific bands from multispectral tensor.

    Args:
        image: Tensor with shape [C, H, W].
        source_bands: Band names corresponding to image channels.
        selected_bands: Band names to extract.

    Returns:
        Tensor with selected channels.
    """

    if image.ndim != 3:
        raise ValueError(f"Expected image shape [C, H, W], got {tuple(image.shape)}")

    missing = [band for band in selected_bands if band not in source_bands]

    if missing:
        raise ValueError(f"Selected bands missing from source bands: {missing}")

    band_to_index = {band: index for index, band in enumerate(source_bands)}
    indices = [band_to_index[band] for band in selected_bands]

    return image[indices, :, :]
```


========================================================================================================================
FILE: band_sets.py
PATH: src/terrasight/features/band_sets.py
========================================================================================================================

```python
from __future__ import annotations

from terrasight.data.band_registry import SENTINEL2_BANDS


BAND_SETS: dict[str, list[str]] = {
    "rgb": ["B4", "B3", "B2"],
    "rgb_nir": ["B4", "B3", "B2", "B8"],
    "rgb_rededge_nir": ["B4", "B3", "B2", "B5", "B6", "B7", "B8"],
    "rgb_rededge_nir_swir": ["B4", "B3", "B2", "B5", "B6", "B7", "B8", "B11", "B12"],
    "full_13": SENTINEL2_BANDS,
}


def get_band_set(name: str) -> list[str]:
    """Return predefined Sentinel-2 band set."""

    if name not in BAND_SETS:
        raise ValueError(f"Unknown band set: {name}. Available: {list(BAND_SETS)}")

    return BAND_SETS[name]


def list_band_sets() -> list[str]:
    """Return available band-set names."""

    return list(BAND_SETS.keys())


def validate_band_set(bands: list[str]) -> None:
    """Validate selected bands."""

    invalid = [band for band in bands if band not in SENTINEL2_BANDS]

    if invalid:
        raise ValueError(f"Invalid Sentinel-2 bands: {invalid}")
```


========================================================================================================================
FILE: spectral_indices.py
PATH: src/terrasight/features/spectral_indices.py
========================================================================================================================

```python
from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch


def _safe_normalized_difference(
    numerator_a: torch.Tensor,
    numerator_b: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute safe normalized difference."""

    return (numerator_a - numerator_b) / (numerator_a + numerator_b + eps)


def compute_ndvi(
    nir: torch.Tensor,
    red: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute NDVI.

    NDVI = (NIR - Red) / (NIR + Red)
    """

    return _safe_normalized_difference(nir, red, eps)


def compute_ndwi(
    green: torch.Tensor,
    nir: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute McFeeters-style NDWI.

    NDWI = (Green - NIR) / (Green + NIR)
    """

    return _safe_normalized_difference(green, nir, eps)


def compute_ndbi(
    swir: torch.Tensor,
    nir: torch.Tensor,
    eps: float = 1e-6,
) -> torch.Tensor:
    """Compute NDBI.

    NDBI = (SWIR - NIR) / (SWIR + NIR)
    """

    return _safe_normalized_difference(swir, nir, eps)


def append_indices_to_multispectral(
    image: torch.Tensor,
    band_names: list[str],
) -> torch.Tensor:
    """Append NDVI, NDWI, and NDBI to a multispectral tensor.

    Expected image shape:
        [C, H, W]

    Required bands:
        B3 = Green
        B4 = Red
        B8 = NIR
        B11 = SWIR1
    """

    if image.ndim != 3:
        raise ValueError(f"Expected image shape [C, H, W], got {tuple(image.shape)}")

    required_bands = ["B3", "B4", "B8", "B11"]
    missing = [band for band in required_bands if band not in band_names]

    if missing:
        raise ValueError(f"Missing required bands for spectral indices: {missing}")

    band_to_index = {band: index for index, band in enumerate(band_names)}

    green = image[band_to_index["B3"]]
    red = image[band_to_index["B4"]]
    nir = image[band_to_index["B8"]]
    swir = image[band_to_index["B11"]]

    ndvi = compute_ndvi(nir=nir, red=red).unsqueeze(0)
    ndwi = compute_ndwi(green=green, nir=nir).unsqueeze(0)
    ndbi = compute_ndbi(swir=swir, nir=nir).unsqueeze(0)

    return torch.cat([image, ndvi, ndwi, ndbi], dim=0)
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/models/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: backbone_factory.py
PATH: src/terrasight/models/backbone_factory.py
========================================================================================================================

```python
from __future__ import annotations

import torch.nn as nn
from torchvision import models

from terrasight.models.model_utils import replace_classifier, replace_first_conv


SUPPORTED_BACKBONES = {
    "resnet18",
    "resnet34",
    "resnet50",
}


def _get_resnet_weights(name: str, pretrained: bool):
    if not pretrained:
        return None

    if name == "resnet18":
        return models.ResNet18_Weights.DEFAULT

    if name == "resnet34":
        return models.ResNet34_Weights.DEFAULT

    if name == "resnet50":
        return models.ResNet50_Weights.DEFAULT

    return None


def build_resnet_backbone(
    name: str,
    input_channels: int,
    num_classes: int,
    pretrained: bool = False,
) -> nn.Module:
    """Build a ResNet model with configurable input channels.

    If pretrained=True and input_channels > 3, ImageNet RGB weights are loaded
    first, then the first convolution is expanded to the requested number of
    channels using RGB-weight transfer.
    """

    if name not in SUPPORTED_BACKBONES:
        raise ValueError(f"Unsupported backbone: {name}. Supported: {SUPPORTED_BACKBONES}")

    weights = _get_resnet_weights(name=name, pretrained=pretrained)

    if name == "resnet18":
        model = models.resnet18(weights=weights)
    elif name == "resnet34":
        model = models.resnet34(weights=weights)
    else:
        model = models.resnet50(weights=weights)

    if input_channels != 3:
        model = replace_first_conv(
            model=model,
            input_channels=input_channels,
            preserve_pretrained=pretrained,
        )

    model = replace_classifier(model, num_classes=num_classes)

    return model


def build_model(
    name: str,
    input_channels: int,
    num_classes: int,
    pretrained: bool = False,
) -> nn.Module:
    """Generic model factory."""

    if name.startswith("resnet"):
        return build_resnet_backbone(
            name=name,
            input_channels=input_channels,
            num_classes=num_classes,
            pretrained=pretrained,
        )

    raise ValueError(f"Unsupported model name: {name}")
```


========================================================================================================================
FILE: model_utils.py
PATH: src/terrasight/models/model_utils.py
========================================================================================================================

```python
from __future__ import annotations

import torch
import torch.nn as nn


def replace_first_conv(
    model: nn.Module,
    input_channels: int,
    preserve_pretrained: bool = True,
) -> nn.Module:
    """Replace ResNet first conv and optionally transfer pretrained RGB weights."""

    if not hasattr(model, "conv1"):
        raise ValueError("Model does not have attribute 'conv1'.")

    old_conv = model.conv1

    new_conv = nn.Conv2d(
        in_channels=input_channels,
        out_channels=old_conv.out_channels,
        kernel_size=old_conv.kernel_size,
        stride=old_conv.stride,
        padding=old_conv.padding,
        bias=old_conv.bias is not None,
    )

    if preserve_pretrained:
        with torch.no_grad():
            if input_channels >= 3:
                new_conv.weight[:, :3, :, :] = old_conv.weight[:, :3, :, :]

                if input_channels > 3:
                    mean_weight = old_conv.weight.mean(dim=1, keepdim=True)
                    for channel in range(3, input_channels):
                        new_conv.weight[:, channel : channel + 1, :, :] = mean_weight
            else:
                new_conv.weight[:, :, :, :] = old_conv.weight[:, :input_channels, :, :]

            if old_conv.bias is not None and new_conv.bias is not None:
                new_conv.bias.copy_(old_conv.bias)

    model.conv1 = new_conv
    return model


def replace_classifier(
    model: nn.Module,
    num_classes: int,
) -> nn.Module:
    """Replace final classifier layer of a ResNet-style model."""

    if not hasattr(model, "fc"):
        raise ValueError("Model does not have attribute 'fc'.")

    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    return model
```


========================================================================================================================
FILE: multispectral_model.py
PATH: src/terrasight/models/multispectral_model.py
========================================================================================================================

```python
from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch.nn as nn

from terrasight.models.backbone_factory import build_model


def build_multispectral_model(
    model_name: str = "resnet18",
    input_channels: int = 13,
    num_classes: int = 10,
    pretrained: bool = False,
) -> nn.Module:
    """Build multispectral classification model."""

    return build_model(
        name=model_name,
        input_channels=input_channels,
        num_classes=num_classes,
        pretrained=pretrained,
    )
```


========================================================================================================================
FILE: rgb_model.py
PATH: src/terrasight/models/rgb_model.py
========================================================================================================================

```python
from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch.nn as nn

from terrasight.models.backbone_factory import build_model


def build_rgb_model(
    model_name: str = "resnet18",
    num_classes: int = 10,
    pretrained: bool = False,
) -> nn.Module:
    """Build RGB classification model."""

    return build_model(
        name=model_name,
        input_channels=3,
        num_classes=num_classes,
        pretrained=pretrained,
    )
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/pipelines/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: evaluate_checkpoint.py
PATH: src/terrasight/pipelines/evaluate_checkpoint.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from terrasight.data.dataset import EuroSATMSDataset
from terrasight.data.preprocessing import normalize_multispectral_tensor
from terrasight.evaluation.metrics import compute_classification_metrics
from terrasight.models.multispectral_model import build_multispectral_model
from terrasight.training.losses import build_loss
from terrasight.utils.config import load_config


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict:
    model.eval()

    total_loss = 0.0
    y_true = []
    y_pred = []

    for images, labels, _metadata in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        logits = model(images)
        loss = criterion(logits, labels)

        predictions = torch.argmax(logits, dim=1)

        total_loss += loss.item() * images.size(0)
        y_true.extend(labels.cpu().tolist())
        y_pred.extend(predictions.cpu().tolist())

    metrics = compute_classification_metrics(y_true, y_pred)
    metrics["loss"] = total_loss / len(dataloader.dataset)

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    config_path = run_dir / "config.yaml"
    checkpoint_path = run_dir / "best_model.pt"

    config = load_config(config_path)

    selected_bands = config["data"].get("bands")
    source_bands = config["data"].get("source_bands")

    test_csv = Path(config["data"]["split_dir"]) / "test.csv"
    ms_root = Path(config["data"]["data_root"])

    test_dataset = EuroSATMSDataset(
        split_csv=test_csv,
        multispectral_root=ms_root,
        transform=normalize_multispectral_tensor,
        source_bands=source_bands,
        selected_bands=selected_bands,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=int(config["training"]["batch_size"]),
        shuffle=False,
        num_workers=0,
    )

    model = build_multispectral_model(
        model_name=config["model"]["name"],
        input_channels=int(config["model"]["input_channels"]),
        num_classes=int(config["model"]["num_classes"]),
        pretrained=False,
    )

    device = get_device()
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model = model.to(device)

    criterion = build_loss("cross_entropy")

    metrics = evaluate_model(
        model=model,
        dataloader=test_loader,
        criterion=criterion,
        device=device,
    )

    output_path = run_dir / "checkpoint_metrics.json"
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print(json.dumps(metrics, indent=2))
    print(f"Saved metrics to: {output_path}")


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: train_multispectral.py
PATH: src/terrasight/pipelines/train_multispectral.py
========================================================================================================================

```python
from __future__ import annotations

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import argparse
import json
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from terrasight.data.dataset import EuroSATMSDataset
from terrasight.data.preprocessing import normalize_multispectral_tensor
from terrasight.evaluation.metrics import compute_classification_metrics
from terrasight.models.multispectral_model import build_multispectral_model
from terrasight.training.losses import build_loss
from terrasight.training.optimizer_factory import build_optimizer
from terrasight.training.scheduler_factory import build_scheduler
from terrasight.utils.config import load_config
from terrasight.utils.run_setup import setup_run


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict[str, Any]:
    model.eval()

    total_loss = 0.0
    y_true: list[int] = []
    y_pred: list[int] = []

    for images, labels, _metadata in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        logits = model(images)
        loss = criterion(logits, labels)
        predictions = torch.argmax(logits, dim=1)

        total_loss += loss.item() * images.size(0)
        y_true.extend(labels.cpu().tolist())
        y_pred.extend(predictions.cpu().tolist())

    metrics = compute_classification_metrics(y_true, y_pred)
    metrics["loss"] = total_loss / len(dataloader.dataset)
    metrics["y_true"] = y_true
    metrics["y_pred"] = y_pred
    return metrics


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    model.train()

    total_loss = 0.0

    for images, labels, _metadata in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad(set_to_none=True)

        logits = model(images)
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)

    return total_loss / len(dataloader.dataset)


def validate_multispectral_config(config: dict[str, Any]) -> None:
    if config["data"]["input_type"] != "multispectral":
        raise ValueError("Expected data.input_type='multispectral'.")

    bands = config["data"].get("bands")

    if bands is None:
        expected_channels = 13
    else:
        expected_channels = len(bands)

    actual_channels = int(config["model"]["input_channels"])

    if actual_channels != expected_channels:
        raise ValueError(
            f"Expected model.input_channels={expected_channels}, "
            f"but got model.input_channels={actual_channels}. "
            "model.input_channels must match the number of selected data.bands."
        )


def train_multispectral_from_config(config_path: str | Path) -> Path:
    config = load_config(config_path)
    validate_multispectral_config(config)

    run_dir = setup_run(config_path)

    train_csv = Path(config["data"]["split_dir"]) / "train.csv"
    test_csv = Path(config["data"]["split_dir"]) / "test.csv"
    ms_root = Path(config["data"]["data_root"])

    selected_bands = config["data"].get("bands")
    source_bands = config["data"].get("source_bands")

    train_dataset = EuroSATMSDataset(
        split_csv=train_csv,
        multispectral_root=ms_root,
        transform=normalize_multispectral_tensor,
        source_bands=source_bands,
        selected_bands=selected_bands,
    )

    test_dataset = EuroSATMSDataset(
        split_csv=test_csv,
        multispectral_root=ms_root,
        transform=normalize_multispectral_tensor,
        source_bands=source_bands,
        selected_bands=selected_bands,
    )

    batch_size = int(config["training"]["batch_size"])

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
    )

    model = build_multispectral_model(
        model_name=config["model"]["name"],
        input_channels=int(config["model"]["input_channels"]),
        num_classes=int(config["model"]["num_classes"]),
        pretrained=bool(config["model"].get("pretrained", False)),
    )

    device = get_device()
    model = model.to(device)

    criterion = build_loss("cross_entropy")

    optimizer = build_optimizer(
        model=model,
        name=config["training"]["optimizer"],
        learning_rate=float(config["training"]["learning_rate"]),
        weight_decay=float(config["training"].get("weight_decay", 0.0)),
    )

    scheduler = build_scheduler(
        optimizer=optimizer,
        name=config["training"].get("scheduler"),
        epochs=int(config["training"]["epochs"]),
    )

    epochs = int(config["training"]["epochs"])

    early_cfg = config["training"].get("early_stopping", {})
    early_enabled = bool(early_cfg.get("enabled", False))
    monitor = early_cfg.get("monitor", "macro_f1")
    patience = int(early_cfg.get("patience", 7))
    min_delta = float(early_cfg.get("min_delta", 0.0))

    if monitor not in {
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
        "macro_precision",
        "macro_recall",
    }:
        raise ValueError(
            f"Unsupported early-stopping monitor: {monitor}. "
            "Use one of: accuracy, macro_f1, weighted_f1, "
            "balanced_accuracy, macro_precision, macro_recall."
        )

    best_score = -float("inf")
    best_macro_f1 = -1.0
    best_metrics: dict[str, Any] = {}
    history: list[dict[str, Any]] = []
    epochs_without_improvement = 0

    for epoch in range(1, epochs + 1):
        train_loss = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
        )

        metrics = evaluate_model(
            model=model,
            dataloader=test_loader,
            criterion=criterion,
            device=device,
        )

        metrics["epoch"] = epoch
        metrics["train_loss"] = train_loss
        history.append(metrics)

        print(
            f"Epoch {epoch}/{epochs} , "
            f"train_loss={train_loss:.4f} , "
            f"val_loss={metrics['loss']:.4f} , "
            f"accuracy={metrics['accuracy']:.4f} , "
            f"macro_f1={metrics['macro_f1']:.4f}"
        )

        if scheduler is not None:
            if scheduler.__class__.__name__ == "ReduceLROnPlateau":
                scheduler.step(metrics["loss"])
            else:
                scheduler.step()

        current_score = float(metrics[monitor])

        if current_score > best_score + min_delta:
            best_score = current_score
            best_macro_f1 = float(metrics["macro_f1"])
            best_metrics = metrics
            epochs_without_improvement = 0

            torch.save(
                model.state_dict(),
                run_dir / "best_model.pt",
            )

            print(f"New best {monitor}: {current_score:.4f}")

        else:
            epochs_without_improvement += 1

            print(
                f"No improvement in {monitor} "
                f"for {epochs_without_improvement}/{patience} epochs."
            )

        if early_enabled and epochs_without_improvement >= patience:
            print(
                f"\nEarly stopping triggered at epoch {epoch}. "
                f"No improvement in {monitor} for {patience} consecutive epochs."
            )
            break

    with (run_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(best_metrics, file, indent=2)

    with (run_dir / "history.json").open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)

    from terrasight.experiments.experiment_tracker import register_experiment

    register_experiment(
        config=config,
        metrics_file=run_dir / "metrics.json",
        run_dir=run_dir,
    )

    print("Multispectral training complete")
    print(f"Best macro-F1: {best_macro_f1:.4f}")
    print(f"Run directory: {run_dir}")

    from terrasight.experiments.experiment_tracker import register_experiment

    register_experiment(
        config=config,
        metrics_file=run_dir / "metrics.json",
        run_dir=run_dir,
    )

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TerraSight multispectral pipeline.")
    parser.add_argument(
        "--config",
        default="configs/v1_multispectral.yaml",
        help="Path to multispectral config file.",
    )

    args = parser.parse_args()

    train_multispectral_from_config(args.config)


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: train_rgb.py
PATH: src/terrasight/pipelines/train_rgb.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
from pathlib import Path

from src.terrasight.training.trainer import train_from_config
from src.terrasight.utils.config import load_config


EXPECTED_RGB_BANDS = ["B4", "B3", "B2"]


def validate_rgb_config(config_path: str | Path) -> None:
    """Validate that the config is suitable for RGB baseline training."""

    config = load_config(config_path)

    input_type = config["data"].get("input_type")
    if input_type != "rgb":
        raise ValueError(f"Expected data.input_type='rgb', got '{input_type}'.")

    input_channels = int(config["model"].get("input_channels"))
    if input_channels != 3:
        raise ValueError(f"Expected model.input_channels=3, got {input_channels}.")

    bands = config["data"].get("bands")
    if bands != EXPECTED_RGB_BANDS:
        raise ValueError(f"Expected RGB bands {EXPECTED_RGB_BANDS}, got {bands}.")


def run_rgb_pipeline(config_path: str | Path) -> Path:
    """Run the RGB baseline training pipeline."""

    validate_rgb_config(config_path)

    run_dir = train_from_config(config_path)

    print("RGB baseline pipeline complete")
    print(f"Outputs saved to: {run_dir}")

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TerraSight RGB baseline pipeline.")
    parser.add_argument(
        "--config",
        default="configs/v1_rgb_baseline.yaml",
        help="Path to RGB baseline config file.",
    )
    args = parser.parse_args()

    run_rgb_pipeline(args.config)


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/reliability/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: calibration.py
PATH: src/terrasight/reliability/calibration.py
========================================================================================================================

```python
from __future__ import annotations

import numpy as np
import torch


def softmax_confidences(logits: torch.Tensor) -> tuple[np.ndarray, np.ndarray]:
    """Return predicted classes and confidence scores from logits."""

    probabilities = torch.softmax(logits, dim=1)
    confidences, predictions = torch.max(probabilities, dim=1)

    return predictions.cpu().numpy(), confidences.cpu().numpy()


def expected_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10,
) -> float:
    """Compute Expected Calibration Error."""

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for lower, upper in zip(bin_boundaries[:-1], bin_boundaries[1:]):
        in_bin = (confidences > lower) & (confidences <= upper)

        if not np.any(in_bin):
            continue

        bin_accuracy = np.mean(y_true[in_bin] == y_pred[in_bin])
        bin_confidence = np.mean(confidences[in_bin])
        bin_weight = np.mean(in_bin)

        ece += bin_weight * abs(bin_accuracy - bin_confidence)

    return float(ece)


def maximum_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10,
) -> float:
    """Compute Maximum Calibration Error."""

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    errors = []

    for lower, upper in zip(bin_boundaries[:-1], bin_boundaries[1:]):
        in_bin = (confidences > lower) & (confidences <= upper)

        if not np.any(in_bin):
            continue

        bin_accuracy = np.mean(y_true[in_bin] == y_pred[in_bin])
        bin_confidence = np.mean(confidences[in_bin])
        errors.append(abs(bin_accuracy - bin_confidence))

    if not errors:
        return 0.0

    return float(max(errors))


def brier_score(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    num_classes: int,
) -> float:
    """Compute multiclass Brier score."""

    one_hot = np.eye(num_classes)[y_true]
    score = np.mean(np.sum((probabilities - one_hot) ** 2, axis=1))

    return float(score)
```


========================================================================================================================
FILE: failure_analysis.py
PATH: src/terrasight/reliability/failure_analysis.py
========================================================================================================================

```python
from __future__ import annotations

from collections import Counter

import numpy as np


def extract_failure_indices(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> list[int]:
    """Return indices where prediction is incorrect."""

    return np.where(y_true != y_pred)[0].tolist()


def confusion_pairs(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: list[str],
    top_k: int = 10,
) -> list[dict[str, object]]:
    """Return most frequent true/predicted failure pairs."""

    failures = y_true != y_pred
    pairs = list(zip(y_true[failures], y_pred[failures]))

    counter = Counter(pairs)

    output = []
    for (true_label, pred_label), count in counter.most_common(top_k):
        output.append(
            {
                "true_class": class_names[int(true_label)],
                "predicted_class": class_names[int(pred_label)],
                "count": int(count),
            }
        )

    return output


def worst_classes_by_f1(
    classwise_report: dict,
    top_k: int = 5,
) -> list[dict[str, object]]:
    """Extract worst classes from a sklearn classification_report dictionary."""

    rows = []

    for class_name, values in classwise_report.items():
        if not isinstance(values, dict):
            continue

        if "f1-score" not in values:
            continue

        rows.append(
            {
                "class_name": class_name,
                "f1_score": float(values["f1-score"]),
                "precision": float(values["precision"]),
                "recall": float(values["recall"]),
                "support": int(values["support"]),
            }
        )

    rows.sort(key=lambda item: item["f1_score"])

    return rows[:top_k]
```


========================================================================================================================
FILE: reliability_report.py
PATH: src/terrasight/reliability/reliability_report.py
========================================================================================================================

```python
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from terrasight.reliability.calibration import (
    expected_calibration_error,
    maximum_calibration_error,
)
from terrasight.reliability.failure_analysis import (
    confusion_pairs,
    extract_failure_indices,
)


def build_reliability_summary(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    class_names: list[str],
) -> dict:
    """Build reliability summary dictionary."""

    failures = extract_failure_indices(y_true, y_pred)

    return {
        "ece": expected_calibration_error(y_true, y_pred, confidences),
        "mce": maximum_calibration_error(y_true, y_pred, confidences),
        "num_samples": int(len(y_true)),
        "num_failures": int(len(failures)),
        "failure_rate": float(len(failures) / len(y_true)),
        "top_confusion_pairs": confusion_pairs(
            y_true=y_true,
            y_pred=y_pred,
            class_names=class_names,
        ),
    }


def save_reliability_summary(
    summary: dict,
    output_path: str | Path,
) -> None:
    """Save reliability summary as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
```


========================================================================================================================
FILE: robustness.py
PATH: src/terrasight/reliability/robustness.py
========================================================================================================================

```python
from __future__ import annotations

import torch


def add_gaussian_noise(
    images: torch.Tensor,
    std: float = 0.05,
) -> torch.Tensor:
    """Add Gaussian noise to image tensor."""

    noise = torch.randn_like(images) * std
    return images + noise


def apply_brightness_shift(
    images: torch.Tensor,
    shift: float = 0.1,
) -> torch.Tensor:
    """Apply additive brightness shift."""

    return images + shift


def dropout_bands(
    images: torch.Tensor,
    band_indices: list[int],
) -> torch.Tensor:
    """Zero selected spectral bands.

    Expected image shape:
        [B, C, H, W]
    """

    output = images.clone()

    for band_index in band_indices:
        output[:, band_index, :, :] = 0.0

    return output


def compute_degradation(
    clean_metric: float,
    perturbed_metric: float,
) -> float:
    """Compute metric degradation."""

    return float(clean_metric - perturbed_metric)
```


========================================================================================================================
FILE: uncertainty.py
PATH: src/terrasight/reliability/uncertainty.py
========================================================================================================================

```python
from __future__ import annotations

import numpy as np
import torch


def predictive_entropy(probabilities: torch.Tensor, eps: float = 1e-8) -> np.ndarray:
    """Compute predictive entropy from class probabilities."""

    entropy = -torch.sum(probabilities * torch.log(probabilities + eps), dim=1)
    return entropy.cpu().numpy()


def confidence_margin(probabilities: torch.Tensor) -> np.ndarray:
    """Compute difference between top-1 and top-2 probabilities."""

    top2 = torch.topk(probabilities, k=2, dim=1).values
    margin = top2[:, 0] - top2[:, 1]

    return margin.cpu().numpy()


def confidence_error_flags(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    high_confidence_threshold: float = 0.9,
) -> dict[str, int]:
    """Count high-confidence correct and incorrect predictions."""

    correct = y_true == y_pred
    high_confidence = confidences >= high_confidence_threshold

    return {
        "high_confidence_correct": int(np.sum(high_confidence & correct)),
        "high_confidence_errors": int(np.sum(high_confidence & ~correct)),
        "low_confidence_correct": int(np.sum(~high_confidence & correct)),
        "low_confidence_errors": int(np.sum(~high_confidence & ~correct)),
    }
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/reporting/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: comparison.py
PATH: src/terrasight/reporting/comparison.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_METRICS = [
    "accuracy",
    "macro_f1",
    "weighted_f1",
    "balanced_accuracy",
]


def load_registry(
    registry_path: str | Path = "experiments/registry.csv",
) -> pd.DataFrame:
    """Load experiment registry."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")

    return pd.read_csv(registry_path)


def build_comparison_table(
    registry: pd.DataFrame,
    metrics: list[str] | None = None,
) -> pd.DataFrame:
    """Build compact experiment comparison table from registry."""

    metrics = metrics or DEFAULT_METRICS

    required_columns = [
        "experiment_id",
        "version",
        "input_type",
        "model",
        "input_channels",
        "bands",
        "epochs",
        "run_directory",
        *metrics,
    ]

    missing = [column for column in required_columns if column not in registry.columns]

    if missing:
        raise ValueError(f"Missing required registry columns: {missing}")

    comparison = registry[required_columns].copy()

    sort_columns = [metric for metric in ["macro_f1", "accuracy"] if metric in comparison.columns]

    if sort_columns:
        comparison = comparison.sort_values(
            by=sort_columns,
            ascending=False,
        )

    return comparison.reset_index(drop=True)


def add_rgb_vs_ms_delta(
    comparison: pd.DataFrame,
    rgb_experiment_id: str,
    ms_experiment_id: str,
    metric: str = "macro_f1",
) -> pd.DataFrame:
    """Add absolute delta between one RGB and one multispectral experiment."""

    if metric not in comparison.columns:
        raise ValueError(f"Metric not found in comparison table: {metric}")

    rgb_rows = comparison[comparison["experiment_id"] == rgb_experiment_id]
    ms_rows = comparison[comparison["experiment_id"] == ms_experiment_id]

    if rgb_rows.empty:
        raise ValueError(f"RGB experiment not found: {rgb_experiment_id}")

    if ms_rows.empty:
        raise ValueError(f"Multispectral experiment not found: {ms_experiment_id}")

    rgb_score = float(rgb_rows.iloc[0][metric])
    ms_score = float(ms_rows.iloc[0][metric])
    delta = ms_score - rgb_score

    output = comparison.copy()
    output[f"delta_vs_rgb_{metric}"] = None

    output.loc[
        output["experiment_id"] == ms_experiment_id,
        f"delta_vs_rgb_{metric}",
    ] = delta

    return output


def save_comparison_table(
    comparison: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """Save comparison table."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    comparison.to_csv(output_path, index=False)


def generate_comparison_table(
    registry_path: str | Path = "experiments/registry.csv",
    output_path: str | Path = "reports/tables/comparison_table.csv",
) -> pd.DataFrame:
    """Generate and save comparison table from registry."""

    registry = load_registry(registry_path)
    comparison = build_comparison_table(registry)
    save_comparison_table(comparison, output_path)

    print("Comparison table generated")
    print(f"Output: {output_path}")

    return comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TerraSight experiment comparison table.")
    parser.add_argument(
        "--registry",
        default="experiments/registry.csv",
        help="Path to experiment registry CSV.",
    )
    parser.add_argument(
        "--output",
        default="reports/tables/comparison_table.csv",
        help="Output comparison table path.",
    )

    args = parser.parse_args()

    generate_comparison_table(
        registry_path=args.registry,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: figures.py
PATH: src/terrasight/reporting/figures.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    confusion_matrix,
)

from terrasight.data.band_registry import EUROSAT_CLASSES


def load_json(path: str | Path) -> Any:
    """Load a JSON file."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def ensure_output_dir(output_dir: str | Path) -> Path:
    """Create output directory if it does not exist."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path


def make_safe_name(name: str) -> str:
    """Create a filesystem-safe output prefix."""

    return (
        name.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )


def load_history(run_dir: str | Path) -> pd.DataFrame | None:
    """Load training history if available."""

    history_path = Path(run_dir) / "history.json"

    if not history_path.exists():
        print(
            f"WARNING: history.json not found in {run_dir}. "
            "Skipping training-curve figures."
        )
        return None

    history = pd.DataFrame(load_json(history_path))

    required_columns = {
        "epoch",
        "train_loss",
        "loss",
        "macro_f1",
    }

    missing = required_columns - set(history.columns)

    if missing:
        print(
            f"WARNING: history.json in {run_dir} is missing columns "
            f"{sorted(missing)}. Skipping training-curve figures."
        )
        return None

    return history


def load_predictions(
    run_dir: str | Path,
) -> tuple[list[int], list[int]] | None:
    """Load prediction labels if predictions.json exists."""

    predictions_path = Path(run_dir) / "predictions.json"

    if not predictions_path.exists():
        print(
            f"WARNING: predictions.json not found in {run_dir}. "
            "Skipping confusion matrix and classwise report."
        )
        return None

    predictions = load_json(predictions_path)

    if "y_true" not in predictions or "y_pred" not in predictions:
        print(
            f"WARNING: Invalid predictions.json in {run_dir}. "
            "Expected keys: 'y_true' and 'y_pred'."
        )
        return None

    return predictions["y_true"], predictions["y_pred"]


def save_loss_curve(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> Path | None:
    """Save train/validation loss curve if history exists."""

    history = load_history(run_dir)

    if history is None:
        return None

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{make_safe_name(name)}_loss_curve.png"

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        history["epoch"],
        history["train_loss"],
        marker="o",
        label="Train loss",
    )

    ax.plot(
        history["epoch"],
        history["loss"],
        marker="o",
        label="Validation loss",
    )

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_title(f"Training and validation loss: {name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_macro_f1_curve(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> Path | None:
    """Save validation macro-F1 curve if history exists."""

    history = load_history(run_dir)

    if history is None:
        return None

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{make_safe_name(name)}_macro_f1_curve.png"

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        history["epoch"],
        history["macro_f1"],
        marker="o",
        label="Validation macro-F1",
    )

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Macro-F1")
    ax.set_title(f"Validation macro-F1: {name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_confusion_matrix(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
    normalize: str | None = None,
) -> Path | None:
    """Save confusion matrix if predictions exist."""

    predictions = load_predictions(run_dir)

    if predictions is None:
        return None

    y_true, y_pred = predictions

    output_dir = ensure_output_dir(output_dir)

    suffix = (
        "normalized_confusion_matrix"
        if normalize
        else "confusion_matrix"
    )

    output_path = output_dir / f"{make_safe_name(name)}_{suffix}.png"

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=list(range(len(EUROSAT_CLASSES))),
        normalize=normalize,
    )

    fig, ax = plt.subplots(figsize=(10, 10))

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=EUROSAT_CLASSES,
    )

    display.plot(
        ax=ax,
        xticks_rotation=45,
        colorbar=True,
        values_format=".2f" if normalize else "d",
    )

    ax.set_title(f"Confusion matrix: {name}")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_classwise_report(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> Path | None:
    """Save class-wise precision/recall/F1 report if predictions exist."""

    predictions = load_predictions(run_dir)

    if predictions is None:
        return None

    y_true, y_pred = predictions

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{make_safe_name(name)}_classwise_report.csv"

    report = classification_report(
        y_true,
        y_pred,
        labels=list(range(len(EUROSAT_CLASSES))),
        target_names=EUROSAT_CLASSES,
        output_dict=True,
        zero_division=0,
    )

    pd.DataFrame(report).T.to_csv(output_path)

    return output_path


def save_registry_comparison(
    registry_path: str | Path,
    output_dir: str | Path,
) -> Path | None:
    """Save model-performance comparison chart from registry.csv."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        print(
            f"WARNING: Registry file not found: {registry_path}. "
            "Skipping registry comparison."
        )
        return None

    registry = pd.read_csv(registry_path)

    required_columns = {
        "experiment_id",
        "accuracy",
        "macro_f1",
        "balanced_accuracy",
    }

    missing = required_columns - set(registry.columns)

    if missing:
        print(
            f"WARNING: Registry missing columns {sorted(missing)}. "
            "Skipping registry comparison."
        )
        return None

    df = registry[
        [
            "experiment_id",
            "accuracy",
            "macro_f1",
            "balanced_accuracy",
        ]
    ].dropna()

    if df.empty:
        print(
            "WARNING: Registry has no rows with accuracy, macro_f1, "
            "and balanced_accuracy. Skipping registry comparison."
        )
        return None

    df = df.drop_duplicates(
        subset=["experiment_id"],
        keep="last",
    )

    df = df.set_index("experiment_id")

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / "model_performance_comparison.png"

    fig, ax = plt.subplots(figsize=(12, 6))

    df.plot(
        kind="bar",
        ax=ax,
    )

    ax.set_ylabel("Score")
    ax.set_ylim(0.85, 1.0)
    ax.set_title("Model performance comparison")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(title="Metric")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def generate_run_figures(
    run_dir: str | Path,
    output_dir: str | Path,
    name: str,
) -> dict[str, Path | None]:
    """Generate all available figures for a single run."""

    outputs: dict[str, Path | None] = {
        "loss_curve": save_loss_curve(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
        "macro_f1_curve": save_macro_f1_curve(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
        "confusion_matrix": save_confusion_matrix(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
            normalize=None,
        ),
        "normalized_confusion_matrix": save_confusion_matrix(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
            normalize="true",
        ),
        "classwise_report": save_classwise_report(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
    }

    return outputs


def print_generated_outputs(
    outputs: dict[str, Path | None],
) -> None:
    """Print generated artifact paths."""

    print("\nGenerated files:")

    for output_name, output_path in outputs.items():
        if output_path is not None:
            print(f"  {output_name}: {output_path}")


def save_version_model_comparison(
    registry_path: str | Path,
    version: str,
    output_dir: str | Path,
    metrics: list[str] | None = None,
    min_y: float | None = None,
    max_y: float = 1.0,
) -> Path | None:
    """Save a trimmed-axis comparison chart for all models of one version."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        print(f"WARNING: Registry file not found: {registry_path}")
        return None

    registry = pd.read_csv(registry_path)

    if metrics is None:
        metrics = [
            "accuracy",
            "macro_f1",
            "weighted_f1",
            "balanced_accuracy",
        ]

    required_columns = {
        "experiment_id",
        "version",
        *metrics,
    }

    missing = required_columns - set(registry.columns)

    if missing:
        print(
            f"WARNING: registry.csv is missing required columns: {sorted(missing)}"
        )
        return None

    version_df = registry[
        registry["version"].astype(str).str.lower() == version.lower()
    ]

    if version_df.empty:
        print(f"WARNING: No experiments found for version: {version}")
        return None

    version_df = version_df.drop_duplicates(
        subset=["experiment_id"],
        keep="last",
    )

    plot_df = version_df[
        ["experiment_id", *metrics]
    ].dropna(subset=metrics)

    if plot_df.empty:
        print(f"WARNING: No valid metric rows found for version: {version}")
        return None

    plot_df = plot_df.set_index("experiment_id")

    metric_values = plot_df[metrics].to_numpy().ravel()
    observed_min = float(metric_values.min())

    if min_y is None:
        min_y = max(0.0, observed_min - 0.01)

    output_dir = ensure_output_dir(output_dir)
    output_path = output_dir / f"{version.lower()}_model_comparison.png"

    fig, ax = plt.subplots(figsize=(14, 7))

    plot_df[metrics].plot(
        kind="bar",
        ax=ax,
    )

    ax.set_xlabel("Experiment")
    ax.set_ylabel("Score")
    ax.set_ylim(min_y, max_y)
    ax.set_title(f"Trimmed model comparison for {version.upper()}")
    ax.tick_params(axis="x", rotation=90)
    ax.legend(title="Metric")

    ax.axhline(
        y=plot_df["accuracy"].max(),
        linestyle="--",
        linewidth=1,
        alpha=0.5,
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TerraSight report figures for a single run."
    )

    parser.add_argument(
        "--run-dir",
        help="Path to one experiment run directory.",
    )

    parser.add_argument(
        "--name",
        default=None,
        help="Optional output name prefix. If omitted, run folder name is used.",
    )

    parser.add_argument(
        "--registry",
        default="experiments/registry.csv",
        help="Optional path to experiment registry CSV.",
    )

    parser.add_argument(
        "--output-dir",
        default="reports/figures",
        help="Directory where figures and classwise reports are saved.",
    )

    parser.add_argument(
        "--version",
        default=None,
        help="Version to compare (v1, v2, v3, v4, v5).",
    )

    args = parser.parse_args()
    print(args)
    if args.output_dir is not None:
        output_dir = ensure_output_dir(args.output_dir)
    else:
        output_dir = "reports/figures"

    if args.version is not None:
        save_version_model_comparison(
            registry_path=args.registry,
            version=args.version,
            output_dir=output_dir,
        )
    if args.run_dir is not None:
        run_dir = Path(args.run_dir)

        if not run_dir.exists():
            raise FileNotFoundError(f"Run directory not found: {run_dir}")

        experiment_name = args.name or run_dir.name

        outputs = generate_run_figures(
            run_dir=run_dir,
            output_dir=output_dir,
            name=experiment_name,
        )

        registry_plot = save_registry_comparison(
            registry_path=args.registry,
            output_dir=output_dir,
        )

        if registry_plot is not None:
            outputs["registry_comparison"] = registry_plot

        print("\nReport-figure generation complete.")
        print(f"Run directory: {run_dir}")
        print(f"Output directory: {output_dir}")

        print_generated_outputs(outputs)


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: figuresnew.py
PATH: src/terrasight/reporting/figuresnew.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix

from terrasight.data.band_registry import EUROSAT_CLASSES


def load_json(path: str | Path) -> Any:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def ensure_output_dir(output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def safe_label(label: str) -> str:
    return (
        label.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )


def load_history(run_dir: str | Path) -> pd.DataFrame | None:
    history_path = Path(run_dir) / "history.json"

    if not history_path.exists():
        print(f"WARNING: history.json not found in {run_dir}.")
        return None

    history = pd.DataFrame(load_json(history_path))
    required = {"epoch", "train_loss", "loss", "macro_f1"}
    missing = required - set(history.columns)

    if missing:
        print(f"WARNING: history.json in {run_dir} missing {sorted(missing)}.")
        return None

    return history


def load_predictions(run_dir: str | Path) -> tuple[list[int], list[int]] | None:
    predictions_path = Path(run_dir) / "predictions.json"

    if not predictions_path.exists():
        print(f"WARNING: predictions.json not found in {run_dir}.")
        return None

    predictions = load_json(predictions_path)

    if "y_true" not in predictions or "y_pred" not in predictions:
        print(f"WARNING: Invalid predictions.json in {run_dir}.")
        return None

    return predictions["y_true"], predictions["y_pred"]


def save_combined_loss_curve(
    runs: list[tuple[Path, str]],
    output_dir: Path,
) -> Path | None:
    output_path = output_dir / "combined_loss_curves.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    plotted = False

    for run_dir, label in runs:
        history = load_history(run_dir)
        if history is None:
            continue

        ax.plot(
            history["epoch"],
            history["train_loss"],
            linestyle="-",
            marker="o",
            label=f"{label} train",
        )
        ax.plot(
            history["epoch"],
            history["loss"],
            linestyle="--",
            marker="o",
            label=f"{label} validation",
        )
        plotted = True

    if not plotted:
        plt.close(fig)
        return None

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_title("Training and validation loss comparison")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_combined_macro_f1_curve(
    runs: list[tuple[Path, str]],
    output_dir: Path,
) -> Path | None:
    output_path = output_dir / "combined_macro_f1_curves.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    plotted = False

    for run_dir, label in runs:
        history = load_history(run_dir)
        if history is None:
            continue

        ax.plot(
            history["epoch"],
            history["macro_f1"],
            marker="o",
            label=label,
        )
        plotted = True

    if not plotted:
        plt.close(fig)
        return None

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Macro-F1")
    ax.set_title("Validation macro-F1 comparison")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_combined_confusion_matrices(
    runs: list[tuple[Path, str]],
    output_dir: Path,
    normalize: str | None = None,
) -> Path | None:
    valid_runs: list[tuple[list[int], list[int], str]] = []

    for run_dir, label in runs:
        predictions = load_predictions(run_dir)
        if predictions is None:
            continue
        y_true, y_pred = predictions
        valid_runs.append((y_true, y_pred, label))

    if not valid_runs:
        return None

    suffix = "normalized_confusion_matrices" if normalize else "confusion_matrices"
    output_path = output_dir / f"combined_{suffix}.png"

    n = len(valid_runs)
    fig, axes = plt.subplots(
        1,
        n,
        figsize=(8 * n, 7),
        squeeze=False,
    )

    for ax, (y_true, y_pred, label) in zip(axes[0], valid_runs):
        cm = confusion_matrix(
            y_true,
            y_pred,
            labels=list(range(len(EUROSAT_CLASSES))),
            normalize=normalize,
        )

        display = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=EUROSAT_CLASSES,
        )

        display.plot(
            ax=ax,
            xticks_rotation=45,
            colorbar=False,
            values_format=".2f" if normalize else "d",
        )

        ax.set_title(label)

    fig.suptitle(
        "Normalized confusion matrices" if normalize else "Confusion matrices",
        fontsize=14,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_classwise_reports(
    runs: list[tuple[Path, str]],
    output_dir: Path,
) -> dict[str, Path]:
    reports: dict[str, Path] = {}

    for run_dir, label in runs:
        predictions = load_predictions(run_dir)
        if predictions is None:
            continue

        y_true, y_pred = predictions
        safe = safe_label(label)
        output_path = output_dir / f"{safe}_classwise_report.csv"

        report = classification_report(
            y_true,
            y_pred,
            labels=list(range(len(EUROSAT_CLASSES))),
            target_names=EUROSAT_CLASSES,
            output_dict=True,
            zero_division=0,
        )

        pd.DataFrame(report).T.to_csv(output_path)
        reports[label] = output_path

    return reports


def save_combined_per_class_f1(
    reports: dict[str, Path],
    output_dir: Path,
) -> Path | None:
    if not reports:
        return None

    data: dict[str, list[float]] = {}

    for label, report_path in reports.items():
        df = pd.read_csv(report_path, index_col=0)

        if "f1-score" not in df.columns:
            continue

        data[label] = [
            float(df.loc[class_name, "f1-score"])
            for class_name in EUROSAT_CLASSES
            if class_name in df.index
        ]

    if not data:
        return None

    comparison = pd.DataFrame(data, index=EUROSAT_CLASSES)
    output_path = output_dir / "combined_per_class_f1.png"

    fig, ax = plt.subplots(figsize=(14, 7))
    comparison.plot(kind="bar", ax=ax)

    ax.set_xlabel("Class")
    ax.set_ylabel("F1-score")
    ax.set_ylim(0.75, 1.0)
    ax.set_title("Per-class F1 comparison")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Experiment", fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def save_registry_comparison(
    registry_path: str | Path,
    output_dir: Path,
) -> Path | None:
    registry_path = Path(registry_path)

    if not registry_path.exists():
        print(f"WARNING: Registry file not found: {registry_path}.")
        return None

    registry = pd.read_csv(registry_path)

    required = {
        "experiment_id",
        "accuracy",
        "macro_f1",
        "balanced_accuracy",
    }

    missing = required - set(registry.columns)
    if missing:
        print(f"WARNING: Registry missing columns {sorted(missing)}.")
        return None

    df = registry[
        ["experiment_id", "accuracy", "macro_f1", "balanced_accuracy"]
    ].dropna()

    if df.empty:
        return None

    df = df.drop_duplicates(subset=["experiment_id"], keep="last")
    df = df.set_index("experiment_id")

    output_path = output_dir / "registry_model_performance_comparison.png"

    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(kind="bar", ax=ax)

    ax.set_ylabel("Score")
    ax.set_ylim(0.85, 1.0)
    ax.set_title("Model performance comparison from registry")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(title="Metric")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path


def print_outputs(outputs: dict[str, Path | None]) -> None:
    for name, path in outputs.items():
        if path is not None:
            print(f"Generated {name}: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TerraSight figures for one experiment run."
    )

    parser.add_argument(
        "--run-dir",
        required=True,
        help="Path to one experiment run directory.",
    )

    parser.add_argument(
        "--name",
        default=None,
        help="Optional figure prefix. If omitted, run folder name is used.",
    )

    parser.add_argument(
        "--registry",
        default="experiments/registry.csv",
        help="Path to experiment registry CSV.",
    )

    parser.add_argument(
        "--output-dir",
        default="reports/figures",
        help="Directory where figures are saved.",
    )

    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    output_dir = ensure_output_dir(args.output_dir)

    name = args.name or run_dir.name

    outputs: dict[str, Path | None] = {
        "loss_curve": save_loss_curve(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
        "macro_f1_curve": save_macro_f1_curve(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
        "confusion_matrix": save_confusion_matrix(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
            normalize=None,
        ),
        "normalized_confusion_matrix": save_confusion_matrix(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
            normalize="true",
        ),
        "classwise_report": save_classwise_report(
            run_dir=run_dir,
            output_dir=output_dir,
            name=name,
        ),
        "registry_comparison": save_registry_comparison(
            registry_path=args.registry,
            output_dir=output_dir,
        ),
    }

    print("Report-figure generation complete.")
    print(f"Run directory: {run_dir}")
    print(f"Output directory: {output_dir}")
    print_generated_outputs(outputs)

if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: report_assets.py
PATH: src/terrasight/reporting/report_assets.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from terrasight.reporting.figures import save_metric_bar_chart, save_training_curve
from terrasight.reporting.tables import (
    load_metrics,
    metrics_to_table,
    save_table,
)


def generate_single_run_assets(
    run_dir: str | Path,
    experiment_name: str | None = None,
    output_dir: str | Path = "reports",
) -> None:
    """Generate report-ready assets for a single run."""

    run_dir = Path(run_dir)
    output_dir = Path(output_dir)

    metrics_path = run_dir / "metrics.json"
    history_path = run_dir / "history.json"

    if experiment_name is None:
        experiment_name = run_dir.name

    metrics = load_metrics(metrics_path)
    table = metrics_to_table(metrics, experiment_name=experiment_name)

    save_table(
        table=table,
        output_path=output_dir / "tables" / f"{experiment_name}_metrics.csv",
    )

    save_metric_bar_chart(
        table=table,
        metric="macro_f1",
        output_path=output_dir / "figures" / f"{experiment_name}_macro_f1.png",
    )

    if history_path.exists():
        with history_path.open("r", encoding="utf-8") as file:
            history = json.load(file)

        save_training_curve(
            history=history,
            output_path=output_dir / "figures" / f"{experiment_name}_training_curve.png",
            metric="macro_f1",
        )

    print("Report assets generated")
    print(f"Output directory: {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TerraSight report assets.")
    parser.add_argument("--run-dir", required=True, help="Path to run directory.")
    parser.add_argument("--experiment-name", default=None, help="Optional display name.")
    parser.add_argument("--output-dir", default="reports", help="Output report directory.")
    args = parser.parse_args()

    generate_single_run_assets(
        run_dir=args.run_dir,
        experiment_name=args.experiment_name,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: tables.py
PATH: src/terrasight/reporting/tables.py
========================================================================================================================

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def load_metrics(metrics_path: str | Path) -> dict[str, Any]:
    """Load metrics JSON file."""

    metrics_path = Path(metrics_path)

    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {metrics_path}")

    with metrics_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def metrics_to_table(
    metrics: dict[str, Any],
    experiment_name: str,
) -> pd.DataFrame:
    """Convert metrics dictionary to one-row table."""

    row = {
        "experiment": experiment_name,
        "accuracy": metrics.get("accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "weighted_f1": metrics.get("weighted_f1"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "loss": metrics.get("loss"),
    }

    return pd.DataFrame([row])


def build_comparison_table(
    rows: list[pd.DataFrame],
) -> pd.DataFrame:
    """Build experiment comparison table."""

    if not rows:
        raise ValueError("No rows provided for comparison table.")

    return pd.concat(rows, ignore_index=True)


def save_table(
    table: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """Save table as CSV."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table.to_csv(output_path, index=False)


def load_registry_table(
    registry_path: str | Path = "experiments/registry.csv",
) -> pd.DataFrame:
    """Load experiment registry CSV."""

    registry_path = Path(registry_path)

    if not registry_path.exists():
        raise FileNotFoundError(f"Registry not found: {registry_path}")

    return pd.read_csv(registry_path)
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/training/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: losses.py
PATH: src/terrasight/training/losses.py
========================================================================================================================

```python
from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch.nn as nn


def build_loss(name: str = "cross_entropy") -> nn.Module:
    """Build loss function."""

    name = name.lower()

    if name in {"cross_entropy", "ce"}:
        return nn.CrossEntropyLoss()

    raise ValueError(f"Unsupported loss function: {name}")
```


========================================================================================================================
FILE: optimizer_factory.py
PATH: src/terrasight/training/optimizer_factory.py
========================================================================================================================

```python
from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn


def build_optimizer(
    model: nn.Module,
    name: str = "adamw",
    learning_rate: float = 3e-4,
    weight_decay: float = 1e-4,
) -> torch.optim.Optimizer:
    """Build optimizer."""

    name = name.lower()

    if name == "adamw":
        return torch.optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )

    if name == "adam":
        return torch.optim.Adam(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )

    if name == "sgd":
        return torch.optim.SGD(
            model.parameters(),
            lr=learning_rate,
            momentum=0.9,
            weight_decay=weight_decay,
        )

    raise ValueError(f"Unsupported optimizer: {name}")
```


========================================================================================================================
FILE: scheduler_factory.py
PATH: src/terrasight/training/scheduler_factory.py
========================================================================================================================

```python
from __future__ import annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch


def build_scheduler(
    optimizer: torch.optim.Optimizer,
    name: str | None = None,
    epochs: int = 30,
):
    """Build learning-rate scheduler.

    Returns None if no scheduler is requested.
    """

    if name is None:
        return None

    name = name.lower()

    if name in {"none", "null"}:
        return None

    if name == "cosine":
        return torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=epochs,
        )

    if name == "plateau":
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode="min",
            patience=3,
            factor=0.5,
        )

    raise ValueError(f"Unsupported scheduler: {name}")
```


========================================================================================================================
FILE: trainer.py
PATH: src/terrasight/training/trainer.py
========================================================================================================================

```python
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.terrasight.data.preprocessing import get_rgb_transform
from src.terrasight.data.dataset import EuroSATRGBDataset
from src.terrasight.evaluation.metrics import compute_classification_metrics
from src.terrasight.models.rgb_model import build_rgb_model
from src.terrasight.training.losses import build_loss
from src.terrasight.training.optimizer_factory import build_optimizer
from src.terrasight.training.scheduler_factory import build_scheduler
from src.terrasight.utils.config import load_config
from src.terrasight.utils.run_setup import setup_run


def get_device() -> torch.device:
    """Return available compute device."""

    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    """Train model for one epoch."""

    model.train()
    total_loss = 0.0

    for images, labels, _metadata in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad(set_to_none=True)

        logits = model(images)
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)

    return total_loss / len(dataloader.dataset)


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict[str, Any]:
    """Evaluate model."""

    model.eval()
    total_loss = 0.0
    y_true: list[int] = []
    y_pred: list[int] = []

    for images, labels, _metadata in dataloader:
        images = images.to(device)
        labels = labels.to(device)

        logits = model(images)
        loss = criterion(logits, labels)

        predictions = torch.argmax(logits, dim=1)

        total_loss += loss.item() * images.size(0)
        y_true.extend(labels.cpu().tolist())
        y_pred.extend(predictions.cpu().tolist())

    metrics = compute_classification_metrics(y_true, y_pred)
    metrics["loss"] = total_loss / len(dataloader.dataset)
    metrics["y_true"] = y_true
    metrics["y_pred"] = y_pred
    return metrics


def save_checkpoint(
    model: nn.Module,
    run_dir: Path,
    filename: str = "checkpoint.pt",
) -> None:
    """Save model checkpoint."""

    checkpoint_path = run_dir / filename
    torch.save(model.state_dict(), checkpoint_path)


from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_metrics(
    metrics: dict[str, Any],
    run_dir: Path,
) -> None:
    """
    Save evaluation metrics and predictions.

    Outputs:
        metrics.json
            Contains scalar metrics only.

        predictions.json
            Contains ground-truth and predicted labels
            for downstream analysis and visualisation.
    """

    run_dir.mkdir(parents=True, exist_ok=True)

    # Save only serializable scalar metrics
    metrics_for_json = {
        key: value
        for key, value in metrics.items()
        if key not in {"y_true", "y_pred"}
    }

    metrics_path = run_dir / "metrics.json"

    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump(metrics_for_json, file, indent=2)

    # Save predictions separately if available
    if "y_true" in metrics and "y_pred" in metrics:

        predictions = {
            "y_true": metrics["y_true"],
            "y_pred": metrics["y_pred"],
        }

        predictions_path = run_dir / "predictions.json"

        with predictions_path.open("w", encoding="utf-8") as file:
            json.dump(predictions, file, indent=2)


def train_from_config(config_path: str | Path) -> Path:
    """Train RGB baseline from config.

    This trainer currently supports RGB only.
    Multispectral training will be added in the next pipeline part.
    """

    config = load_config(config_path)
    run_dir = setup_run(config_path)

    if config["data"]["input_type"] != "rgb":
        raise ValueError(
            "Part 7 trainer currently supports RGB configs only. "
            "Multispectral support will be added in the multispectral pipeline."
        )

    train_csv = Path(config["data"]["split_dir"]) / "train.csv"
    test_csv = Path(config["data"]["split_dir"]) / "test.csv"

    train_dataset = EuroSATRGBDataset(
        split_csv=train_csv,
        transform=get_rgb_transform(train=True),
    )
    test_dataset = EuroSATRGBDataset(
        split_csv=test_csv,
        transform=get_rgb_transform(train=False),
    )

    batch_size = int(config["training"]["batch_size"])

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
    )

    model = build_rgb_model(
        model_name=config["model"]["name"],
        num_classes=int(config["model"]["num_classes"]),
        pretrained=bool(config["model"].get("pretrained", False)),
    )

    device = get_device()
    model = model.to(device)

    criterion = build_loss("cross_entropy")

    optimizer = build_optimizer(
        model=model,
        name=config["training"]["optimizer"],
        learning_rate=float(config["training"]["learning_rate"]),
        weight_decay=float(config["training"].get("weight_decay", 0.0)),
    )

    scheduler = build_scheduler(
        optimizer=optimizer,
        name=config["training"].get("scheduler"),
        epochs=int(config["training"]["epochs"]),
    )

    epochs = int(config["training"]["epochs"])
    best_macro_f1 = -1.0
    best_metrics: dict[str, Any] = {}

    history: list[dict[str, Any]] = []

    for epoch in range(1, epochs + 1):
        train_loss = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
        )

        metrics = evaluate_model(
            model=model,
            dataloader=test_loader,
            criterion=criterion,
            device=device,
        )

        metrics["epoch"] = epoch
        metrics["train_loss"] = train_loss

        history.append(metrics)

        print(
            f"Epoch {epoch}/{epochs} | "
            f"train_loss={train_loss:.4f} | "
            f"val_loss={metrics['loss']:.4f} | "
            f"accuracy={metrics['accuracy']:.4f} | "
            f"macro_f1={metrics['macro_f1']:.4f}"
        )

        if scheduler is not None:
            if scheduler.__class__.__name__ == "ReduceLROnPlateau":
                scheduler.step(metrics["loss"])
            else:
                scheduler.step()

        if metrics["macro_f1"] > best_macro_f1:
            best_macro_f1 = metrics["macro_f1"]
            best_metrics = metrics
            save_checkpoint(model, run_dir, "best_model.pt")

    save_metrics(best_metrics, run_dir)
    from terrasight.experiments.experiment_tracker import register_experiment

    register_experiment(
        config=config,
        metrics_file=run_dir / "metrics.json",
        run_dir=run_dir,
    )
    history_path = run_dir / "history.json"
    with history_path.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)

    print("Training complete")
    print(f"Best macro-F1: {best_macro_f1:.4f}")
    print(f"Run directory: {run_dir}")

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Train TerraSight RGB baseline.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    train_from_config(args.config)


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: __init__.py
PATH: src/terrasight/utils/__init__.py
========================================================================================================================

```python

```


========================================================================================================================
FILE: config.py
PATH: src/terrasight/utils/config.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


REQUIRED_TOP_LEVEL_KEYS = ["experiment", "seed", "data", "model", "training", "evaluation"]


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(f"Config must be a YAML dictionary: {path}")

    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in config]

    if missing:
        raise ValueError(f"Missing required config keys: {missing}")

    if "id" not in config["experiment"]:
        raise ValueError("Missing experiment.id")

    if "dataset" not in config["data"]:
        raise ValueError("Missing data.dataset")

    if "bands" not in config["data"]:
        raise ValueError("Missing data.bands")

    if "name" not in config["model"]:
        raise ValueError("Missing model.name")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load and validate a TerraSight config file.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)

    print("Config loaded successfully")
    print(f"Experiment ID: {config['experiment']['id']}")
    print(f"Model: {config['model']['name']}")
    print(f"Bands: {config['data']['bands']}")


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: reproducibility.py
PATH: src/terrasight/utils/reproducibility.py
========================================================================================================================

```python
from __future__ import annotations

import os
import random

import numpy as np


def set_seed(seed: int, deterministic: bool = True) -> None:
    """Set random seeds for reproducible experiments."""

    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

        if deterministic:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


def get_seed_from_config(config: dict) -> int:
    """Extract seed from config dictionary."""

    seed = config.get("seed")

    if seed is None:
        raise ValueError("Config does not contain a seed value.")

    return int(seed)
```


========================================================================================================================
FILE: run_setup.py
PATH: src/terrasight/utils/run_setup.py
========================================================================================================================

```python
from __future__ import annotations

import argparse
import json
import platform
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from terrasight.utils.config import load_config
from terrasight.utils.reproducibility import get_seed_from_config, set_seed


def create_run_dir(config: dict[str, Any], base_dir: str | Path = "results") -> Path:
    """Create a timestamped run directory."""

    experiment_id = config["experiment"]["id"]
    version = config["experiment"].get("version", "unknown_version")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = Path(base_dir) / version / f"{timestamp}_{experiment_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    return run_dir


def save_config_copy(config_path: str | Path, run_dir: Path) -> None:
    """Copy original config file into run directory."""

    config_path = Path(config_path)
    destination = run_dir / "config.yaml"
    shutil.copy2(config_path, destination)


def save_metadata(config: dict[str, Any], run_dir: Path) -> None:
    """Save reproducibility metadata."""

    metadata = {
        "experiment_id": config["experiment"]["id"],
        "version": config["experiment"].get("version"),
        "seed": config.get("seed"),
        "created_at": datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }

    metadata_path = run_dir / "metadata.json"

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def setup_run(config_path: str | Path) -> Path:
    """Load config, set seed, create run directory, and save metadata."""

    config = load_config(config_path)

    seed = get_seed_from_config(config)
    set_seed(seed)

    run_dir = create_run_dir(config)
    save_config_copy(config_path, run_dir)
    save_metadata(config, run_dir)

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare reproducible TerraSight run folder.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    run_dir = setup_run(args.config)

    print("Run setup complete")
    print(f"Run directory: {run_dir}")


if __name__ == "__main__":
    main()
```


========================================================================================================================
FILE: dependency_links.txt
PATH: src/terrasight.egg-info/dependency_links.txt
========================================================================================================================

```yaml


```


========================================================================================================================
FILE: SOURCES.txt
PATH: src/terrasight.egg-info/SOURCES.txt
========================================================================================================================

```yaml
pyproject.toml
src/terrasight/__init__.py
src/terrasight.egg-info/PKG-INFO
src/terrasight.egg-info/SOURCES.txt
src/terrasight.egg-info/dependency_links.txt
src/terrasight.egg-info/top_level.txt
src/terrasight/data/__init__.py
src/terrasight/data/band_registry.py
src/terrasight/data/dataset.py
src/terrasight/data/preprocessing.py
src/terrasight/data/split.py
src/terrasight/evaluation/__init__.py
src/terrasight/evaluation/confusion.py
src/terrasight/evaluation/metrics.py
src/terrasight/explainability/__init__.py
src/terrasight/features/__init__.py
src/terrasight/features/spectral_indices.py
src/terrasight/models/__init__.py
src/terrasight/models/backbone_factory.py
src/terrasight/models/model_utils.py
src/terrasight/models/multispectral_model.py
src/terrasight/models/rgb_model.py
src/terrasight/pipelines/__init__.py
src/terrasight/pipelines/train_rgb.py
src/terrasight/reliability/__init__.py
src/terrasight/reporting/__init__.py
src/terrasight/training/__init__.py
src/terrasight/training/losses.py
src/terrasight/training/optimizer_factory.py
src/terrasight/training/scheduler_factory.py
src/terrasight/training/trainer.py
src/terrasight/utils/__init__.py
src/terrasight/utils/config.py
src/terrasight/utils/reproducibility.py
src/terrasight/utils/run_setup.py
tests/test_metrics.py
tests/test_models.py
tests/test_spectral_indices.py
tests/test_training.py
```


========================================================================================================================
FILE: top_level.txt
PATH: src/terrasight.egg-info/top_level.txt
========================================================================================================================

```yaml
terrasight

```


========================================================================================================================
FILE: test_band_sets.py
PATH: tests/test_band_sets.py
========================================================================================================================

```python
import torch

from terrasight.data.band_registry import SENTINEL2_BANDS
from terrasight.features.band_selection import select_bands
from terrasight.features.band_sets import get_band_set, list_band_sets, validate_band_set


def test_get_rgb_band_set() -> None:
    bands = get_band_set("rgb")

    assert bands == ["B4", "B3", "B2"]


def test_list_band_sets() -> None:
    names = list_band_sets()

    assert "rgb" in names
    assert "full_13" in names


def test_validate_band_set() -> None:
    validate_band_set(["B4", "B3", "B2"])


def test_select_bands() -> None:
    image = torch.randn(13, 4, 4)

    selected = select_bands(
        image=image,
        source_bands=SENTINEL2_BANDS,
        selected_bands=["B4", "B3", "B2"],
    )

    assert selected.shape == (3, 4, 4)


def test_select_full_bands() -> None:
    image = torch.randn(13, 4, 4)

    selected = select_bands(
        image=image,
        source_bands=SENTINEL2_BANDS,
        selected_bands=SENTINEL2_BANDS,
    )

    assert selected.shape == (13, 4, 4)
```


========================================================================================================================
FILE: test_comparison.py
PATH: tests/test_comparison.py
========================================================================================================================

```python
import pandas as pd

from terrasight.reporting.comparison import (
    add_rgb_vs_ms_delta,
    build_comparison_table,
)


def test_build_comparison_table() -> None:
    registry = pd.DataFrame(
        [
            {
                "experiment_id": "rgb",
                "version": "v1",
                "input_type": "rgb",
                "model": "resnet18",
                "input_channels": 3,
                "bands": "B4,B3,B2",
                "epochs": 1,
                "accuracy": 0.90,
                "macro_f1": 0.89,
                "weighted_f1": 0.90,
                "balanced_accuracy": 0.88,
                "run_directory": "results/v1/rgb",
            },
            {
                "experiment_id": "ms",
                "version": "v1",
                "input_type": "multispectral",
                "model": "resnet18",
                "input_channels": 13,
                "bands": "B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B10,B11,B12",
                "epochs": 1,
                "accuracy": 0.95,
                "macro_f1": 0.94,
                "weighted_f1": 0.95,
                "balanced_accuracy": 0.93,
                "run_directory": "results/v1/ms",
            },
        ]
    )

    comparison = build_comparison_table(registry)

    assert comparison.shape[0] == 2
    assert comparison.iloc[0]["experiment_id"] == "ms"


def test_add_rgb_vs_ms_delta() -> None:
    comparison = pd.DataFrame(
        [
            {
                "experiment_id": "rgb",
                "version": "v1",
                "input_type": "rgb",
                "model": "resnet18",
                "input_channels": 3,
                "bands": "B4,B3,B2",
                "epochs": 1,
                "accuracy": 0.90,
                "macro_f1": 0.89,
                "weighted_f1": 0.90,
                "balanced_accuracy": 0.88,
                "run_directory": "results/v1/rgb",
            },
            {
                "experiment_id": "ms",
                "version": "v1",
                "input_type": "multispectral",
                "model": "resnet18",
                "input_channels": 13,
                "bands": "full_13",
                "epochs": 1,
                "accuracy": 0.95,
                "macro_f1": 0.94,
                "weighted_f1": 0.95,
                "balanced_accuracy": 0.93,
                "run_directory": "results/v1/ms",
            },
        ]
    )

    output = add_rgb_vs_ms_delta(
        comparison=comparison,
        rgb_experiment_id="rgb",
        ms_experiment_id="ms",
        metric="macro_f1",
    )

    delta_value = output.loc[
        output["experiment_id"] == "ms",
        "delta_vs_rgb_macro_f1",
    ].iloc[0]

    assert abs(delta_value - 0.05) < 1e-8
```


========================================================================================================================
FILE: test_explainability.py
PATH: tests/test_explainability.py
========================================================================================================================

```python
import torch
import torch.nn as nn

from terrasight.explainability.gradcam import GradCAM
from terrasight.explainability.spectral_attribution import (
    band_occlusion_scores,
    rank_band_importance,
)


class TinyCNN(nn.Module):
    def __init__(self, input_channels: int = 3, num_classes: int = 2) -> None:
        super().__init__()
        self.conv = nn.Conv2d(input_channels, 4, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(4, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.relu(self.conv(x))
        x = self.pool(x).flatten(1)
        return self.fc(x)


def test_gradcam_generates_heatmap() -> None:
    model = TinyCNN(input_channels=3, num_classes=2)
    target_layer = model.conv

    gradcam = GradCAM(model=model, target_layer=target_layer)

    image = torch.randn(1, 3, 32, 32)
    heatmap = gradcam.generate(image=image, class_index=1)

    gradcam.close()

    assert heatmap.shape == (32, 32)
    assert torch.all(heatmap >= 0)
    assert torch.all(heatmap <= 1)


def test_band_occlusion_scores() -> None:
    model = TinyCNN(input_channels=3, num_classes=2)
    image = torch.randn(1, 3, 32, 32)
    band_names = ["B4", "B3", "B2"]

    scores = band_occlusion_scores(
        model=model,
        image=image,
        target_class=1,
        band_names=band_names,
    )

    assert set(scores.keys()) == set(band_names)


def test_rank_band_importance() -> None:
    scores = {
        "B4": 0.1,
        "B3": 0.3,
        "B2": -0.2,
    }

    ranked = rank_band_importance(scores)

    assert ranked[0][0] == "B3"
    assert ranked[-1][0] == "B2"
```


========================================================================================================================
FILE: test_metrics.py
PATH: tests/test_metrics.py
========================================================================================================================

```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import numpy as np

from terrasight.evaluation.confusion import compute_confusion_matrix
from terrasight.evaluation.metrics import compute_classification_metrics, compute_classwise_report


def test_compute_classification_metrics() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 1, 0, 2])

    metrics = compute_classification_metrics(y_true, y_pred)

    assert metrics["accuracy"] == 0.75
    assert "macro_f1" in metrics
    assert "weighted_f1" in metrics
    assert "balanced_accuracy" in metrics


def test_compute_classwise_report() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 1, 0, 2])

    report = compute_classwise_report(
        y_true,
        y_pred,
        target_names=["class_0", "class_1", "class_2"],
    )

    assert "class_0" in report
    assert "class_1" in report
    assert "class_2" in report


def test_compute_confusion_matrix() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 1, 0, 2])

    cm = compute_confusion_matrix(y_true, y_pred)

    assert cm.shape == (3, 3)
    assert cm.sum() == 4
```


========================================================================================================================
FILE: test_models.py
PATH: tests/test_models.py
========================================================================================================================

```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import torch

from terrasight.models.rgb_model import build_rgb_model
from terrasight.models.multispectral_model import build_multispectral_model


def test_rgb_model_forward_pass() -> None:
    model = build_rgb_model(
        model_name="resnet18",
        num_classes=10,
        pretrained=False,
    )

    x = torch.randn(2, 3, 64, 64)
    y = model(x)

    assert y.shape == (2, 10)


def test_multispectral_model_forward_pass() -> None:
    model = build_multispectral_model(
        model_name="resnet18",
        input_channels=13,
        num_classes=10,
        pretrained=False,
    )

    x = torch.randn(2, 13, 64, 64)
    y = model(x)

    assert y.shape == (2, 10)


def test_index_augmented_model_forward_pass() -> None:
    model = build_multispectral_model(
        model_name="resnet18",
        input_channels=16,
        num_classes=10,
        pretrained=False,
    )

    x = torch.randn(2, 16, 64, 64)
    y = model(x)

    assert y.shape == (2, 10)
```


========================================================================================================================
FILE: test_registry.py
PATH: tests/test_registry.py
========================================================================================================================

```python
import json
from pathlib import Path

from terrasight.experiments.experiment_tracker import register_experiment


def test_registry_append(tmp_path):

    metrics_path = tmp_path / "metrics.json"

    metrics = {
        "accuracy": 0.9,
        "macro_f1": 0.8,
        "weighted_f1": 0.85,
        "balanced_accuracy": 0.82,
    }

    with metrics_path.open("w") as f:
        json.dump(metrics, f)

    config = {
        "experiment": {
            "id": "test",
            "version": "v1",
        },
        "data": {
            "input_type": "rgb",
            "bands": ["B4", "B3", "B2"],
        },
        "model": {
            "name": "resnet18",
            "input_channels": 3,
        },
        "training": {
            "epochs": 1,
        },
    }

    registry_path = tmp_path / "registry.csv"

    register_experiment(
        config=config,
        metrics_file=metrics_path,
        run_dir=tmp_path,
        registry_path=registry_path,
    )

    assert registry_path.exists()
```


========================================================================================================================
FILE: test_reliability.py
PATH: tests/test_reliability.py
========================================================================================================================

```python
import numpy as np
import torch

from terrasight.reliability.calibration import (
    expected_calibration_error,
    maximum_calibration_error,
    softmax_confidences,
)
from terrasight.reliability.failure_analysis import (
    confusion_pairs,
    extract_failure_indices,
)
from terrasight.reliability.robustness import (
    add_gaussian_noise,
    apply_brightness_shift,
    compute_degradation,
    dropout_bands,
)
from terrasight.reliability.uncertainty import (
    confidence_error_flags,
    confidence_margin,
    predictive_entropy,
)


def test_softmax_confidences() -> None:
    logits = torch.tensor([[3.0, 1.0], [0.2, 2.0]])

    predictions, confidences = softmax_confidences(logits)

    assert predictions.tolist() == [0, 1]
    assert confidences.shape == (2,)


def test_expected_calibration_error() -> None:
    y_true = np.array([0, 1, 1, 0])
    y_pred = np.array([0, 1, 0, 0])
    confidences = np.array([0.9, 0.8, 0.7, 0.6])

    ece = expected_calibration_error(y_true, y_pred, confidences)

    assert isinstance(ece, float)
    assert ece >= 0.0


def test_maximum_calibration_error() -> None:
    y_true = np.array([0, 1, 1, 0])
    y_pred = np.array([0, 1, 0, 0])
    confidences = np.array([0.9, 0.8, 0.7, 0.6])

    mce = maximum_calibration_error(y_true, y_pred, confidences)

    assert isinstance(mce, float)
    assert mce >= 0.0


def test_predictive_entropy() -> None:
    probs = torch.tensor([[0.8, 0.2], [0.5, 0.5]])

    entropy = predictive_entropy(probs)

    assert entropy.shape == (2,)
    assert entropy[1] > entropy[0]


def test_confidence_margin() -> None:
    probs = torch.tensor([[0.8, 0.2], [0.55, 0.45]])

    margin = confidence_margin(probs)

    assert margin.shape == (2,)
    assert margin[0] > margin[1]


def test_confidence_error_flags() -> None:
    y_true = np.array([0, 1, 1])
    y_pred = np.array([0, 0, 1])
    confidences = np.array([0.95, 0.91, 0.4])

    flags = confidence_error_flags(y_true, y_pred, confidences)

    assert flags["high_confidence_correct"] == 1
    assert flags["high_confidence_errors"] == 1


def test_failure_indices() -> None:
    y_true = np.array([0, 1, 2])
    y_pred = np.array([0, 2, 2])

    failures = extract_failure_indices(y_true, y_pred)

    assert failures == [1]


def test_confusion_pairs() -> None:
    y_true = np.array([0, 1, 1, 2])
    y_pred = np.array([0, 2, 2, 1])
    class_names = ["A", "B", "C"]

    pairs = confusion_pairs(y_true, y_pred, class_names)

    assert pairs[0]["true_class"] == "B"
    assert pairs[0]["predicted_class"] == "C"
    assert pairs[0]["count"] == 2


def test_robustness_transforms() -> None:
    images = torch.ones((2, 13, 4, 4))

    noisy = add_gaussian_noise(images, std=0.01)
    bright = apply_brightness_shift(images, shift=0.1)
    dropped = dropout_bands(images, band_indices=[0, 1])

    assert noisy.shape == images.shape
    assert bright.shape == images.shape
    assert torch.all(dropped[:, 0, :, :] == 0)
    assert torch.all(dropped[:, 1, :, :] == 0)


def test_compute_degradation() -> None:
    degradation = compute_degradation(clean_metric=0.95, perturbed_metric=0.90)

    assert abs(degradation - 0.05) < 1e-8
```


========================================================================================================================
FILE: test_reporting.py
PATH: tests/test_reporting.py
========================================================================================================================

```python
import json

import pandas as pd

from terrasight.reporting.figures import save_metric_bar_chart, save_training_curve
from terrasight.reporting.report_assets import generate_single_run_assets
from terrasight.reporting.tables import build_comparison_table, load_metrics, metrics_to_table


def test_metrics_to_table() -> None:
    metrics = {
        "accuracy": 0.9,
        "macro_f1": 0.8,
        "weighted_f1": 0.85,
        "balanced_accuracy": 0.82,
        "loss": 0.3,
    }

    table = metrics_to_table(metrics, experiment_name="test_exp")

    assert table.shape[0] == 1
    assert table.loc[0, "experiment"] == "test_exp"
    assert table.loc[0, "accuracy"] == 0.9


def test_build_comparison_table() -> None:
    row1 = pd.DataFrame([{"experiment": "rgb", "accuracy": 0.9}])
    row2 = pd.DataFrame([{"experiment": "ms", "accuracy": 0.95}])

    table = build_comparison_table([row1, row2])

    assert table.shape[0] == 2


def test_load_metrics(tmp_path) -> None:
    metrics_path = tmp_path / "metrics.json"

    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump({"accuracy": 0.9}, file)

    metrics = load_metrics(metrics_path)

    assert metrics["accuracy"] == 0.9


def test_save_metric_bar_chart(tmp_path) -> None:
    table = pd.DataFrame(
        [
            {"experiment": "rgb", "macro_f1": 0.8},
            {"experiment": "ms", "macro_f1": 0.9},
        ]
    )

    output_path = tmp_path / "figures" / "bar.png"

    save_metric_bar_chart(
        table=table,
        metric="macro_f1",
        output_path=output_path,
    )

    assert output_path.exists()


def test_save_training_curve(tmp_path) -> None:
    history = [
        {"epoch": 1, "macro_f1": 0.7},
        {"epoch": 2, "macro_f1": 0.8},
    ]

    output_path = tmp_path / "figures" / "curve.png"

    save_training_curve(
        history=history,
        output_path=output_path,
        metric="macro_f1",
    )

    assert output_path.exists()


def test_generate_single_run_assets(tmp_path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    with (run_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(
            {
                "accuracy": 0.9,
                "macro_f1": 0.8,
                "weighted_f1": 0.85,
                "balanced_accuracy": 0.82,
                "loss": 0.3,
            },
            file,
        )

    with (run_dir / "history.json").open("w", encoding="utf-8") as file:
        json.dump(
            [
                {"epoch": 1, "macro_f1": 0.7},
                {"epoch": 2, "macro_f1": 0.8},
            ],
            file,
        )

    output_dir = tmp_path / "reports"

    generate_single_run_assets(
        run_dir=run_dir,
        experiment_name="test_exp",
        output_dir=output_dir,
    )

    assert (output_dir / "tables" / "test_exp_metrics.csv").exists()
    assert (output_dir / "figures" / "test_exp_macro_f1.png").exists()
    assert (output_dir / "figures" / "test_exp_training_curve.png").exists()
```


========================================================================================================================
FILE: test_spectral_indices.py
PATH: tests/test_spectral_indices.py
========================================================================================================================

```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import torch

from terrasight.features.spectral_indices import (
    append_indices_to_multispectral,
    compute_ndbi,
    compute_ndvi,
    compute_ndwi,
)


def test_compute_ndvi() -> None:
    nir = torch.tensor([0.8])
    red = torch.tensor([0.2])

    ndvi = compute_ndvi(nir=nir, red=red)

    assert torch.allclose(ndvi, torch.tensor([0.6]), atol=1e-5)


def test_compute_ndwi() -> None:
    green = torch.tensor([0.6])
    nir = torch.tensor([0.2])

    ndwi = compute_ndwi(green=green, nir=nir)

    assert torch.allclose(ndwi, torch.tensor([0.5]), atol=1e-5)


def test_compute_ndbi() -> None:
    swir = torch.tensor([0.7])
    nir = torch.tensor([0.3])

    ndbi = compute_ndbi(swir=swir, nir=nir)

    assert torch.allclose(ndbi, torch.tensor([0.4]), atol=1e-5)


def test_append_indices_to_multispectral() -> None:
    band_names = [
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B8",
        "B8A",
        "B9",
        "B10",
        "B11",
        "B12",
    ]

    image = torch.ones((13, 4, 4))

    output = append_indices_to_multispectral(image=image, band_names=band_names)

    assert output.shape == (16, 4, 4)
```


========================================================================================================================
FILE: test_training.py
PATH: tests/test_training.py
========================================================================================================================

```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import torch

from terrasight.models.rgb_model import build_rgb_model
from terrasight.training.losses import build_loss
from terrasight.training.optimizer_factory import build_optimizer
from terrasight.training.scheduler_factory import build_scheduler


def test_build_cross_entropy_loss() -> None:
    loss = build_loss("cross_entropy")
    assert isinstance(loss, torch.nn.CrossEntropyLoss)


def test_build_optimizer() -> None:
    model = build_rgb_model(pretrained=False)
    optimizer = build_optimizer(
        model=model,
        name="adamw",
        learning_rate=0.001,
        weight_decay=0.0,
    )

    assert isinstance(optimizer, torch.optim.AdamW)


def test_build_scheduler_none() -> None:
    model = build_rgb_model(pretrained=False)
    optimizer = build_optimizer(model=model)

    scheduler = build_scheduler(
        optimizer=optimizer,
        name=None,
        epochs=2,
    )

    assert scheduler is None


def test_single_training_step() -> None:
    model = build_rgb_model(pretrained=False)
    criterion = build_loss("cross_entropy")
    optimizer = build_optimizer(model=model)

    x = torch.randn(2, 3, 64, 64)
    y = torch.tensor([0, 1])

    logits = model(x)
    loss = criterion(logits, y)

    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

    assert loss.item() > 0
```

