# TerraSight: EuroSAT RGB vs Multispectral Land-Cover Classification

**Author:** Toktam Khatibi, PhD
> **Project Documentation**
>
> This repository is accompanied by a formal technical report that presents the complete scientific investigation, including the research questions, hypotheses, experimental methodology, statistical analysis, explainability studies, reliability assessment, robustness evaluation, and conclusions.
>
> The report is available at:
>
> - `docs/technical_report.md`
> - `docs/technical_report.pdf`
>
> The README serves as the primary repository guide, while the technical report provides the detailed scientific narrative and interpretation of the results.

# Executive Summary

TerraSight is a research-grade remote-sensing machine-learning framework that investigates the value of Sentinel-2 multispectral imagery for land-cover classification using the EuroSAT benchmark dataset.

The project goes beyond conventional classification benchmarking by combining:

- RGB versus multispectral comparison
- Transfer-learning evaluation
- Sentinel-2 band-ablation studies
- Spectral separability analysis
- Statistical significance testing
- Reliability and calibration assessment
- Explainability analysis using Grad-CAM
- Robustness evaluation
- Reproducible machine-learning workflows

The central objective is to determine whether carefully selected Sentinel-2 spectral bands provide meaningful information beyond RGB imagery and to understand why these improvements occur from both machine-learning and remote-sensing perspectives.

### Main Findings

1. ImageNet-pretrained RGB models achieved the highest overall classification accuracy (**97.46%**).
2. The best multispectral configuration combined **RGB + RedEdge + NIR + SWIR** bands and achieved **95.67% accuracy** and **95.56% Macro-F1**.
3. Statistical testing demonstrated that the multispectral improvement is significant for class-balanced performance metrics.
4. Spectral separability analysis revealed that classification performance is strongly linked to the intrinsic physical similarity of land-cover classes.
5. Using all available Sentinel-2 bands does not necessarily produce the best results.
6. Carefully selected multispectral information is more valuable than simply increasing spectral dimensionality.

### Central Scientific Conclusion

> Spectral selection is more important than spectral quantity. Carefully selected Red Edge, Near-Infrared (NIR), and Short-Wave Infrared (SWIR) bands provide complementary information beyond RGB imagery and significantly improve discrimination of challenging land-cover classes.

### Practical Significance

The methodology developed in this project is directly relevant to trustworthy AI systems for:

- Earth observation
- Environmental monitoring
- Vegetation assessment
- Infrastructure corridor monitoring
- Land-use and land-cover mapping
- Geospatial decision-support systems

By combining performance evaluation with statistical validation, explainability, robustness analysis, and reproducibility practices, TerraSight demonstrates a complete workflow for developing deployable remote-sensing AI systems.

Unlike conventional classification benchmarks, TerraSight focuses on a central scientific question:

> Which Sentinel-2 spectral information contributes most effectively to land-cover classification performance?

The framework emphasizes reproducibility, scientific rigor, explainability, reliability, and practical interpretation of multispectral remote-sensing models.

# Key Contributions

This project makes the following technical and scientific contributions:

1. Systematic RGB versus multispectral comparison using Sentinel-2 imagery.
2. Evaluation of transfer learning for multispectral remote-sensing classification.
3. Controlled Sentinel-2 band-ablation experiments.
4. Physical interpretation of spectral-band utility through spectral separability analysis.
5. Statistical validation using bootstrap confidence intervals and McNemar significance testing.
6. Reliability assessment using calibration and confidence analysis.
7. Explainability analysis using Grad-CAM.
8. Robustness evaluation under perturbations and band removal.
9. Fully reproducible configuration-driven machine-learning framework.

## Formal Assessment Report

This README provides the full technical project documentation, including extended analyses, figures, reproducibility details, and supplementary interpretation.

A concise assessment report prepared for the Aston University technical task is provided separately:

```text
docs/technical_report.md
```

The formal report is kept within the required word limit, while this README serves as the complete project reference document.

# Project Overview and Architecture

## Figure 1. Graphical Abstract

The graphical abstract summarizes the complete research workflow and the key scientific findings of the project. Starting from the EuroSAT Sentinel-2 dataset, the study compares RGB and multispectral representations using ResNet18-based architectures, investigates the contribution of individual spectral bands through systematic ablation studies, and evaluates model reliability, explainability, and robustness.

The study demonstrates that carefully selected spectral bands can provide complementary information beyond RGB imagery, while increasing the number of spectral bands does not necessarily improve classification performance. The results highlight the importance of informed spectral-band selection and model calibration in Earth Observation applications.

<p align="center">
  <img src="images/graphical_abstract.jpg"
       alt="TerraSight Graphical Abstract"
       width="1000">
</p>

**Figure 1.** Graphical abstract of the TerraSight project showing dataset inputs, experimental pipelines, evaluation modules, explainability analysis, reliability assessment, and the principal scientific findings.

### Key Messages

- Comparison of RGB and multispectral Sentinel-2 representations.
- Evaluation of pretrained and non-pretrained ResNet18 models.
- Systematic spectral-band ablation experiments.
- Reliability and calibration assessment using confidence-based metrics.
- Explainability analysis using Grad-CAM visualizations.
- Investigation of robustness under input perturbations.
- Identification of the most informative spectral-band combinations.
- End-to-end reproducible machine learning workflow.

## Figure 2. Project Architecture

Figure 2 presents the complete technical architecture of the project. The architecture is organized as a sequence of interconnected layers, beginning with data acquisition and preprocessing, followed by model development, experimental evaluation, explainability analysis, robustness testing, and reproducibility infrastructure.

This architecture was designed to satisfy both engineering and scientific objectives. Beyond achieving strong classification performance, the framework provides mechanisms for understanding model decisions, evaluating prediction confidence, assessing robustness, and ensuring experimental reproducibility.

<p align="center">
  <img src="images/project_architecture.jpg"
       alt="TerraSight Project Architecture"
       width="1200">
</p>

**Figure 2.** End-to-end architecture of the TerraSight framework showing data processing, model development, experimental evaluation, reliability analysis, explainability modules, robustness assessment, and reproducibility infrastructure.

### Architectural Components

#### Data Layer

- EuroSAT RGB dataset.
- EuroSAT multispectral Sentinel-2 dataset.
- Ten land-cover classes.

#### Preprocessing Layer

- Dataset validation.
- Stratified train/test splitting.
- Data normalization.
- Data augmentation.
- RGB and multispectral dataloaders.

#### Modeling Layer

- RGB ResNet18 (pretrained).
- RGB ResNet18 (trained from scratch).
- Multispectral ResNet18 (trained from scratch).
- Adapted pretrained multispectral ResNet18.

#### Experimental Layer

- RGB versus multispectral comparison.
- Spectral-band ablation studies.
- Multi-seed evaluation for stability analysis.

#### Evaluation Layer

- Accuracy.
- Macro-F1 score.
- Weighted-F1 score.
- Balanced accuracy.
- Confusion matrix analysis.
- Per-class performance assessment.

#### Reliability Layer

- Expected Calibration Error (ECE).
- Confidence histogram analysis.
- Reliability diagrams.
- High-confidence failure analysis.

#### Explainability Layer

- Grad-CAM visualizations.
- Class-specific attention analysis.
- Failure-case interpretation.
- Spectral attribution investigation.

#### Robustness Layer

- Gaussian noise perturbation.
- Brightness variation analysis.
- Band-dropout experiments.
- Performance degradation assessment.

#### Reproducibility Layer

- YAML configuration files.
- Experiment registry.
- Fixed random seeds.
- Automated figure generation.
- Automated reporting pipeline.

## Scientific Investigation Framework and Decision Chain
Figure 3 presents the complete scientific reasoning framework that guided the design, execution, and interpretation of the TerraSight project. Unlike a conventional machine-learning workflow that focuses primarily on model development, this framework represents a hypothesis-driven investigation into the value of Sentinel-2 multispectral information for land-cover classification.
<p align="center">
  <img src="images/Figure_3.jpg"
       alt="TerraSight Project Architecture"
       width="1200">
</p>

**Figure 3.** Scientific investigation framework and decision chain

The study begins with the central research question:

> Which Sentinel-2 spectral information contributes most effectively to land-cover classification?

To address this question, three scientific hypotheses were formulated. First, non-RGB spectral bands may provide complementary information beyond visible-spectrum imagery. Second, not all Sentinel-2 bands contribute equally to classification performance. Third, careful spectral-band selection may be more important than simply increasing the number of input bands.

The experimental design was informed by three sources of evidence: the technical assessment requirements, findings from the remote-sensing literature, and the physical characteristics of Sentinel-2 spectral bands. This evidence-based design process ensured that all experimental choices were scientifically justified rather than selected arbitrarily.

A controlled comparison was then performed between RGB-only and multispectral models under identical experimental conditions. Following the initial comparison, systematic band-ablation experiments were conducted to investigate the contribution of different spectral-band combinations, including RGB, NIR, Red Edge, SWIR, and full-spectrum Sentinel-2 inputs. This process identified the most effective spectral configuration for subsequent analysis.

After selecting the strongest spectral configuration, evidence was collected from multiple complementary perspectives, including quantitative performance metrics, qualitative visual analysis, and spectral-domain investigations. The resulting evidence was evaluated through four independent scientific questions:

### Q1. Why does multispectral information help?

This branch focuses on understanding the mechanisms behind observed performance improvements. Analysis included class-wise performance assessment, spectral separability analysis, physical interpretation of Sentinel-2 bands, Grad-CAM visualizations, and failure-case investigation. These analyses provide insight into how Red Edge, NIR, and SWIR bands contribute complementary information beyond RGB imagery and help explain class-specific improvements.

### Q2. Is the observed improvement real?

This branch evaluates whether performance differences are statistically meaningful. Bootstrap confidence intervals, McNemar significance tests, effect-size analysis, and multi-seed validation were used to assess the robustness of the reported improvements and reduce the risk of drawing conclusions from random variation.

### Q3. Can the model be trusted?

This branch investigates prediction reliability. Calibration analysis, reliability diagrams, confidence distributions, and high-confidence failure analysis were used to assess whether model confidence accurately reflects prediction correctness and whether the resulting models are suitable for trustworthy decision-support applications.

### Q4. Is the model robust?

This branch evaluates model behaviour under realistic perturbations. Gaussian noise, brightness variation, and band-dropout experiments were used to quantify performance degradation and identify sensitivity to input uncertainty and spectral-information loss.

