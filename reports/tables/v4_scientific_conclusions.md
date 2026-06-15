# V4 Band-Ablation Scientific Conclusions

## Overall V4 model comparison

| Model                |   Accuracy |   Macro-F1 |
|:---------------------|-----------:|-----------:|
| RGB                  |     0.9494 |     0.9480 |
| RGB+NIR              |     0.9546 |     0.9531 |
| RGB+RedEdge+NIR      |     0.9539 |     0.9529 |
| RGB+RedEdge+NIR+SWIR |     0.9567 |     0.9556 |
| PhysicalBands        |     0.9541 |     0.9528 |
| Full13NoB10          |     0.9496 |     0.9479 |
| Full13               |     0.9457 |     0.9443 |

## Scientific questions

| question                                  | comparison                                 | target_classes                                                   |   mean_f1_gain | conclusion                                                                                              |
|:------------------------------------------|:-------------------------------------------|:-----------------------------------------------------------------|---------------:|:--------------------------------------------------------------------------------------------------------|
| Does NIR help vegetation classes?         | RGB+NIR minus RGB                          | AnnualCrop, Forest, HerbaceousVegetation, Pasture, PermanentCrop |         0.0050 | Yes. NIR improves vegetation-class F1 on average.                                                       |
| Does RedEdge improve crop discrimination? | RGB+RedEdge+NIR minus RGB+NIR              | AnnualCrop, HerbaceousVegetation, PermanentCrop                  |         0.0015 | RedEdge provides a small positive crop-discrimination gain.                                             |
| Does SWIR improve urban/water separation? | RGB+RedEdge+NIR+SWIR minus RGB+RedEdge+NIR | Highway, Industrial, Residential, River, SeaLake                 |         0.0013 | SWIR provides a small positive gain for urban/water-related classes.                                    |
| Does removing B10 help?                   | Full13NoB10 minus Full13                   | All classes                                                      |         0.0036 | Removing B10 gives a small positive Macro-F1 gain.                                                      |
| Do atmospheric bands reduce performance?  | PhysicalBands minus Full13                 | All classes                                                      |         0.0085 | Yes. Surface-focused physical bands outperform Full13, suggesting atmospheric bands reduce performance. |

## Interpretation

### Does NIR help vegetation classes?

**Comparison:** RGB+NIR minus RGB

**Target classes:** AnnualCrop, Forest, HerbaceousVegetation, Pasture, PermanentCrop

**Mean F1 gain:** 0.0050

**Conclusion:** Yes. NIR improves vegetation-class F1 on average.

### Does RedEdge improve crop discrimination?

**Comparison:** RGB+RedEdge+NIR minus RGB+NIR

**Target classes:** AnnualCrop, HerbaceousVegetation, PermanentCrop

**Mean F1 gain:** 0.0015

**Conclusion:** RedEdge provides a small positive crop-discrimination gain.

### Does SWIR improve urban/water separation?

**Comparison:** RGB+RedEdge+NIR+SWIR minus RGB+RedEdge+NIR

**Target classes:** Highway, Industrial, Residential, River, SeaLake

**Mean F1 gain:** 0.0013

**Conclusion:** SWIR provides a small positive gain for urban/water-related classes.

### Does removing B10 help?

**Comparison:** Full13NoB10 minus Full13

**Target classes:** All classes

**Mean F1 gain:** 0.0036

**Conclusion:** Removing B10 gives a small positive Macro-F1 gain.

### Do atmospheric bands reduce performance?

**Comparison:** PhysicalBands minus Full13

**Target classes:** All classes

**Mean F1 gain:** 0.0085

**Conclusion:** Yes. Surface-focused physical bands outperform Full13, suggesting atmospheric bands reduce performance.

## Main scientific conclusion

The V4 ablation results should be interpreted as a controlled spectral-input study. The key question is not whether adding more bands always improves performance, but whether physically meaningful bands improve class separability. If selected multispectral subsets outperform Full13, the defensible conclusion is that spectral selection is more important than simply maximizing the number of input channels.
