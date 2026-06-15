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