The results from all four validation branches were integrated through an evidence-synthesis stage. Rather than relying solely on classification accuracy, conclusions were derived from a combination of statistical, spectral, explainability, reliability, and robustness evidence.

### Scientific Conclusion

The combined evidence demonstrates that carefully selected multispectral information provides meaningful complementary information beyond RGB imagery. In particular, Red Edge, Near-Infrared (NIR), and Short-Wave Infrared (SWIR) bands improve discrimination of several challenging land-cover classes. The findings further show that increasing the number of spectral bands does not necessarily improve performance. Instead, the results support the central conclusion:

> **Spectral selection is more important than spectral quantity.**

### Reproducibility Framework

A reproducibility framework supports every stage of the investigation. The framework includes fixed train-test splits, fixed random seeds, YAML-based experiment configurations, an experiment registry, automated reporting, command validation, and version-controlled source code. These components ensure that all reported results can be independently reproduced and audited.

### Limitations and Future Work

Several limitations remain. The study was conducted using a single benchmark dataset, multi-seed validation was applied only to the strongest configurations, and segmentation experiments were not performed because EuroSAT does not provide ground-truth segmentation labels. Future work may investigate self-supervised learning, foundation models, additional remote-sensing datasets, and more advanced uncertainty-estimation techniques.

### Operational and Industrial Relevance

Beyond benchmark performance, the framework demonstrates a complete workflow for developing trustworthy Earth Observation AI systems. By combining explainability, calibration analysis, robustness testing, statistical validation, and reproducibility practices, the methodology aligns with the requirements of real-world image-analysis and geospatial decision-support systems. The resulting workflow is directly relevant to industrial AI applications that require transparent, reliable, and reproducible model behaviour.
### Design Principles

The framework was designed around five core principles:

1. **Performance** — achieve strong land-cover classification accuracy.
2. **Interpretability** — explain model decisions through visual analysis.
3. **Reliability** — quantify prediction confidence and calibration quality.
4. **Robustness** — evaluate behavior under realistic perturbations.
5. **Reproducibility** — ensure experiments can be repeated exactly.

Together, these components form a comprehensive Earth Observation machine-learning framework that extends beyond conventional benchmark classification and emphasizes scientific rigor, transparency, and reproducibility.

## Key Results

| Finding | Result |
|----------|----------|
| Dataset | EuroSAT |
| Classes | 10 |
| Sensor | Sentinel-2 |
| Samples | ~27,000 |
| Best Overall Model | RGB ResNet18 (ImageNet Pretrained) |
| Best Overall Accuracy | **97.46%** |
| Best Multispectral Configuration | RGB + RedEdge + NIR + SWIR |
| Best Multispectral Accuracy | **95.67%** |
| Best Multispectral Macro-F1 | **95.56%** |
| Best Multispectral Calibration (ECE) | **0.0039** |
| Number of Experimental Configurations | 11+ |
| Random Seeds Evaluated | 3 |

### Main Scientific Finding

The results demonstrate that **spectral selection is more important than spectral quantity**.

Using all available Sentinel-2 bands did not produce the strongest multispectral performance. Instead, a carefully selected combination of RGB, RedEdge, NIR, and SWIR bands achieved the best balance of accuracy, calibration quality, and computational efficiency.

These findings suggest that multispectral information provides complementary information beyond RGB imagery, but performance gains depend strongly on selecting the most informative spectral channels rather than simply increasing input dimensionality.

## Research Questions

### Primary Research Question

Does Sentinel-2 multispectral information provide measurable benefits beyond RGB imagery for land-cover classification?

### Secondary Research Questions

1. Which Sentinel-2 spectral bands contribute most effectively to classification performance?
2. Can transfer learning improve multispectral remote-sensing models?
3. Is a carefully selected subset of spectral bands sufficient to match the performance of full multispectral models?
4. How reliable and interpretable are the resulting predictions?

### Hypothesis

Near-Infrared (NIR), RedEdge, and Short-Wave Infrared (SWIR) bands contain vegetation, moisture, and surface-composition information that is unavailable in RGB imagery. Therefore, combining selected multispectral bands with RGB information is expected to improve discrimination between spectrally similar land-cover classes.

## Scientific Contributions

This project makes several practical and scientific contributions:

### 1. RGB vs Multispectral Benchmark

A systematic comparison of RGB and multispectral ResNet18 classifiers using the EuroSAT dataset.

### 2. Transfer Learning for Multispectral Remote Sensing

Evaluation of adapted ImageNet-pretrained models versus training from scratch.

### 3. Sentinel-2 Band Ablation Study

Controlled experiments investigating the contribution of individual spectral groups, including:

- RGB
- RGB + NIR
- RGB + RedEdge + NIR
- RGB + RedEdge + NIR + SWIR
- Physical Surface Bands
- Full 13-Band Sentinel-2 Imagery

### 4. Statistical Validation

Paired bootstrap confidence intervals and McNemar significance testing were used to evaluate whether observed multispectral improvements were statistically meaningful.

Statistical results were generated automatically using paired bootstrap confidence intervals and McNemar significance testing. Detailed outputs are available in:

```text
reports/tables/statistical_tests/statistical_analysis.csv
reports/tables/statistical_tests/statistical_summary.md
```

### 5. Reliability and Calibration Analysis

Assessment of prediction trustworthiness using calibration metrics and confidence-based evaluation.

### 6. Explainability and Error Analysis

Investigation of model behaviour through Grad-CAM visualizations, confidence analysis, and failure-case inspection.

### 7. Reproducible Research Framework

Experiment tracking, configuration management, reproducible pipelines, and documented workflows suitable for future extension.

## Execution Environment

Experiments reported in this repository were executed using the following environment:

| Component | Value |
|------------|---------|
| PyTorch | 2.12.0+cpu |
| CUDA Available | False |
| CUDA Version | None |
| GPU Count | 0 |
| Execution Mode | CPU-only |
| Random Seed | 42 |

The framework is hardware-agnostic and supports GPU acceleration when CUDA-enabled PyTorch installations are available.

## Computational Considerations

The project was intentionally developed and evaluated on CPU-only hardware.

This demonstrates that:

- the framework is reproducible without specialised GPU resources;
- all reported experiments can be reproduced on standard research workstations;
- architectural choices prioritise reproducibility and practicality alongside performance.

Training times can be significantly reduced using CUDA-enabled GPUs without modifying the implementation.

### Computational Constraints

The framework was intentionally developed and evaluated under modest computational resources using CPU-only execution. This demonstrates that the proposed methodology can be reproduced without specialized hardware and remains accessible to researchers and practitioners with limited computational infrastructure.

Future work could investigate larger architectures, foundation models, and extensive hyperparameter optimization using GPU-accelerated environments.

## Dataset

### EuroSAT

The project uses the EuroSAT benchmark dataset, a widely adopted remote-sensing dataset derived from Sentinel-2 satellite imagery.

| Property | Value |
|----------|----------|
| Dataset | EuroSAT |
| Number of Classes | 10 |
| Total Images | ~27,000 |
| Spatial Resolution | 64 × 64 pixels |
| Source Sensor | Sentinel-2 |
| Modalities | RGB and Multispectral |

### Land-Cover Classes

The dataset contains the following land-use and land-cover categories:

- AnnualCrop
- Forest
- HerbaceousVegetation
- Highway
- Industrial
- Pasture
- PermanentCrop
- Residential
- River
- SeaLake

### Sentinel-2 Spectral Bands

Experiments utilize combinations of Sentinel-2 spectral bands:

| Spectral Group | Bands |
|----------|----------|
| RGB | B2, B3, B4 |
| RedEdge | B5, B6, B7 |
| Near Infrared (NIR) | B8, B8A |
| Water Vapour | B9 |
| Cirrus | B10 |
| Short-Wave Infrared (SWIR) | B11, B12 |

These bands capture complementary information related to vegetation health, moisture content, atmospheric conditions, and surface composition.

### Dataset Citation

> Helber, P., Bischke, B., Dengel, A., & Borth, D. (2019). EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing*.

## Methodology
#### Hyperparameter Strategy

A fixed hyperparameter configuration was used across comparable experiments to ensure a fair controlled comparison between RGB and multispectral inputs. The objective of this project was not exhaustive hyperparameter optimization, but a scientifically controlled evaluation of spectral information.

Core training settings, including optimizer, learning rate, batch size, number of epochs, early-stopping patience, and random seed, were defined in YAML configuration files and kept consistent across matched experiments.

This design prevents performance differences from being confounded by unequal tuning effort. Hyperparameter optimization is therefore treated as future work rather than a primary component of the current assessment.
### Experimental Design

The project follows a progressive experimental strategy designed to evaluate both predictive performance and spectral utility.

#### Phase 1 — RGB vs Multispectral Comparison

Four baseline models were evaluated:

| Experiment | Description |
|----------|----------|
| RGB Pretrained | ImageNet-pretrained RGB ResNet18 |
| RGB Scratch | RGB ResNet18 trained from scratch |
| Multispectral Adapted | Pretrained ResNet18 adapted for multispectral inputs |
| Multispectral Scratch | Multispectral ResNet18 trained from scratch |

The objective was to determine whether transfer learning and multispectral information improve classification performance.

#### Phase 2 — Sentinel-2 Band Ablation Study

A series of controlled experiments investigated the contribution of different spectral groups:

| Configuration |
|----------|
| RGB |
| RGB + NIR |
| RGB + RedEdge + NIR |
| RGB + RedEdge + NIR + SWIR |
| Physical Surface Bands |
| Full13 Without B10 |
| Full13 |

The objective was to identify the most informative spectral combinations and quantify the value of additional bands.

#### Phase 3 — Reliability and Explainability Analysis

Beyond classification accuracy, the framework evaluates:

- Confidence calibration
- Reliability diagrams
- Expected Calibration Error (ECE)
- Prediction confidence distributions
- Grad-CAM visual explanations
- High-confidence failure cases
- Spectral sensitivity through band-ablation experiments

This enables a more comprehensive assessment of model trustworthiness and practical deployment suitability.

## Project Evolution and Results Organization

The TerraSight project was originally designed as a staged research framework consisting of four progressive development phases.

### V1 — Assessment Compliance

This phase established the mandatory project foundation and assessment requirements, including:

- EuroSAT dataset preparation
- RGB baseline model
- Multispectral classification model
- Reproducible train/test split
- Training and evaluation pipelines
- Configuration-driven experiments
- Experiment tracking and reporting

The outputs of this phase are stored in the baseline experiment results and form the foundation for all subsequent analyses.

### V2 — Scientific Experimental Validation

