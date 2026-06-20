from __future__ import annotations

import argparse
from pathlib import Path

from terrasight.data.band_registry import EUROSAT_CLASSES
from terrasight.explainability.class_specific_importance import (
    summarize_class_specific_importance,
)
from terrasight.reporting.generate_confusion_matrices import get_project_root


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate class-specific Sentinel-2 band-importance summaries."
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", default="reports/tables/class_specific_importance")
    parser.add_argument("--top-k", type=int, default=3)

    args = parser.parse_args()

    root = get_project_root()
    input_path = root / args.input
    output_dir = root / args.output_dir

    if not input_path.exists():
        raise FileNotFoundError(input_path)

    outputs = summarize_class_specific_importance(
        details=input_path,
        output_dir=output_dir,
        class_names=EUROSAT_CLASSES,
        top_k=args.top_k,
    )

    print(f"Saved class-specific importance outputs to: {output_dir}")
    for name, df in outputs.items():
        print(f"{name}: {df.shape}")


if __name__ == "__main__":
    main()