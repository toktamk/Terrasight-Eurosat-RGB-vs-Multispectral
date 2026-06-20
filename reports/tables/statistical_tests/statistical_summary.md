# Statistical Validation Summary

Comparison: **RGB ResNet18** vs **RGB+RedEdge+NIR+SWIR ResNet18**.

Both models were evaluated on the same paired test samples. Bootstrap confidence intervals estimate metric uncertainty, while McNemar's test evaluates whether the two models make significantly different paired errors.

## Bootstrap Improvement Confidence Intervals

| Metric | Mean Difference, B-A (%) | 95% CI Low (%) | 95% CI High (%) | Interpretation |
|---|---:|---:|---:|---|
| accuracy | 0.706 | -0.019 | 1.352 | CI overlaps zero |
| macro_f1 | 0.740 | 0.011 | 1.412 | favours model B; CI excludes zero |
| balanced_accuracy | 0.653 | -0.073 | 1.324 | CI overlaps zero |

## McNemar Test

| Quantity | Value |
|---|---:|
| Model A correct / Model B wrong | 137 |
| Model A wrong / Model B correct | 176 |
| McNemar statistic | 4.613419 |
| p-value | 0.031723 |

Conclusion: the paired prediction difference is **statistically significant** at p < 0.05.