The objective of V2 was to strengthen the scientific rigor of the RGB-versus-multispectral comparison.

Implemented activities included:

- Experiment registry and tracking
- Class-wise performance analysis
- Confusion-matrix generation
- RGB-versus-multispectral comparison tables
- Structured result logging
- Comparative performance visualization
- Reproducibility verification

Rather than creating a separate `results/v2/` directory, these analyses were integrated directly into the reporting framework and generated from the baseline experiment outputs. Consequently, V2 primarily produced derived analytical artifacts rather than independent model-training runs.

Key V2 outputs include:

- RGB vs Multispectral comparison tables
- Class-wise performance analysis
- Confusion matrices
- Performance comparison figures
- Experiment registry (`experiments/registry.csv`)

### V3 — Reliability and Explainability

The goal of V3 was to investigate model trustworthiness beyond conventional accuracy metrics.

Implemented components include:

- Calibration analysis
- Expected Calibration Error (ECE)
- Reliability diagrams
- Confidence-distribution analysis
- High-confidence failure analysis
- Grad-CAM visual explanations
- Confusion-pair explainability analysis
- Spectral attribution and band-importance analysis
- Robustness and perturbation experiments

These analyses operate on trained models generated during V1 and V4 rather than producing new standalone training results. Therefore, V3 outputs are organized within dedicated reporting directories instead of a separate `results/v3/` experiment directory.

Key V3 outputs include:

- Reliability diagrams
- Confidence histograms
- Grad-CAM visualizations
- High-confidence failure analyses
- Spectral attribution results
- Robustness analyses
- Calibration metrics

### V4 — Spectral Analysis and Advanced Evaluation

The final phase focused on understanding the contribution of Sentinel-2 spectral information through controlled experiments.

Implemented activities include:

- Sentinel-2 band-ablation studies
- Spectral subset evaluation
- RGB versus multispectral comparisons
- Spectral sensitivity analysis
- Robustness-based band importance estimation
- Advanced scientific interpretation

Because V4 introduced new model-training experiments and generated substantial independent outputs, these results are stored in dedicated experiment directories and constitute the largest experimental component of the project.

## Why There Are No Dedicated `results/v2` and `results/v3` Directories

V2 and V3 primarily represent analytical and evaluation stages rather than independent model-development stages.

Their outputs are derived from models trained during V1 and V4 and are therefore stored within:

```text
reports/figures/
reports/tables/
```

## Repository Structure

```text
terrasight-eurosat-rgb-vs-multispectral/
├── configs/            # Experiment configurations
├── dataset/            # Dataset metadata and preparation
├── docs/               # Extended analyses and documentation
├── experiments/        # Experiment registry and tracking
├── reports/            # Figures, tables, and generated outputs
├── results/            # Model outputs and evaluation results
├── scripts/            # Training and evaluation scripts
├── src/                # Core source code
├── tests/              # Automated tests
└── README.md
```

# Experimental Results

This section presents the empirical evaluation of RGB and multispectral deep-learning models on the EuroSAT benchmark. The experiments investigate three key aspects:

1. The effectiveness of RGB versus multispectral imagery.
2. The impact of transfer learning.
3. The contribution of individual Sentinel-2 spectral groups through controlled band-ablation studies.

## V1: RGB vs Multispectral Comparison

The first experimental phase compares RGB and multispectral ResNet18 models trained using both transfer learning and random initialization.

### Model Comparison

| Model | Accuracy (%) | Macro-F1 (%) | Balanced Accuracy (%) |
|---------|---------:|---------:|---------:|
| RGB ResNet18 (Pretrained) | **97.46** | **97.45** | **97.45** |
| RGB ResNet18 (Scratch) | 95.17 | 95.11 | 95.10 |
| Multispectral ResNet18 (Adapted Pretrained) | 95.46 | 95.37 | 95.36 |
| Multispectral ResNet18 (Scratch) | 93.20 | 92.99 | 93.09 |

![V1 RGB vs Multispectral Comparison](reports/figures/v1_model_comparison.png)

**Figure 4.** Performance comparison between RGB and multispectral baseline models. Transfer learning substantially improves both RGB and multispectral performance.

### Key Findings

- Transfer learning consistently outperformed training from scratch.
- The RGB pretrained model achieved the highest overall classification performance.
- Adapting pretrained RGB weights to multispectral inputs significantly improved multispectral performance.
- Multispectral training from scratch produced the weakest results, highlighting the importance of pretrained initialization.

### Training Dynamics

Representative training and validation curves for the best RGB and multispectral models are shown below.

<table>
<tr>
<td align="center" width="50%">

**RGB (ImageNet-pretrained ResNet18)**

<img src="reports/figures/20260613_113317_v1_rgb_resnet18_seed42_loss_curve.png" width="100%">

</td>

<td align="center" width="50%">

**Multispectral (Adapted Pretrained ResNet18)**

<img src="reports/figures/20260614_061742_v1_multispectral_resnet18_adapted_seed42_loss_curve.png" width="100%">

</td>
</tr>
</table>

**Figure 5.** Representative training and validation curves demonstrating stable optimization and convergence behaviour.

## Class-Level Performance Analysis

While overall accuracy is informative, class-level analysis provides deeper insight into the strengths and weaknesses of each model.

### Best RGB Model

![RGB Confusion Matrix](reports/figures/confusion_matrices/v1_rgb_resnet18_seed42_confusion_matrix.png)

**Figure 6.** Confusion matrix for the best-performing RGB model.

### Best Multispectral Model

![Multispectral Confusion Matrix](reports/figures/confusion_matrices/v1_multispectral_resnet18_adapted_seed42_confusion_matrix.png)

**Figure 7.** Confusion matrix for the best-performing multispectral model.

### Per-Class Performance Analysis

While aggregate metrics provide an overall assessment of model quality, class-level performance analysis reveals how different spectral configurations affect individual land-cover categories.

![Per-Class F1 Comparison](reports/figures/per_class_f1_comparison.png)

**Figure 8.** Per-class F1-score comparison across all evaluated spectral configurations. The figure illustrates how Sentinel-2 band selection influences classification performance for individual EuroSAT classes.

### Interpretation

Several important observations emerge from the class-level analysis.

#### 1. Water and Urban Classes Are Consistently Easy to Classify

The highest F1 scores are achieved for:

- SeaLake
- Residential
- Forest
- River

These classes exhibit distinctive spatial structures and spectral characteristics, allowing all spectral configurations to achieve strong performance.

In particular, **SeaLake** consistently achieves F1 scores above 0.98 across nearly all configurations, indicating excellent separability.

#### 2. Agricultural Classes Remain the Most Challenging

The lowest F1 scores occur for:

- PermanentCrop
- HerbaceousVegetation
- AnnualCrop
- Pasture

These categories contain similar vegetation structures, crop textures, and seasonal characteristics, resulting in substantial class overlap.

Among all classes, **PermanentCrop** remains the most difficult category, with F1 scores approximately 7–10 percentage points lower than the best-performing classes.

#### 3. Multispectral Information Benefits Vegetation-Related Classes

The largest improvements from multispectral information are observed for:

- PermanentCrop
- HerbaceousVegetation
- AnnualCrop
- River

Adding RedEdge, NIR, and SWIR information improves discrimination between vegetation-dominated classes that are difficult to separate using RGB information alone.

This behaviour is consistent with the physical interpretation of Sentinel-2 bands, where:

- RedEdge bands capture vegetation condition and chlorophyll content;
- NIR bands capture vegetation reflectance structure;
- SWIR bands provide moisture and surface-composition information.

#### 4. RGB + RedEdge + NIR + SWIR Provides the Most Consistent Performance

The best-performing multispectral configuration:

```text
RGB + RedEdge + NIR + SWIR
```

achieves strong performance across nearly all classes and avoids the performance degradation observed in some Full13 experiments.

Notably, this configuration improves:

- PermanentCrop
- Residential
- SeaLake
- River

while maintaining competitive performance for all remaining categories.

#### 5. More Bands Do Not Necessarily Improve Performance

The Full13 and Full13NoB10 configurations do not consistently outperform the reduced-band configurations.

Several classes achieve equal or better performance using:

```text
RGB + RedEdge + NIR + SWIR
```

than with the complete Sentinel-2 spectral stack.

This observation supports the central finding of the project:

> Spectral selection is more important than spectral quantity.

### Scientific Implications

The per-class analysis demonstrates that multispectral information does not benefit all land-cover categories equally.

The largest gains occur in vegetation-related classes where spectral reflectance differences provide information that is unavailable in RGB imagery. Conversely, classes with highly distinctive spatial structures, such as SeaLake and Residential, already achieve near-ceiling performance with RGB information alone.

These findings suggest that the primary value of multispectral imagery lies in improving discrimination between spectrally similar vegetation and agricultural categories rather than uniformly improving performance across all classes.

#### Overfitting Assessment

The training dynamics do not indicate severe overfitting. Both the RGB-pretrained and adapted multispectral models exhibit stable convergence behaviour, with training and validation losses decreasing consistently throughout optimization.

The validation curves closely follow the training curves, suggesting good generalization to unseen data. Early stopping was employed during training to prevent unnecessary optimization after validation performance ceased improving.

A mild overfitting pattern was observed in the Full13 multispectral configuration during the band-ablation study, where validation loss reached its minimum early and subsequently increased. This behaviour suggests that incorporating all available Sentinel-2 bands may introduce redundant or less informative spectral information.

In contrast, the best-performing spectral subset (RGB + RedEdge + NIR + SWIR) demonstrated stable convergence and superior generalization performance. These findings support the conclusion that careful spectral-band selection not only improves classification accuracy but may also reduce overfitting risk compared with using the complete Sentinel-2 spectral stack.

To improve generalization, training employed data augmentation, transfer learning, and early stopping. Because the validation curves did not exhibit severe overfitting, additional regularization techniques such as dropout were not required.

## V4: Sentinel-2 Band Ablation Study

To determine which spectral information contributes most effectively to land-cover classification, a series of controlled band-ablation experiments was performed.

### Evaluated Spectral Configurations

| Configuration | Included Bands |
|----------|----------|
| RGB | B2, B3, B4 |
| RGB + NIR | RGB + B8, B8A |
| RGB + RedEdge + NIR | RGB + B5–B8A |
| RGB + RedEdge + NIR + SWIR | RGB + B5–B12 |
| Physical Surface Bands | Surface-related Sentinel-2 bands |
| Full13 Without B10 | All bands except cirrus band |
| Full13 | All Sentinel-2 bands |

### Ablation Results

