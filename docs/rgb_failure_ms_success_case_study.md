# RGB Failure to Multispectral Success Case Study

Expected outputs:

```text
reports/tables/case_studies/rgb_failure_ms_success.csv
reports/figures/case_studies/rgb_failure_ms_success.png
```

Recommended command:

```bash
python scripts/generate_rgb_failure_ms_success_gallery.py --rgb-predictions reports/tables/predictions/v1_rgb_resnet18_seed42_predictions.csv --ms-predictions reports/tables/predictions/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_predictions.csv --output-csv reports/tables/case_studies/rgb_failure_ms_success.csv --output-png reports/figures/case_studies/rgb_failure_ms_success.png --max-examples 12
```

Interpretation to add below the generated figure:

> The selected examples show cases where the RGB model misclassified the land-cover class but the RGB+RedEdge+NIR+SWIR model corrected the prediction. These examples support the central multispectral hypothesis: non-visible Sentinel-2 bands can provide complementary evidence when visible-spectrum texture and colour are ambiguous. NIR and RedEdge information are most relevant for vegetation/crop discrimination, while SWIR can support separation where moisture or surface material differences are important.
