from __future__ import annotations

from terrasight.data.band_registry import SENTINEL2_BANDS


BAND_SETS: dict[str, list[str]] = {
    "rgb": ["B4", "B3", "B2"],
    "rgb_nir": ["B4", "B3", "B2", "B8"],
    "rgb_rededge_nir": ["B4", "B3", "B2", "B5", "B6", "B7", "B8"],
    "rgb_rededge_nir_swir": ["B4", "B3", "B2", "B5", "B6", "B7", "B8", "B11", "B12"],
    "full_13": SENTINEL2_BANDS,
}


def get_band_set(name: str) -> list[str]:
    """Return predefined Sentinel-2 band set."""

    if name not in BAND_SETS:
        raise ValueError(f"Unknown band set: {name}. Available: {list(BAND_SETS)}")

    return BAND_SETS[name]


def list_band_sets() -> list[str]:
    """Return available band-set names."""

    return list(BAND_SETS.keys())


def validate_band_set(bands: list[str]) -> None:
    """Validate selected bands."""

    invalid = [band for band in bands if band not in SENTINEL2_BANDS]

    if invalid:
        raise ValueError(f"Invalid Sentinel-2 bands: {invalid}")