| Configuration | Accuracy (%) | Macro-F1 (%) |
|----------|---------:|---------:|
| RGB | 94.94 | 94.86 |
| RGB + NIR | 95.21 | 95.12 |
| RGB + RedEdge + NIR | 95.52 | 95.41 |
| RGB + RedEdge + NIR + SWIR | **95.67** | **95.56** |
| Physical Surface Bands | 94.73 | 94.60 |
| Full13 Without B10 | 95.33 | 95.24 |
| Full13 | 95.47 | 95.38 |

![Band Ablation Comparison](reports/figures/v4_band_ablation_comparison.png)

**Figure 9.** Comparison of spectral configurations evaluated during the Sentinel-2 band-ablation study.

### Key Findings

The ablation study reveals several important observations:

1. Adding NIR information improves performance over RGB alone.
2. RedEdge bands provide additional gains for vegetation-related classes.
3. SWIR information further improves discrimination of complex land-cover types.
4. The best-performing configuration is **RGB + RedEdge + NIR + SWIR**.
5. Using all available Sentinel-2 bands does not necessarily produce the best performance.

These findings support the conclusion that **spectral selection is more important than spectral quantity**.

## Spectral Separability Analysis

To quantitatively assess the physical distinguishability of EuroSAT land-cover classes, pairwise class separability was evaluated using two complementary remote-sensing metrics:

1. **Bhattacharyya Distance (BD)** – measures statistical separation between class distributions using class means and covariance structures.
2. **Spectral Angle Mapper (SAM)** – measures spectral similarity by computing the angle between mean spectral signatures.

Together, these analyses provide a physical explanation for the observed classification performance, confusion patterns, and the effectiveness of multispectral information.

### Bhattacharyya Distance Analysis

Figure 10 presents the pairwise Bhattacharyya distance matrix for all EuroSAT classes.

![Bhattacharyya Distance Heatmap](reports/figures/spectral_analysis/bhattacharyya_heatmap.png)
**Figure 10**. The pairwise Bhattacharyya distance matrix for all EuroSAT classes

Higher values indicate stronger statistical separation and therefore easier classification, whereas lower values indicate classes that are more difficult to distinguish.

#### Most Separable Class Pairs

| Class Pair | Bhattacharyya Distance |
|------------|----------------------:|
| Pasture vs SeaLake | 22.73 |
| PermanentCrop vs SeaLake | 22.70 |
| AnnualCrop vs SeaLake | 17.75 |
| Residential vs SeaLake | 12.84 |
| Highway vs SeaLake | 12.81 |

The results demonstrate that **SeaLake** is by far the most distinctive class in the dataset. Water exhibits a spectral response that differs substantially from vegetation, urban infrastructure, and agricultural land-cover types, resulting in very large separability values.

This finding is consistent with the classification experiments, where water-related classes achieved some of the highest F1 scores and exhibited minimal confusion with other categories.

#### Least Separable Class Pairs

| Class Pair | Bhattacharyya Distance |
|------------|----------------------:|
| Industrial vs Residential | 0.97 |
| Highway vs River | 1.04 |
| Highway vs PermanentCrop | 1.20 |
| AnnualCrop vs Highway | 1.41 |
| Highway vs Residential | 1.43 |

![Least Separable Pairs](reports/figures/spectral_analysis/top10_least_separable_pairs_bhattacharyya.png)
**Figure 11**. Top-10 least separable pairs based on Bhattacharyya distance

These results indicate that several urban and transportation-related classes possess highly overlapping spectral distributions. In particular, **Industrial**, **Residential**, and **Highway** classes exhibit limited statistical separation, explaining many of the observed classification errors.

### Spectral Angle Mapper Analysis

Figure 12 presents pairwise spectral similarity measured using Spectral Angle Mapper.

![Spectral Angle Heatmap](reports/figures/spectral_analysis/spectral_angle_heatmap.png)
**Figure 12**. Pairwise spectral similarity using Spectral Angle Mapper

SAM evaluates the angular difference between mean spectral signatures and is less sensitive to illumination intensity than Euclidean distance measures.

#### Most Spectrally Different Class Pairs

| Class Pair | SAM (degrees) |
|------------|--------------:|
| Pasture vs SeaLake | 52.14 |
| Forest vs SeaLake | 51.76 |
| AnnualCrop vs SeaLake | 48.23 |
| PermanentCrop vs SeaLake | 47.67 |
| HerbaceousVegetation vs SeaLake | 46.86 |

![Most Spectrally Different Pairs](reports/figures/spectral_analysis/top10_most_different_pairs_sam.png)
**Figure 13**. Top-10 most different pairs

Again, **SeaLake** emerges as the most physically distinct class. The large spectral angles indicate that water exhibits fundamentally different reflectance behaviour across Sentinel-2 bands compared with vegetation and built environments.

#### Most Spectrally Similar Class Pairs

| Class Pair | SAM (degrees) |
|------------|--------------:|
| AnnualCrop vs PermanentCrop | 2.87 |
| Forest vs Pasture | 3.63 |
| HerbaceousVegetation vs PermanentCrop | 3.81 |
| AnnualCrop vs Highway | 3.87 |
| PermanentCrop vs Residential | 4.56 |

![Most Spectrally Similar Pairs](reports/figures/spectral_analysis/top10_most_similar_pairs_sam.png)
**Figure 14**. Top-10 most similar pairs

The smallest spectral angle was observed between **AnnualCrop** and **PermanentCrop**, indicating extremely similar spectral signatures. This finding provides a physical explanation for the confusion frequently observed among vegetation-related classes.

### Relationship to Classification Performance

The separability analysis provides strong evidence that classification performance is closely linked to the intrinsic spectral characteristics of the underlying land-cover classes.

Several important observations emerge:

1. **SeaLake** exhibits exceptionally large Bhattacharyya distances and SAM angles relative to nearly all other classes, explaining its consistently strong classification performance.
2. **AnnualCrop**, **PermanentCrop**, **Pasture**, and **HerbaceousVegetation** exhibit relatively small spectral differences, making them inherently more challenging to distinguish.
3. Urban classes such as **Industrial**, **Residential**, and **Highway** also display limited separability, contributing to classification ambiguity.
4. The effectiveness of the selected **Red Edge**, **Near-Infrared (NIR)**, and **Short-Wave Infrared (SWIR)** bands is consistent with their ability to capture subtle vegetation and moisture differences that are not fully represented in RGB imagery.

### Key Finding

> Spectral separability analysis demonstrates that EuroSAT classification performance is strongly influenced by the intrinsic physical similarity of land-cover classes. Classes with large Bhattacharyya distances and spectral angles are reliably classified, whereas classes with highly similar spectral signatures produce the majority of classification errors. These findings provide a physical justification for the observed benefits of carefully selected multispectral bands, particularly for vegetation-related land-cover discrimination.

### Reproducibility

This analysis can be reproduced using:

```bash
python -m terrasight.reporting.generate_spectral_separability --data-dir <MULTISPECTRAL_DATASET_DIR> --tables-dir reports/tables/spectral_analysis --figures-dir reports/figures/spectral_analysis
```

Generated outputs:

```text
reports/tables/spectral_analysis/class_mean_signatures.csv
reports/tables/spectral_analysis/bhattacharyya_distances.csv
reports/tables/spectral_analysis/spectral_angles.csv
reports/tables/spectral_analysis/pairwise_spectral_separability.csv

reports/figures/spectral_analysis/bhattacharyya_heatmap.png
reports/figures/spectral_analysis/spectral_angle_heatmap.png
reports/figures/spectral_analysis/top10_least_separable_pairs_bhattacharyya.png
reports/figures/spectral_analysis/top10_most_separable_pairs_bhattacharyya.png
reports/figures/spectral_analysis/top10_most_similar_pairs_sam.png
reports/figures/spectral_analysis/top10_most_different_pairs_sam.png
```


## Statistical Validation

To determine whether the performance improvement produced by the **RGB + RedEdge + NIR + SWIR** configuration was statistically meaningful, paired prediction-level statistical testing was performed.

Because both models were evaluated on the same fixed test set, paired statistical procedures provide a more rigorous assessment than comparing aggregate metrics alone.

### Bootstrap Confidence Intervals

Bootstrap resampling (1,000 iterations) was used to estimate confidence intervals for performance differences between the RGB baseline and the best-performing multispectral configuration.

| Metric | Mean Difference (%) | 95% Confidence Interval |
|----------|----------:|----------|
| Accuracy | +0.706 | [-0.019, 1.352] |
| Macro-F1 | +0.740 | [0.011, 1.412] |
| Balanced Accuracy | +0.653 | [-0.073, 1.324] |

The Macro-F1 confidence interval excludes zero, indicating statistically meaningful improvement in class-balanced classification performance. In contrast, the confidence intervals for Accuracy and Balanced Accuracy overlap zero, suggesting that the strongest evidence of improvement is observed in class-balanced performance rather than aggregate accuracy alone.

### McNemar Significance Test

McNemar's test was applied to paired predictions to determine whether the multispectral model corrected significantly more RGB errors than it introduced.

| Quantity | Value |
|----------|------:|
| RGB Correct / Multispectral Wrong | 137 |
| RGB Wrong / Multispectral Correct | 176 |
| McNemar Statistic | 4.613 |
| p-value | 0.0317 |

Because *p* < 0.05, the difference is statistically significant at the 95% confidence level.

### Multi-Seed Validation Scope

Multi-seed evaluation was performed only for the strongest selected configurations rather than for every experiment in the full benchmark. Specifically, the best-performing configuration from the seed-42 experiments was repeated using additional random seeds 43 and 44 to assess training stability.

Therefore, the multi-seed results should be interpreted as a robustness check for the selected best model, not as a complete multi-seed comparison across all experimental configurations.

### Interpretation

Three important conclusions emerge:

1. The RGB + RedEdge + NIR + SWIR configuration shows improved performance relative to the RGB baseline, with the strongest statistical evidence observed for Macro-F1.
2. The strongest statistical evidence of improvement is observed in **Macro-F1**, indicating better class-balanced discrimination across EuroSAT land-cover categories.
3. McNemar's test indicates that the multispectral model corrected significantly more RGB classification errors than it introduced (p = 0.0317), providing paired-sample evidence that the observed improvement is unlikely to be attributable to random variation alone.

### Scientific Implications

The statistical analysis provides quantitative evidence supporting the central hypothesis of this project: carefully selected multispectral information contributes complementary discriminative information beyond RGB imagery.

