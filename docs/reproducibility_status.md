# Reproducibility Status

Generated: 2026-06-20 13:24:21

Overall status: **PASSED**

## Command Verification

| Check | Status | Command |
|---|---:|---|
| Package import | ✓ | `python -c import terrasight; print('TerraSight import successful')` |
| Unit tests | ✓ | `pytest` |
| Reproducibility command tests | ✓ | `pytest tests/test_reproducibility_commands.py` |
| Report asset validation | ✓ | `python -m terrasight.reporting.check_report_assets --show-discovered --strict` |

## Artifact Verification

| Artifact | Status |
|---|---:|
| `experiments/registry.csv` | ✓ |
| `reports/tables/statistical_tests/statistical_analysis.csv` | ✓ |
| `reports/tables/statistical_tests/statistical_summary.md` | ✓ |
| `reports/tables/spectral_analysis/class_mean_signatures.csv` | ✓ |
| `reports/tables/spectral_analysis/bhattacharyya_distances.csv` | ✓ |
| `reports/tables/spectral_analysis/spectral_angles.csv` | ✓ |
| `reports/figures/spectral_analysis/bhattacharyya_heatmap.png` | ✓ |
| `reports/figures/spectral_analysis/spectral_angle_heatmap.png` | ✓ |
| `reports/figures/reliability` | ✓ |
| `reports/figures/gradcam` | ✓ |
| `reports/figures/robustness` | ✓ |
| `reports/figures/failure_cases` | ✓ |

## Command Outputs

### Package import

```text
TerraSight import successful
```

### Unit tests

```text
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\DELL Precision 5550\Documents\GitHub\Terrasight-Eurosat-RGB-vs-Multispectral
configfile: pyproject.toml
collected 211 items

tests\test_band_sets.py .....                                            [  2%]
tests\test_comparison.py ..                                              [  3%]
tests\test_explainability.py ...                                         [  4%]
tests\test_metrics.py ...                                                [  6%]
tests\test_models.py ...                                                 [  7%]
tests\test_registry.py .                                                 [  8%]
tests\test_reliability.py ..........                                     [ 12%]
tests\test_reporting.py ......                                           [ 15%]
tests\test_reproducibility_commands.py ................................. [ 31%]
........................................................................ [ 65%]
.................................................................        [ 96%]
tests\test_spectral_indices.py ....                                      [ 98%]
tests\test_training.py ....                                              [100%]

============================== warnings summary ===============================
tests/test_explainability.py::test_gradcam_generates_heatmap
  C:\Users\DELL Precision 5550\Documents\GitHub\terrasight-eurosat-rgb-vs-multispectral\src\terrasight\explainability\gradcam.py:50: UserWarning: Full backward hook is firing when gradients are computed with respect to module outputs since no inputs require gradients. See https://docs.pytorch.org/docs/main/generated/torch.nn.Module.html#torch.nn.Module.register_full_backward_hook for more details.
    score.backward()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================= 211 passed, 1 warning in 22.94s =======================
```

### Reproducibility command tests

```text
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\DELL Precision 5550\Documents\GitHub\Terrasight-Eurosat-RGB-vs-Multispectral
configfile: pyproject.toml
collected 170 items

tests\test_reproducibility_commands.py ................................. [ 19%]
........................................................................ [ 61%]
.................................................................        [100%]

============================= 170 passed in 0.54s =============================
```

### Report asset validation

```text
42_normalized_confusion_matrix.png
  - reports\figures\confusion_matrices\v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_confusion_matrix.png
  - reports\figures\confusion_matrices\v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_normalized_confusion_matrix.png
  ... 2 more

Model comparison figures: 4 found
  - reports\figures\per_class_f1_comparison.png
  - reports\figures\v1_model_comparison.png
  - reports\figures\v4_band_ablation_comparison.png
  - reports\figures\v4_model_comparison.png

Prediction CSVs: 11 found
  - reports\tables\predictions\v1_multispectral_resnet18_adapted_seed42_predictions.csv
  - reports\tables\predictions\v1_multispectral_resnet18_scratch_seed42_predictions.csv
  - reports\tables\predictions\v1_rgb_resnet18_scratch_seed42_predictions.csv
  - reports\tables\predictions\v1_rgb_resnet18_seed42_predictions.csv
  - reports\tables\predictions\v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42_predictions.csv
  - reports\tables\predictions\v4_ablation_full13_resnet18_pretrained_adapted_seed42_predictions.csv
  - reports\tables\predictions\v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42_predictions.csv
  - reports\tables\predictions\v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42_predictions.csv
  - reports\tables\predictions\v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42_predictions.csv
  - reports\tables\predictions\v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_predictions.csv
  - reports\tables\predictions\v4_ablation_rgb_resnet18_pretrained_adapted_seed42_predictions.csv

Classwise reports: 11 found
  - reports\tables\predictions\v1_multispectral_resnet18_adapted_seed42_classwise_report.csv
  - reports\tables\predictions\v1_multispectral_resnet18_scratch_seed42_classwise_report.csv
  - reports\tables\predictions\v1_rgb_resnet18_scratch_seed42_classwise_report.csv
  - reports\tables\predictions\v1_rgb_resnet18_seed42_classwise_report.csv
  - reports\tables\predictions\v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42_classwise_report.csv
  - reports\tables\predictions\v4_ablation_full13_resnet18_pretrained_adapted_seed42_classwise_report.csv
  - reports\tables\predictions\v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42_classwise_report.csv
  - reports\tables\predictions\v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42_classwise_report.csv
  - reports\tables\predictions\v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42_classwise_report.csv
  - reports\tables\predictions\v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_classwise_report.csv
  - reports\tables\predictions\v4_ablation_rgb_resnet18_pretrained_adapted_seed42_classwise_report.csv

Summary
================================================================================
Present assets: 24
Missing required assets: 0
Missing optional assets: 0
Missing report sections: 0

Report asset status: READY
```

## Conclusion

This file records the reproducibility verification status for the TerraSight submission package.
It should be regenerated immediately before final submission.
