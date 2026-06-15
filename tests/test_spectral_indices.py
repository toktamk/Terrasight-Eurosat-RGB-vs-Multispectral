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