Importantly, the results do **not** support the claim that simply increasing the number of spectral bands improves performance. Instead, they demonstrate that a targeted combination of **RedEdge**, **Near-Infrared (NIR)**, and **Short-Wave Infrared (SWIR)** bands provides measurable and statistically significant benefits when integrated with RGB information.

### Key Finding

> Carefully selected multispectral information provides statistically significant improvements beyond RGB imagery, particularly for balanced land-cover classification performance. These findings strengthen the conclusion that **spectral selection is more important than spectral quantity** for EuroSAT land-cover classification.

These results strengthen the reliability of the reported conclusions by demonstrating that the observed improvements are unlikely to be explained by random variation alone.

---
### Reproducibility and Generated Outputs

Statistical results can be reproduced using:

```bash
python -m terrasight.reporting.statistical_analysis \
  --model-a reports/tables/probabilities/<MODEL_A_PROBABILITIES>.csv \
  --model-b reports/tables/probabilities/<MODEL_B_PROBABILITIES>.csv \
  --model-a-name "<MODEL_A_NAME>" \
  --model-b-name "<MODEL_B_NAME>" \
  --output reports/tables/statistical_tests/statistical_analysis.csv \
  --summary reports/tables/statistical_tests/statistical_summary.md \
  --bootstrap 1000 \
  --seed 42
```

Generated outputs:

```text
reports/tables/statistical_tests/statistical_analysis.csv
reports/tables/statistical_tests/statistical_summary.md
```


## Reliability and Calibration Analysis

Accurate predictions alone are insufficient for practical deployment. Models should also provide reliable confidence estimates.

### Expected Calibration Error (ECE)

| Model | ECE ↓ |
|----------|----------:|
| RGB Pretrained (V1) | 0.0075 |
| RGB Scratch (V1) | 0.0231 |
| Multispectral Adapted (V1) | 0.0269 |
| Multispectral Scratch (V1) | 0.0385 |
| RGB + RedEdge + NIR + SWIR (V4) | **0.0039** |
| Full13 (V4) | 0.0050 |

The results show that transfer learning substantially improves calibration quality. The best-performing multispectral configuration achieved the lowest Expected Calibration Error, indicating excellent agreement between predicted confidence and empirical accuracy.

![Reliability Diagram](reports/figures/reliability/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_reliability_diagram.png)

**Figure 15.** Reliability diagram for the best-performing multispectral model. The curve closely follows the ideal calibration line, resulting in very low calibration error.

### Interpretation

The RGB + RedEdge + NIR + SWIR model achieved both:

- Highest multispectral classification performance.
- Best confidence calibration.

This suggests that the model is not only accurate but also trustworthy in terms of confidence estimation.

---

## Prediction Confidence Analysis

To evaluate model certainty, confidence histograms were generated from softmax prediction probabilities.

| RGB Baseline | Multispectral Baseline |
|:---:|:---:|
| ![](reports/figures/reliability/v1_rgb_resnet18_seed42_confidence_histogram.png) | ![](reports/figures/reliability/v1_multispectral_resnet18_adapted_seed42_confidence_histogram.png) |
| **(a)** RGB Pretrained | **(b)** Multispectral Adapted |

| Full13 | RGB + RedEdge + NIR |
|:---:|:---:|
| ![](reports/figures/reliability/v4_ablation_full13_resnet18_pretrained_adapted_seed42_confidence_histogram.png) | ![](reports/figures/reliability/v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42_confidence_histogram.png) |
| **(c)** Full13 | **(d)** RGB + RedEdge + NIR |

**Figure 16.** Confidence distributions for representative RGB and multispectral models.

### Interpretation

Several consistent patterns emerge:

- Most predictions have confidence values above 0.95.
- Multispectral models exhibit slightly sharper confidence distributions than RGB-only models.
- Reduced-band configurations achieve confidence distributions comparable to Full13 models.
- Carefully selected spectral subsets preserve most discriminative information while reducing input dimensionality.

## Summary of Experimental Findings

The experimental results support four primary conclusions:

1. **Transfer learning is essential** for achieving strong performance in both RGB and multispectral settings.

2. **RGB pretrained models remain extremely competitive**, achieving the highest overall classification accuracy.

3. **Multispectral information provides complementary value**, particularly when combining RGB, RedEdge, NIR, and SWIR bands.

4. **Spectral selection is more important than spectral quantity**, as carefully chosen subsets outperform full-band configurations.

The following sections investigate model reliability, explainability, robustness, and failure modes in greater detail.

## V5: Supplementary Architecture Benchmark Experiments

To investigate whether classification performance can be further improved through architectural scaling, a supplementary set of experiments was conducted using larger ImageNet-pretrained CNN architectures.

Unlike the V1–V4 experiments, which focused on the scientific value of multispectral information and Sentinel-2 band selection, these experiments evaluate the impact of network architecture while keeping the input modality fixed to RGB imagery.

### Evaluated Architectures

| Model | Input | Pretrained |
|---------|---------|---------|
| ResNet18 | RGB | Yes |
| ResNet50 | RGB | Yes |
| EfficientNet-B0 | RGB | Yes |
| EfficientNet-B2 | RGB | Yes |

### Results

| Model | Accuracy (%) | Macro-F1 (%) | Balanced Accuracy (%) |
|---------|---------:|---------:|---------:|
| ResNet18 | 97.46 | 97.45 | 97.45 |
| ResNet50 | 97.39 | 97.36 | 97.30 |
| EfficientNet-B0 | **98.39** | 98.32 | 98.25 |
| EfficientNet-B2 | **98.39** | **98.34** | **98.34** |

### Key Findings

Several important observations emerge:

1. Simply increasing model depth from ResNet18 to ResNet50 does not improve performance on EuroSAT.
2. EfficientNet architectures substantially outperform both ResNet18 and ResNet50.
3. EfficientNet-B0 achieves approximately 1% absolute accuracy improvement over the strongest ResNet models.
4. EfficientNet-B2 provides the highest overall Macro-F1 and Balanced Accuracy.
5. The performance difference between EfficientNet-B0 and EfficientNet-B2 is relatively small, suggesting diminishing returns from additional model scaling.

### Interpretation

These supplementary experiments demonstrate that architectural choice can have a larger impact on classification accuracy than increasing network depth within the ResNet family.

The results indicate that EfficientNet's compound scaling strategy provides a more effective use of model capacity for EuroSAT land-cover classification than conventional ResNet scaling.

Importantly, these experiments were performed using RGB imagery only. Therefore, the V5 results should be interpreted as an architecture benchmark rather than a multispectral analysis.

### Practical Implication

For applications where maximizing classification accuracy is the primary objective, EfficientNet-B0 and EfficientNet-B2 represent strong deployment candidates.

However, the central scientific conclusions of this project remain unchanged:

> Spectral selection is more important than spectral quantity, and carefully chosen multispectral bands provide complementary information beyond RGB imagery.

# Explainability, Robustness, Reproducibility, and Deployment

This section investigates model behaviour beyond classification accuracy, focusing on explainability, robustness, reproducibility, and practical deployment considerations.

---

## Explainability Analysis

Understanding why a model makes a prediction is particularly important in remote-sensing applications where decisions may influence environmental monitoring, land-use assessment, agricultural planning, and policy-making.

To investigate model behaviour, Grad-CAM (Gradient-weighted Class Activation Mapping) was used to visualize the spatial regions that contribute most strongly to model predictions.

### Grad-CAM Analysis

Representative Grad-CAM visualizations are shown below.

![Grad-CAM Examples](reports/figures/gradcam/gradcam_summary.png)

**Figure 17.** Representative Grad-CAM visualizations showing regions that contribute most strongly to model predictions.

### Key Observations

Several consistent patterns emerge:

1. The model typically focuses on semantically meaningful regions rather than background noise.

2. Vegetation-related classes often activate on homogeneous vegetation structures and field patterns.

3. Urban classes activate on dense built-up regions, road networks, and man-made structures.

4. Water-related classes activate primarily on river and lake boundaries.

These observations suggest that the learned representations capture meaningful land-cover characteristics rather than relying on spurious correlations.

### Interpretation

Grad-CAM visualizations indicate that the model frequently attends to regions that are consistent with human interpretation of the scene.

While Grad-CAM does not provide causal explanations, it offers useful qualitative evidence that the classifier relies on semantically relevant image content.

---
## Spectral Attribution and Band Importance Analysis

To better understand how individual Sentinel-2 spectral bands contribute to model predictions, an occlusion-based spectral attribution analysis was performed on the best-performing multispectral configuration:

```text
RGB + RedEdge + NIR + SWIR
```

The analysis systematically removes individual spectral bands and measures the resulting reduction in prediction confidence and prediction stability.

### Global Band Importance

The overall importance ranking obtained from the band-occlusion analysis is shown below.

| Rank | Band | Mean Confidence Drop | Prediction Change Rate |
|--------:|--------|--------:|--------:|
| 1 | B3 (Green) | 0.519 | 54.81% |
| 2 | B2 (Blue) | 0.283 | 29.20% |
| 3 | B4 (Red) | 0.210 | 21.00% |
| 4 | B11 (SWIR) | 0.027 | 3.74% |
| 5 | B8 (NIR) | 0.019 | 2.72% |
| 6 | B5 (RedEdge) | 0.012 | 2.43% |
| 7 | B12 (SWIR) | 0.008 | 1.93% |
| 8 | B7 (RedEdge) | 0.005 | 1.63% |
| 9 | B8A (Narrow NIR) | 0.002 | 1.02% |
| 10 | B6 (RedEdge) | 0.002 | 1.19% |

### Interpretation

Several important observations emerge from the analysis:

1. The RGB bands remain the dominant source of predictive information.
2. The Green band (B3) is by far the most influential spectral channel, causing prediction changes in more than half of all test samples when removed.
3. Blue (B2) and Red (B4) also contribute substantially to model performance.
4. Among the multispectral channels, SWIR (B11) and NIR (B8) provide the strongest complementary information.
5. RedEdge bands contribute useful but smaller improvements compared with RGB and SWIR channels.

These findings are consistent with the band-ablation experiments, which demonstrated that carefully selected spectral subsets outperform the complete Sentinel-2 spectral stack.

### Class-Specific Band Importance

The most informative bands vary across land-cover categories.

| Class | Top Bands |
|----------|----------|
| AnnualCrop | B3, B2, B11 |
| Forest | B4, B3, B2 |
| HerbaceousVegetation | B3, B4, B2 |
| Highway | B3, B2, B4 |
| Industrial | B3, B2, B4 |
| Pasture | B3, B2, B4 |
| PermanentCrop | B3, B2, B4 |
| Residential | B3, B2, B4 |
| River | B11, B3, B4 |
| SeaLake | B4, B2, B5 |

