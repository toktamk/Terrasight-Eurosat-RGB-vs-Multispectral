from __future__ import annotations

EUROSAT_CLASSES = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake",
]

CLASS_TO_INDEX = {class_name: index for index, class_name in enumerate(EUROSAT_CLASSES)}
INDEX_TO_CLASS = {index: class_name for class_name, index in CLASS_TO_INDEX.items()}

SENTINEL2_BANDS = [
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

RGB_BANDS = ["B4", "B3", "B2"]

BAND_DESCRIPTIONS = {
    "B1": "Coastal aerosol",
    "B2": "Blue",
    "B3": "Green",
    "B4": "Red",
    "B5": "Red Edge 1",
    "B6": "Red Edge 2",
    "B7": "Red Edge 3",
    "B8": "NIR",
    "B8A": "Narrow NIR",
    "B9": "Water vapour",
    "B10": "Cirrus",
    "B11": "SWIR 1",
    "B12": "SWIR 2",
}