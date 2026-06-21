## Reliability and Calibration Analysis

Reliable confidence estimates are critical for real-world remote-sensing systems because operational decisions often depend not only on whether a prediction is correct, but also on how trustworthy the model believes that prediction to be.

To evaluate prediction reliability, TerraSight incorporates confidence-based analyses including:

- Reliability diagrams
- Expected Calibration Error (ECE)
- Confidence-distribution analysis
- High-confidence failure analysis

These analyses complement conventional classification metrics by assessing whether predicted probabilities correspond to observed accuracy.

### Reliability Analysis

Reliability diagrams compare predicted confidence against empirical accuracy across confidence bins.

A perfectly calibrated model follows the diagonal line, indicating that predictions with 80% confidence are correct approximately 80% of the time.

Deviations below the diagonal indicate **overconfidence**, whereas deviations above the diagonal indicate **underconfidence**.

#### Key Observations

Several consistent patterns emerged across all evaluated models:

1. Most predictions occur in the high-confidence region (>0.90).
2. Transfer learning improves confidence calibration compared with training from scratch.
3. Multispectral information improves both classification performance and confidence quality when informative spectral bands are selected.
4. Calibration quality varies substantially across spectral configurations despite similar classification performance.

### Expected Calibration Error (ECE)

Expected Calibration Error (ECE) was used as the primary calibration metric.

Lower values indicate better agreement between model confidence and empirical accuracy.

| Model | ECE ↓ |
|----------|----------:|
| RGB Pretrained (V1) | 0.0075 |
| RGB Scratch (V1) | 0.0231 |
| Multispectral Adapted (V1) | 0.0269 |
| Multispectral Scratch (V1) | 0.0385 |
| RGB + RedEdge + NIR + SWIR (V4) | **0.0039** |
| Full13 (V4) | 0.0050 |

#### Interpretation

Several important findings emerge from the calibration results:

- Transfer learning substantially improves calibration quality.
- RGB pretrained models are considerably better calibrated than RGB models trained from scratch.
- Adapted multispectral models exhibit improved calibration compared with multispectral models trained from random initialization.
- Carefully selected multispectral bands improve both predictive performance and confidence reliability.

The strongest calibration performance was achieved by the:

```text
RGB + RedEdge + NIR + SWIR
```

configuration, which achieved:

```text
ECE = 0.0039
```

This indicates excellent agreement between predicted confidence and observed accuracy.

### Reliability Diagrams

| RGB Baseline | Multispectral Adapted |
|:---:|:---:|
| ![](reports/figures/reliability/v1_rgb_resnet18_seed42_reliability_diagram.png) | ![](reports/figures/reliability/v1_multispectral_resnet18_adapted_seed42_reliability_diagram.png) |
| **(a)** RGB Pretrained | **(b)** Multispectral Adapted |

**Figure 1.** Reliability diagrams for the primary V1 models. The diagonal line represents perfect calibration.

The RGB pretrained model exhibits the strongest calibration among the V1 experiments, with its reliability curve closely following the ideal diagonal. The adapted multispectral model also demonstrates good calibration behaviour, although slight deviations appear in several confidence bins.

Both pretrained models are substantially better calibrated than their scratch-trained counterparts, reinforcing the value of transfer learning for confidence estimation as well as classification accuracy.

### Calibration Across Spectral Configurations

Reliability analysis of the V4 spectral-ablation experiments reveals that spectral selection influences not only classification performance but also confidence quality.

#### Calibration Ranking

| Rank | Configuration | Calibration Quality |
|--------|-----------------------------|----------------------|
| 1 | RGB + RedEdge + NIR + SWIR | Excellent |
| 2 | Full13 without B10 | Excellent |
| 3 | Full13 | Very Good |
| 4 | RGB + RedEdge + NIR | Good |
| 5 | Physical Surface Bands | Moderate |
| 6 | RGB | Poor |
| 7 | RGB + NIR | Worst |

Several notable observations emerge:

- RGB and RGB+NIR exhibit systematic overconfidence.
- Adding only NIR improves discriminative power but does not sufficiently improve calibration.
- RedEdge information noticeably improves confidence reliability.
- SWIR further improves confidence–accuracy alignment.
- Removing B10 does not degrade calibration and may slightly improve it.

These findings support the broader conclusion of this project:

> Spectral selection is more important than spectral quantity.

### Prediction Confidence Analysis

Prediction confidence histograms were generated using maximum softmax probabilities.

| RGB Baseline | Multispectral Baseline |
|:---:|:---:|
| ![](reports/figures/reliability/v1_rgb_resnet18_seed42_confidence_histogram.png) | ![](reports/figures/reliability/v1_multispectral_resnet18_adapted_seed42_confidence_histogram.png) |
| **(a)** RGB Pretrained | **(b)** Multispectral Adapted |

| Full13 | RGB + RedEdge + NIR |
|:---:|:---:|
| ![](reports/figures/reliability/v4_ablation_full13_resnet18_pretrained_adapted_seed42_confidence_histogram.png) | ![](reports/figures/reliability/v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42_confidence_histogram.png) |
| **(c)** Full13 | **(d)** RGB + RedEdge + NIR |

**Figure 2.** Prediction confidence distributions for representative RGB and multispectral models.

#### Interpretation

Several consistent trends are visible:

1. Most predictions receive confidence values above 0.95.
2. Multispectral models produce slightly sharper confidence distributions than RGB-only models.
3. Reduced-band multispectral configurations preserve confidence levels comparable to Full13 models.
4. Carefully selected spectral subsets achieve confidence behaviour similar to larger multispectral inputs while requiring fewer spectral channels.

These results indicate that useful multispectral information can improve certainty without requiring the complete Sentinel-2 spectral stack.

### High-Confidence Failure Analysis

Although the best-performing models achieve high overall accuracy, some errors occur with extremely high confidence.

Examples include:

| True Class | Predicted Class | Confidence |
|------------|----------------|------------|
| PermanentCrop | AnnualCrop | 0.993 |
| AnnualCrop | PermanentCrop | 0.997 |
| HerbaceousVegetation | PermanentCrop | 0.994 |
| River | AnnualCrop | 0.984 |
| Highway | Industrial | 0.988 |

These failures demonstrate that:

- High confidence does not guarantee correctness.
- Remaining errors primarily occur between semantically related classes.
- Agricultural and vegetation categories remain the most challenging classes.
- Calibration analysis is essential even for highly accurate models.

Most high-confidence errors arise from intrinsic class overlap rather than arbitrary prediction failures.

### Reliability Conclusions

The reliability and calibration analyses support four main conclusions:

1. Transfer learning improves both classification performance and confidence quality.
2. Carefully selected multispectral information improves calibration relative to RGB-only models.
3. The RGB + RedEdge + NIR + SWIR configuration provides the strongest balance of accuracy and reliability.
4. Confidence calibration remains important because high-confidence failures persist even in the best-performing models.

Overall, the results demonstrate that multispectral information contributes not only to classification performance but also to the trustworthiness of model predictions, which is essential for operational remote-sensing applications.