### Interpretation

The class-specific analysis reveals physically meaningful relationships between spectral bands and land-cover types:

- River is the only class for which SWIR (B11) becomes the most important band, reflecting the strong sensitivity of SWIR wavelengths to water content.
- SeaLake benefits from RedEdge information (B5), suggesting that shoreline and aquatic vegetation characteristics contribute to class discrimination.
- Agricultural and vegetation classes rely heavily on visible-spectrum information but still benefit from complementary multispectral cues.
- Urban classes such as Residential and Industrial remain primarily driven by RGB texture and structural information.

### Sample-Level Spectral Attribution

A sample-level attribution analysis was performed on representative test images.

Across the analyzed samples:

- B3 (Green) was identified as the most influential band in 13 of 20 cases.
- B2 (Blue) was the most influential band in 5 of 20 cases.
- B4 (Red) was the most influential band in 2 of 20 cases.

This consistency further supports the conclusion that visible-spectrum information remains the primary driver of classification performance, while multispectral channels provide targeted complementary information that improves discrimination among challenging classes.

### Key Finding

> The results indicate that multispectral information is valuable not because every additional band contributes equally, but because a small number of carefully selected spectral channels provide complementary information unavailable in RGB imagery. In particular, SWIR and NIR bands improve discrimination of challenging vegetation and water-related classes, while RGB bands remain the dominant source of predictive information.

## Per-Class Spectral Signature Analysis

To better understand the physical characteristics of the EuroSAT classes and to provide an interpretable connection between Sentinel-2 spectral bands and classification performance, a per-class spectral signature analysis was performed.

For each class, the mean reflectance was computed across all images and all pixels for every Sentinel-2 spectral band. The resulting spectral profiles summarize the characteristic spectral behaviour of each land-cover category.

### Global Spectral Signature Comparison

![Per-Class Spectral Signatures](reports/figures/spectral_signatures/per_class_spectral_signatures.png)

**Figure 18.** Mean Sentinel-2 spectral signatures for all EuroSAT land-cover classes. Shaded regions represent one standard deviation around the mean.

### Interpretation

Several physically meaningful patterns emerge:

#### Vegetation Classes

The vegetation-related categories:

- Forest
- Pasture
- AnnualCrop
- PermanentCrop
- HerbaceousVegetation

show the characteristic vegetation spectral response:

- relatively low reflectance in the visible bands (B2–B4),
- a strong increase through the RedEdge region (B5–B7),
- high reflectance in the Near Infrared bands (B8 and B8A),
- elevated responses in SWIR bands (B11 and B12).

### Interpretation

Several physically meaningful patterns emerge from the per-class spectral signatures.

#### Vegetation Classes

Vegetation-related categories such as Forest, Pasture, AnnualCrop, PermanentCrop, and HerbaceousVegetation show the characteristic vegetation spectral response:

* relatively low reflectance in visible bands due to chlorophyll absorption;
* a sharp increase across the RedEdge region;
* high reflectance in Near-Infrared bands due to internal leaf structure;
* class-dependent variation in SWIR bands related to moisture content and surface composition.

This behaviour explains why RedEdge, NIR, and SWIR bands improve discrimination among vegetation and agricultural classes that are difficult to separate using RGB imagery alone.

#### Water-Related Classes

SeaLake and River exhibit spectral behaviour that differs strongly from vegetation and built-up classes. Their lower NIR and SWIR responses are consistent with the absorption characteristics of water, explaining their high spectral separability and strong classification performance.

#### Built-Up and Infrastructure Classes

Residential, Industrial, and Highway classes show more mixed spectral behaviour because they contain combinations of impervious surfaces, vegetation, shadows, and surrounding context. This helps explain residual confusion between urban and transportation-related categories.

Overall, the spectral signature analysis supports the central conclusion of this project: multispectral information is most valuable when selected according to physically meaningful spectral properties rather than by using all available bands indiscriminately.


## High-Confidence Failure Analysis

Although the best-performing model achieves strong overall performance, understanding its failures provides valuable insight into remaining challenges.

![High-Confidence Failures](reports/figures/failure_cases/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_high_confidence_failures.png)

**Figure 19.** Representative high-confidence misclassifications produced by the best-performing multispectral model.

### Key Observations

Most failures occur between semantically similar classes, including:

- AnnualCrop ↔ PermanentCrop
- Pasture ↔ HerbaceousVegetation
- River ↔ Vegetation Classes
- Highway ↔ Industrial

These classes often exhibit similar spatial textures, vegetation patterns, and spectral signatures.

### Interpretation

The failure analysis suggests that:

1. Many remaining errors arise from intrinsic dataset ambiguity.
2. Most misclassifications occur between related land-cover categories.
3. Completely unrelated class confusions are rare.
4. Confidence calibration remains important because some incorrect predictions receive very high confidence scores.

Overall, the failure cases indicate limitations of the dataset taxonomy and class separability rather than catastrophic model behaviour.

---
## Feature Space Analysis (t-SNE and UMAP)

To better understand how different models organize semantic information internally, we visualized the learned feature embeddings from the penultimate layer using **t-distributed Stochastic Neighbor Embedding (t-SNE)** and **Uniform Manifold Approximation and Projection (UMAP)**.

Feature vectors were extracted from the final encoder representation immediately before the classification head and projected into two dimensions. Two visualization modes are provided:

1. **By Class** – points colored according to ground-truth land-cover category.
2. **By Correctness** – correctly classified samples versus misclassified samples.

### Why Feature-Space Analysis Matters

Unlike accuracy metrics, feature-space visualizations reveal:

- Class separability in latent space.
- Inter-class confusion patterns.
- Cluster compactness and intra-class variability.
- Representation quality learned by different architectures.
- Locations where misclassifications occur.
- Whether additional spectral bands improve semantic discrimination.

A high-quality representation is characterized by:

- Compact intra-class clusters.
- Large inter-class separation.
- Few samples near cluster boundaries.
- Misclassified samples concentrated at cluster interfaces.

---

# V1 RGB ResNet18 Baseline

### t-SNE Projection

#### By Class

![V1 RGB ResNet18 t-SNE by Class](reports/figures/feature_space/v1_rgb_resnet18_seed42_tsne_by_class.png)
**Figure 20**. T-SNE per class visualization of V1 rgb resnet18 baseline model 

#### By Correctness

![V1 RGB ResNet18 t-SNE by Correctness](reports/figures/feature_space/v1_rgb_resnet18_seed42_tsne_by_correctness.png)
**Figure 21**. T-SNE by correctness visualization of V1 rgb resnet18 baseline model 

### UMAP Projection

#### By Class

![V1 RGB ResNet18 UMAP by Class](reports/figures/feature_space/v1_rgb_resnet18_seed42_umap_by_class.png)
**Figure 22**. UMAP per class visualization of V1 rgb resnet18 baseline model 

#### By Correctness

![V1 RGB ResNet18 UMAP by Correctness](reports/figures/feature_space/v1_rgb_resnet18_seed42_umap_by_correctness.png)
**Figure 23**. UMAP by correctness visualization of V1 rgb resnet18 baseline model 

### Interpretation

The RGB baseline already learns highly discriminative representations.

Key observations:

- Most EuroSAT classes form distinct and compact clusters.
- SeaLake, Forest, Residential, Highway, and Industrial are particularly well separated.
- Misclassified samples occur primarily near cluster boundaries.
- Very few outliers appear deep inside foreign clusters.
- The latent space demonstrates that even RGB imagery contains sufficient information for strong land-cover discrimination.

The correctness plots confirm that classification errors are not random; they occur predominantly in regions where semantic similarity between classes is highest.

---

# V4 RGB + RedEdge + NIR + SWIR (Best Spectral Ablation)

### t-SNE Projection

#### By Class

![V4 RGB+RedEdge+NIR+SWIR t-SNE by Class](reports/figures/feature_space/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_tsne_by_class.png)
**Figure 24**. T-SNE per class visualization of V4 multispectral resnet18 adapted model 

#### By Correctness

![V4 RGB+RedEdge+NIR+SWIR t-SNE by Correctness](reports/figures/feature_space/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_tsne_by_correctness.png)
**Figure 25**. T-SNE by correctness visualization of V4 multispectral resnet18 adapted model

### UMAP Projection

#### By Class

![V4 RGB+RedEdge+NIR+SWIR UMAP by Class](reports/figures/feature_space/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_umap_by_class.png)
**Figure 26**. UMAP per class visualization of V4 multispectral resnet18 adapted model

#### By Correctness

![V4 RGB+RedEdge+NIR+SWIR UMAP by Correctness](reports/figures/feature_space/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_umap_by_correctness.png)
**Figure 27**. UMAP by correctness visualization of V4 multispectral resnet18 adapted model

### Interpretation

Adding physically meaningful spectral bands significantly improves latent-space organization.

Key observations:

- Clusters become more compact than the RGB baseline.
- Increased separation is observed between vegetation-related classes.
- Boundary overlap is reduced.
- Misclassified samples become more localized around a few ambiguous regions.
- The representation geometry appears smoother and more structured.

These results provide qualitative evidence that RedEdge, NIR, and SWIR bands contribute complementary information beyond RGB, improving semantic discrimination in the learned feature space.

---

# V5 EfficientNet-B0

### t-SNE Projection

#### By Class

![EfficientNet-B0 t-SNE by Class](reports/figures/feature_space/v5_rgb_efficientnet_b0_pretrained_seed42_tsne_by_class.png)
**Figure 28**. T-SNE per class visualization of V5 rgb efficientnet-b0 adapted model

#### By Correctness

![EfficientNet-B0 t-SNE by Correctness](reports/figures/feature_space/v5_rgb_efficientnet_b0_pretrained_seed42_tsne_by_correctness.png)
**Figure 29**. T-SNE by correctness visualization of V5 rgb efficientnet-b0 adapted model

### UMAP Projection

#### By Class

![EfficientNet-B0 UMAP by Class](reports/figures/feature_space/v5_rgb_efficientnet_b0_pretrained_seed42_umap_by_class.png)
**Figure 30**. UMAP per class visualization of V5 rgb efficientnet-b0 adapted model

#### By Correctness

![EfficientNet-B0 UMAP by Correctness](reports/figures/feature_space/v5_rgb_efficientnet_b0_pretrained_seed42_umap_by_correctness.png)
**Figure 31**. UMAP by correctness visualization of V5 rgb efficientnet-b0 adapted model

