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
