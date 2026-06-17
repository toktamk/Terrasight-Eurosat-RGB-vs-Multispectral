## Failure Analysis and Explainability

Beyond aggregate performance metrics, understanding *why* a model succeeds or fails is essential for trustworthy remote-sensing applications. TerraSight incorporates a multi-level explainability framework combining:

- High-confidence failure analysis
- Confusion-pair analysis
- Grad-CAM visual explanations
- Failure-case Grad-CAM interpretation

These analyses provide insight into residual classification errors, model attention behaviour, and the role of spectral information in difficult classification scenarios.

---

### High-Confidence Failure Analysis

Although the best-performing model achieved strong overall performance (95.67% Accuracy, 95.56% Macro-F1), a small number of errors were produced with extremely high confidence.

<p align="center">
<img src="reports/figures/failure_cases/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_high_confidence_failures.png" width="100%">
</p>

**Figure X.** High-confidence misclassifications from the best-performing multispectral model (RGB + RedEdge + NIR + SWIR).

Each example displays the true class, predicted class, and confidence score. Many incorrect predictions occur with confidence values exceeding 0.98, indicating that the model can be highly certain even when incorrect.

#### Dominant Failure Modes

Most failures occur between semantically related land-cover categories:

- PermanentCrop ↔ AnnualCrop
- PermanentCrop ↔ HerbaceousVegetation
- Pasture ↔ HerbaceousVegetation
- River ↔ AnnualCrop
- Highway ↔ Industrial

These categories share similar spatial structures, vegetation characteristics, or contextual information, making separation challenging even when multispectral information is available.

#### Agricultural Class Ambiguity

The most common failures involve:

- AnnualCrop
- PermanentCrop
- Pasture
- HerbaceousVegetation

These classes often contain:

- similar vegetation density;
- comparable field geometry;
- overlapping seasonal characteristics;
- related agricultural management practices.

Consequently, even highly discriminative models struggle to identify clear decision boundaries between these categories.

#### Context-Dominated Errors

Several failures suggest that surrounding scene context influences predictions:

- River → AnnualCrop
- River → HerbaceousVegetation
- Highway → Industrial

In these examples, the target object occupies only a small portion of the image while surrounding land-cover dominates the scene. The model therefore relies heavily on contextual cues rather than the narrow linear structure itself.

#### Key Insight

Importantly, the model rarely confuses unrelated classes. Most mistakes occur between categories that are visually, spectrally, or semantically similar.

This behaviour suggests that the learned feature representations are meaningful and that the remaining errors primarily reflect intrinsic ambiguity within the EuroSAT dataset rather than deficiencies in model training.

---

### Confusion-Pair Analysis

To better understand residual errors, Grad-CAM was applied to representative confusion pairs.

| Confusion Pair | Interpretation |
|----------------|----------------|
| AnnualCrop → PermanentCrop | Similar agricultural parcel structure and crop texture |
| PermanentCrop → AnnualCrop | Shared field geometry and vegetation characteristics |
| HerbaceousVegetation → PermanentCrop | Dense vegetation regions with overlapping spectral signatures |
| Industrial → Residential | Similar urban morphology and road-network patterns |
| River → Highway | Linear structures with comparable spatial geometry |

The most persistent confusion pair across all experiments was:

```text
PermanentCrop ↔ HerbaceousVegetation
```

This finding is consistent with the confusion-matrix analysis and supports the conclusion that vegetation-related classes remain the primary classification challenge.

---

### Grad-CAM Explainability

Gradient-weighted Class Activation Mapping (Grad-CAM) was used to investigate which image regions contributed most strongly to model predictions.

The framework supports:

- Class-specific Grad-CAM
- Confusion-pair Grad-CAM
- High-confidence failure Grad-CAM

Representative correctly classified examples are shown below.

| PermanentCrop | Residential | River |
|---------------|-------------|--------|
| ![](reports/figures/gradcam/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_layer3_class_examples_00_PermanentCrop_to_PermanentCrop.png) | ![](reports/figures/gradcam/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_layer3_class_examples_00_Residential_to_Residential.png) | ![](reports/figures/gradcam/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_layer3_class_examples_05_River_to_River.png) |

**Figure X.** Representative Grad-CAM explanations from the best-performing multispectral model.

#### Interpretation

The visualizations indicate that the model attends to semantically meaningful land-cover structures:

- **PermanentCrop:** cultivated parcels, field boundaries, and agricultural texture.
- **Residential:** dense building clusters and transportation infrastructure.
- **River:** elongated water channels and surrounding hydrological structures.

These attention patterns provide evidence that predictions are based on relevant land-cover characteristics rather than spurious image artifacts.

---

### Failure-Case Grad-CAM Analysis

To investigate why errors occur, Grad-CAM was applied to representative high-confidence failures.

| Failure Type | Representative Cause |
|--------------|---------------------|
| PermanentCrop → AnnualCrop | Similar crop texture and field geometry |
| HerbaceousVegetation → PermanentCrop | Overlapping vegetation characteristics |
| Industrial → Residential | Similar urban spatial organization |
| River → AnnualCrop | Mixed land-cover scenes |
| River → Highway | Similar elongated structures |

Representative examples are shown below.

| (a) PermanentCrop → Industrial | (b) AnnualCrop → SeaLake |
|---|---|
| ![](reports/figures/gradcam/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_layer3_high_confidence_failure_00_PermanentCrop_to_Industrial.png) | ![](reports/figures/gradcam/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_layer3_high_confidence_failure_01_AnnualCrop_to_SeaLake.png) |

| (c) HerbaceousVegetation → PermanentCrop | (d) PermanentCrop → AnnualCrop |
|---|---|
| ![](reports/figures/gradcam/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_layer3_high_confidence_failure_02_HerbaceousVegetation_to_PermanentCrop.png) | ![](reports/figures/gradcam/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_layer3_high_confidence_failure_03_PermanentCrop_to_AnnualCrop.png) |

**Figure X.** Representative high-confidence failures and corresponding Grad-CAM explanations.

The activation maps reveal that the model generally attends to meaningful structures even when predictions are incorrect. Most failures arise because multiple classes share similar spectral and spatial characteristics rather than because attention is focused on irrelevant image regions.

This behaviour increases confidence that the model has learned useful land-cover representations and that residual errors primarily reflect dataset complexity.

---

### Explainability Conclusions

The explainability analysis supports four main conclusions:

1. The model consistently focuses on semantically meaningful land-cover structures.
2. Most residual errors occur between spectrally and visually related classes rather than unrelated categories.
3. Agricultural classes remain the dominant source of classification difficulty.
4. High-confidence failures reveal intrinsic ambiguity within the EuroSAT dataset rather than systematic model malfunction.

Overall, the Grad-CAM and failure analyses provide qualitative evidence that the proposed multispectral model learns interpretable spatial representations and bases its decisions on physically meaningful land-cover characteristics, increasing confidence in the trustworthiness of the reported results.