### Interpretation

EfficientNet-B0 produces highly structured representations despite its relatively small parameter count.

Key observations:

- Strong cluster compactness is observed.
- Most classes occupy well-defined manifolds.
- Several clusters become elongated, suggesting preservation of intra-class variability.
- Error samples remain concentrated near transition regions.
- Representation quality is competitive with larger architectures.

This indicates that EfficientNet-B0 achieves an excellent trade-off between model complexity and representation quality.

---

# V5 EfficientNet-B2

### t-SNE Projection

#### By Class

![EfficientNet-B2 t-SNE by Class](reports/figures/feature_space/v5_rgb_efficientnet_b2_pretrained_seed42_tsne_by_class.png)
**Figure 32**. T-SNE per class visualization of V5 rgb efficientnet-b2 adapted model

#### By Correctness

![EfficientNet-B2 t-SNE by Correctness](reports/figures/feature_space/v5_rgb_efficientnet_b2_pretrained_seed42_tsne_by_correctness.png)
**Figure 33**. T-SNE by correctness visualization of V5 rgb efficientnet-b2 adapted model

### UMAP Projection

#### By Class

![EfficientNet-B2 UMAP by Class](reports/figures/feature_space/v5_rgb_efficientnet_b2_pretrained_seed42_umap_by_class.png)
**Figure 34**. UMAP per class visualization of V5 rgb efficientnet-b2 adapted model

#### By Correctness

![EfficientNet-B2 UMAP by Correctness](reports/figures/feature_space/v5_rgb_efficientnet_b2_pretrained_seed42_umap_by_correctness.png)
**Figure 35**. UMAP by correctness visualization of V5 rgb efficientnet-b2 adapted model

### Interpretation

EfficientNet-B2 generates one of the cleanest feature spaces among all evaluated architectures.

Key observations:

- Very compact class clusters.
- Excellent inter-class separation.
- Minimal overlap between categories.
- Misclassified samples are sparse and localized.
- UMAP reveals nearly isolated semantic manifolds for each land-cover type.

The representation quality aligns closely with the model's strong classification performance.

---

# V5 ResNet50

### t-SNE Projection

#### By Class

![ResNet50 t-SNE by Class](reports/figures/feature_space/v5_rgb_resnet50_pretrained_seed42_tsne_by_class.png)
**Figure 36**. T-SNE per class visualization of V5 rgb efficientnet-b0 adapted model

#### By Correctness

![ResNet50 t-SNE by Correctness](reports/figures/feature_space/v5_rgb_resnet50_pretrained_seed42_tsne_by_correctness.png)
**Figure 37**. T-SNE by correctness visualization of V5 rgb resnet-50 adapted model

### UMAP Projection

#### By Class

![ResNet50 UMAP by Class](reports/figures/feature_space/v5_rgb_resnet50_pretrained_seed42_umap_by_class.png)
**Figure 38**. UMAP by per class visualization of V5 rgb resnet-50 adapted model

#### By Correctness

![ResNet50 UMAP by Correctness](reports/figures/feature_space/v5_rgb_resnet50_pretrained_seed42_umap_by_correctness.png)
**Figure 39**. UMAP by correctness visualization of V5 rgb resnet-50 adapted model

### Interpretation

ResNet50 learns highly discriminative high-dimensional representations that remain well separated after dimensionality reduction.

Key observations:

- Strong semantic clustering across all classes.
- Few ambiguous regions.
- Misclassified samples remain near cluster interfaces.
- The latent structure demonstrates robust feature extraction capabilities.
- Class manifolds are generally smooth and compact.

The results confirm that deeper residual networks can learn rich semantic embeddings even from relatively small remote-sensing image patches.

---

# Cross-Model Comparison

The feature-space visualizations reveal several important trends:

| Model | Cluster Separation | Cluster Compactness | Error Localization |
|---------|---------|---------|---------|
| V1 RGB ResNet18 | High | Moderate | Good |
| V4 RGB+RedEdge+NIR+SWIR | Very High | High | Very Good |
| EfficientNet-B0 | High | High | Good |
| EfficientNet-B2 | Excellent | Excellent | Excellent |
| ResNet50 | Excellent | Excellent | Excellent |

### Main Findings

1. All models learn meaningful semantic representations.
2. Spectral augmentation (RedEdge + NIR + SWIR) improves feature-space organization relative to RGB-only inputs.
3. EfficientNet-B2 and ResNet50 produce the most discriminative latent spaces.
4. Misclassified samples consistently occur near semantic boundaries, indicating that model errors are primarily driven by class ambiguity rather than representation failure.
5. The strong separation observed in both t-SNE and UMAP projections provides qualitative support for the quantitative performance metrics reported in earlier sections.

Overall, the feature-space analysis confirms that the proposed TerraSight pipeline learns robust and semantically meaningful representations for EuroSAT land-cover classification.


## Robustness Analysis

Robustness experiments evaluate how model performance changes under controlled perturbations designed to simulate realistic remote-sensing conditions.

The best-performing multispectral model:

```text
RGB + RedEdge + NIR + SWIR
````

was subjected to several perturbation types.

### Noise and Illumination Robustness

| Perturbation        | Accuracy Drop | Macro-F1 Drop |
| ------------------- | ------------: | ------------: |
| Gaussian Noise      |         0.33% |         0.33% |
| Brightness Increase |        -0.04% |        -0.04% |
| Brightness Decrease |         0.31% |         0.32% |

These results demonstrate strong resilience to moderate acquisition noise and illumination variation.

### Spectral Band Sensitivity

| Band Removed     | Macro-F1 Drop |
| ---------------- | ------------: |
| B3 (Green)       |    **59.70%** |
| B2 (Blue)        |        28.63% |
| B4 (Red)         |        18.06% |
| B11 (SWIR)       |         1.09% |
| B8 (NIR)         |         0.85% |
| B12 (SWIR)       |         0.27% |
| B6 (RedEdge)     |         0.27% |
| B5 (RedEdge)     |         0.24% |
| B8A (Narrow NIR) |         0.13% |
| B7 (RedEdge)     |         0.10% |

![Robustness-Based Spectral Sensitivity Analysis](reports/figures/robustness/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_robustness_macro_f1_drop.png)

**Figure 40.** Macro-F1 degradation under perturbations and single-band dropout experiments.

### Key Findings

The robustness analysis reveals that:

* RGB channels remain the dominant source of discriminative information.
* NIR and SWIR bands provide measurable complementary value.
* The model is highly robust to moderate noise and illumination changes.
* Spectral selection contributes more strongly to performance than simply increasing the number of bands.

---
## Reproducibility

A major objective of TerraSight is to ensure full experimental reproducibility.

### Experiment Tracking

All experiments are tracked using:

```text
experiments/registry.csv
```

which records:

* Experiment identifiers
* Spectral configurations
* Hyperparameters
* Training settings
* Evaluation metrics
* Output locations

### Configuration Management

Experiments are defined using version-controlled YAML configuration files:

```text
configs/
├── datasets/
├── models/
├── training/
└── experiments/
```

This approach enables exact reproduction of every reported result.

### Multi-Seed Evaluation

To reduce sensitivity to random initialization, experiments were evaluated using multiple random seeds.

Benefits include:

* More reliable performance estimates
* Improved statistical robustness
* Reduced variance due to stochastic training behaviour

---

## Installation

### Clone Repository

```bash
git clone https://github.com/toktamk/Terrasight-Eurosat-RGB-vs-Multispectral.git
cd Terrasight-Eurosat-RGB-vs-Multispectral
```

### Create Environment

```bash
python -m venv .venv 
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Install Dependencies

```bash
pip install -e .
pip install -r requirements.txt
python -c "import terrasight; print('Installation successful')"
```

## Dataset Preparation

Download the EuroSAT dataset and organize it according to the expected directory structure.

```text
Download the EuroSAT RGB dataset and the corresponding Sentinel-2 multispectral dataset. Extract the datasets and place the class-specific image folders into the appropriate raw-data directories:

data/
├── raw/
│   ├── rgb/
│   │   ├── AnnualCrop/
│   │   ├── Forest/
│   │   ├── HerbaceousVegetation/
│   │   ├── Highway/
│   │   ├── Industrial/
│   │   ├── Pasture/
│   │   ├── PermanentCrop/
│   │   ├── Residential/
│   │   ├── River/
│   │   └── SeaLake/
│   │
│   └── multispectral/
│       ├── AnnualCrop/
│       ├── Forest/
│       ├── HerbaceousVegetation/
│       ├── Highway/
│       ├── Industrial/
│       ├── Pasture/
│       ├── PermanentCrop/
│       ├── Residential/
│       ├── River/
│       └── SeaLake/
```
> **Note:** The repository does not redistribute the EuroSAT dataset. Users must download the dataset from the original source and place it in the directory structure shown above before running any experiments.

Then run:

```bash
python scripts/prepare_dataset.py
```

to generate training, validation, and test splits.

## Training

### RGB Baseline

```bash
python scripts/train.py --config configs/experiments/v1_rgb_pretrained.yaml
```

### Multispectral Baseline

```bash
python scripts/train.py --config configs/experiments/v1_multispectral_adapted.yaml
```

### Band Ablation Experiment

```bash
python scripts/train.py --config configs/experiments/v4_rgb_rededge_nir_swir.yaml
```

## Evaluation

Evaluate a trained model:

```bash
python scripts/evaluate.py --checkpoint path/to/checkpoint.pt
```

Generate figures and reports:

```bash
python scripts/generate_report_figures.py
```

Generate reliability analysis:

```bash
python scripts/reliability_analysis.py
```

Generate Grad-CAM visualizations:

```bash
python scripts/generate_gradcam.py
```
## Relevance to Infrastructure AI and Real-World Deployment

Although EuroSAT is a land-cover classification benchmark, the methodology developed in this project is directly relevant to the design of trustworthy AI systems for geospatial monitoring, environmental assessment, and infrastructure-related remote-sensing applications.

The project was intentionally designed not only to maximize classification performance but also to investigate the reliability, interpretability, and practical value of multispectral information for operational AI systems.

### Value of Multispectral Information

One of the central findings of this work is that carefully selected multispectral bands provide complementary information beyond conventional RGB imagery.

Different Sentinel-2 bands capture different physical properties of the Earth's surface:

| Spectral Region | Information Captured |
|----------------|---------------------|
| RGB | Visual appearance and texture |
| Red Edge | Vegetation stress and chlorophyll content |
| Near-Infrared (NIR) | Vegetation vigor and biomass |
| Short-Wave Infrared (SWIR) | Moisture content and material properties |

