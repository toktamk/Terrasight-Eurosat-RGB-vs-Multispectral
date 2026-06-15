from __future__ import annotations

import json
from pathlib import Path


def save_band_attribution(
    scores: dict[str, float],
    output_path: str | Path,
) -> None:
    """Save band attribution scores as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(scores, file, indent=2)


def build_explainability_summary(
    predicted_class: str,
    target_class: str,
    band_scores: dict[str, float],
) -> dict:
    """Create compact explainability summary."""

    ranked = sorted(band_scores.items(), key=lambda item: item[1], reverse=True)

    return {
        "predicted_class": predicted_class,
        "target_class": target_class,
        "top_bands": [
            {"band": band, "score": float(score)}
            for band, score in ranked[:5]
        ],
    }