The statistical validation, band-ablation experiments, and spectral separability analysis collectively demonstrate that selective integration of Red Edge, NIR, and SWIR information can improve land-cover discrimination beyond visible-spectrum imagery alone.

In real-world infrastructure and environmental monitoring systems, these spectral characteristics can support applications such as:

- Vegetation encroachment monitoring
- Environmental impact assessment
- Land-use and land-cover mapping
- Asset corridor monitoring
- Flood and water-body detection
- Ecological and habitat assessment

### Reliability and Confidence-Aware Decision Making

High predictive accuracy alone is insufficient for operational deployment.

Real-world AI systems must provide reliable confidence estimates so that users can assess the trustworthiness of individual predictions.

The calibration analysis performed in this project demonstrates how confidence estimates can be evaluated alongside classification performance.

This capability is important because a highly confident incorrect prediction may be more harmful than a low-confidence uncertain prediction. Confidence-aware systems enable human reviewers to prioritize uncertain predictions for manual inspection and quality assurance.

### Explainability and Trustworthy AI

Explainability is a critical requirement for many operational AI systems.

The Grad-CAM analysis performed in this project provides insight into which image regions influence model decisions, enabling qualitative verification that predictions are based on meaningful scene characteristics rather than spurious artifacts.

Such explainability techniques support:

- Human-in-the-loop workflows
- Model auditing and validation
- Error investigation
- Regulatory and stakeholder transparency
- Trustworthy deployment of AI systems

### Robustness to Real-World Conditions

Remote-sensing imagery is frequently affected by variations in illumination, atmospheric conditions, seasonal effects, sensor noise, and data quality issues.

The robustness experiments conducted in this project evaluate model behaviour under perturbed conditions and provide insight into the stability of different spectral configurations.

Understanding model robustness is essential for operational deployment because production systems must remain reliable when conditions differ from those observed during training.

### Reproducibility and Engineering Practices

A major objective of this project was the development of a fully reproducible machine-learning workflow.

The project includes:

- Configuration-driven experimentation
- Experiment registry tracking
- Automated reporting pipelines
- Reproducible command-line workflows
- Statistical validation procedures
- Automated figure generation

These engineering practices support maintainability, traceability, and scientific reproducibility, which are essential characteristics of both research-grade and production-grade AI systems.

### Key Takeaway

> The primary contribution of this project extends beyond achieving high classification accuracy. Through statistical validation, spectral analysis, reliability assessment, explainability, robustness testing, and reproducible engineering practices, the project demonstrates how multispectral remote-sensing systems can be developed and evaluated as trustworthy AI solutions suitable for real-world geospatial and infrastructure-monitoring applications.

## Limitations

Several limitations should be considered when interpreting the results:

1. Experiments are limited to the EuroSAT dataset and a single Sentinel-2 benchmark.
2. Statistical significance testing was performed for key RGB-versus-multispectral comparisons, but not exhaustively for every experimental configuration.
3. Most multispectral experiments were conducted using ResNet18-based architectures; larger architectures were evaluated primarily on RGB imagery.
4. Grad-CAM provides qualitative rather than causal explanations of model behaviour.
5. Results may not directly generalize to other geographic regions, seasons, sensors, or land-cover taxonomies.
6. Multi-seed evaluation was performed for selected high-performing configurations rather than the complete experiment suite.
7. Additional validation on independent remote-sensing datasets would further strengthen the generality of the conclusions.

Experiments were conducted under CPU-only computational constraints; therefore extensive hyperparameter optimization and large-scale architecture benchmarking were outside the scope of this study.

# Discussion, Conclusions, and Additional Resources
## Discussion

This project investigated the value of Sentinel-2 multispectral imagery for land-cover classification using the EuroSAT benchmark dataset.

The results demonstrate that transfer learning remains highly effective in remote-sensing applications and that carefully selected multispectral information can improve classification performance beyond RGB-only inputs.

However, the experiments also reveal that increasing the number of spectral bands does not automatically improve performance. In several cases, reduced-band configurations achieved comparable or superior results relative to full-band models.

This observation suggests that the primary challenge is not maximizing spectral dimensionality but identifying the most informative spectral channels for the target task.

### RGB vs Multispectral Trade-Off

The experimental results highlight an important distinction:

- The **ImageNet-pretrained RGB model** achieved the highest overall classification accuracy.
- The **RGB + RedEdge + NIR + SWIR model** achieved the strongest multispectral performance and best calibration characteristics.

This indicates that RGB imagery already contains substantial discriminative information for EuroSAT classification, while carefully selected multispectral bands provide complementary information that improves robustness, confidence reliability, and performance for challenging land-cover categories.

### RGB versus Multispectral Interpretation

The ImageNet-pretrained RGB ResNet18 achieved the highest overall performance in the main benchmark. Therefore, this study does not claim that multispectral input universally outperforms RGB imagery.

Instead, the results show that carefully selected multispectral bands provide complementary information and improve performance relative to weaker multispectral configurations, such as Full13 or poorly selected band subsets.

The main conclusion is therefore not:

> Multispectral models outperform RGB models.

but rather:

> Spectral selection is more important than spectral quantity, and selected RedEdge, NIR, and SWIR bands provide physically meaningful complementary information within multispectral models.
## Conclusions

The main conclusions of this study are:

### 1. Transfer Learning Is Essential

Across both RGB and multispectral experiments, pretrained models consistently outperformed models trained from scratch.

### 2. RGB Remains a Strong Baseline

The RGB pretrained ResNet18 achieved the highest overall classification performance, demonstrating the effectiveness of transfer learning from large-scale natural image datasets.

### 3. Multispectral Information Provides Complementary Value

Near-Infrared (NIR), RedEdge, and Short-Wave Infrared (SWIR) bands contributed measurable improvements when combined with RGB information.

### 4. Spectral Selection Is More Important Than Spectral Quantity

The best-performing multispectral model used a carefully selected subset of Sentinel-2 bands rather than the complete spectral stack.

### 5. Reliable AI Requires More Than Accuracy

Reliability analysis, calibration assessment, confidence evaluation, explainability methods, and robustness testing provide valuable insights that are not captured by accuracy metrics alone.

## Alignment with Project Objectives

This project addresses all primary objectives of the technical assessment:

| Objective | Status |
|------------|---------|
| RGB vs Multispectral Comparison | ✓ Completed |
| Transfer Learning Evaluation | ✓ Completed |
| Sentinel-2 Band Investigation | ✓ Completed |
| Experimental Reproducibility | ✓ Completed |
| Quantitative Evaluation | ✓ Completed |
| Error Analysis | ✓ Completed |
| Explainability Analysis | ✓ Completed |
| Reliability Assessment | ✓ Completed |
| Robustness Evaluation | ✓ Completed |
| Scientific Interpretation | ✓ Completed |
| Statistical Validation | ✓ Completed |

## Extended Documentation

The repository includes additional analyses and technical documentation beyond the main README.

| Document | Description |
|-----------|-------------|
| `docs/reliability_analysis.md` | Calibration, ECE, reliability diagrams, and confidence analysis |
| `docs/explainability_analysis.md` | Grad-CAM and visual interpretation results |
| `docs/failure_analysis.md` | High-confidence failure investigation |
| `docs/robustness_analysis.md` | Noise, illumination, and band-dropout experiments |
| `docs/experimental_appendix.md` | Supplementary figures, tables, and ablation results |

## Reproducibility Checklist

The repository includes:

- Version-controlled source code
- Configuration-driven experiments
- Experiment registry (`registry.csv`)
- Fixed random seeds
- Automated evaluation scripts
- Figure-generation utilities
- Structured output directories
- Reproducible training pipelines

These components allow all reported experiments to be reproduced from configuration files and recorded experiment metadata.


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

## Repository Navigation

```text
README.md                         # Project overview
configs/                          # Experiment configurations
src/                              # Core implementation
scripts/                          # Training and evaluation scripts
experiments/registry.csv          # Experiment tracking
results/                          # Model outputs
reports/figures/                  # Generated figures
docs/                             # Extended analyses
````

## Citation

If you use this repository, please cite:

```bibtex
@misc{khatibi2026terrasight,
  title={TerraSight: EuroSAT RGB vs Multispectral Land-Cover Classification},
  author={Toktam Khatibi},
  year={2026},
  url={https://github.com/toktamk/Terrasight-Eurosat-RGB-vs-Multispectral}
}
```

## Contact

**Toktam Khatibi, PhD**

GitHub: https://github.com/toktamk/Terrasight-Eurosat-RGB-vs-Multispectral

For questions, suggestions, or collaboration opportunities, please open an issue in the repository.

## Acknowledgements

This work builds upon:

* EuroSAT Dataset
* Sentinel-2 Mission (European Space Agency)
* PyTorch
* Torchvision
* Open-source remote-sensing research community

**TerraSight demonstrates that understanding spectral information can be as important as improving classification accuracy. By combining reproducible experimentation, band-ablation studies, reliability analysis, and explainability methods, the project provides a systematic investigation of how Sentinel-2 spectral information contributes to land-cover classification performance.**

## Future Work
Several directions could further extend this work:

### Model Development

* Vision Transformers (ViTs)
* ConvNeXt
* Remote-sensing foundation models
* Self-supervised learning

### Data and Modalities

* Multi-temporal Sentinel-2 imagery
* Sentinel-1 SAR integration
* Cross-dataset evaluation
* Domain adaptation

### Reliability and Explainability

* Temperature scaling
* Conformal prediction
* Spectral attribution methods
* Class-specific band importance analysis

### Operational Deployment

* Efficient inference pipelines
* Model compression
* Edge deployment
* Real-time monitoring systems


Potential extensions include:

* Self-supervised multispectral pretraining
* Vision Transformers and foundation models
* Temporal Sentinel-2 analysis
* Cross-dataset evaluation
* Hierarchical land-cover classification
* Advanced calibration techniques
* Multi-modal fusion with SAR imagery

## Citation

If you use this work, please cite:

```bibtex
@misc{khatibi2026terrasight,
  title={TerraSight: EuroSAT RGB vs Multispectral Land-Cover Classification},
  author={Toktam Khatibi},
  year={2026},
  url={https://github.com/toktamk/Terrasight-Eurosat-RGB-vs-Multispectral}
}
```

## Acknowledgements

* EuroSAT Dataset
* Sentinel-2 Mission (European Space Agency)
* PyTorch
* Torchvision
* Open-source remote-sensing community

