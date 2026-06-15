from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RequiredAsset:
    path: str
    description: str
    required: bool = True


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def build_required_assets() -> list[RequiredAsset]:
    return [
        RequiredAsset(
            path="reports/final_report_template.md",
            description="Final report Markdown template",
        ),
        RequiredAsset(
            path="reports/tables/final_model_comparison.csv",
            description="Final model comparison table",
        ),
        RequiredAsset(
            path="reports/tables/comparison_table.csv",
            description="General comparison table",
            required=False,
        ),
        RequiredAsset(
            path="reports/tables/classwise_comparison.csv",
            description="Per-class precision, recall, and F1 table",
        ),
        RequiredAsset(
            path="reports/tables/classwise_improvement_summary.csv",
            description="Class-wise improvement summary",
        ),
        RequiredAsset(
            path="reports/tables/confusion_pair_analysis.csv",
            description="Confusion-pair analysis table",
        ),
        RequiredAsset(
            path="reports/tables/v4_band_effects.csv",
            description="V4 scientific question summary table",
        ),
        RequiredAsset(
            path="reports/tables/v4_class_level_band_effects.csv",
            description="V4 class-level band-effect table",
        ),
        RequiredAsset(
            path="reports/tables/v4_confusion_change_summary.csv",
            description="V4 confusion-pair change table",
        ),
        RequiredAsset(
            path="reports/tables/v4_scientific_conclusions.md",
            description="V4 scientific conclusions Markdown",
        ),
        RequiredAsset(
            path="reports/figures/v1_model_comparison.png",
            description="V1 RGB vs multispectral model comparison figure",
        ),
        RequiredAsset(
            path="reports/figures/v4_model_comparison.png",
            description="V4 band-ablation model comparison figure",
        ),
        RequiredAsset(
            path="reports/figures/v4_band_ablation_comparison.png",
            description="V4 band-ablation comparison figure",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v1_rgb_resnet18_seed42_confusion_matrix.png",
            description="RGB pretrained confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v1_rgb_resnet18_seed42_normalized_confusion_matrix.png",
            description="RGB pretrained normalized confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v1_multispectral_resnet18_adapted_seed42_confusion_matrix.png",
            description="Multispectral adapted confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v1_multispectral_resnet18_adapted_seed42_normalized_confusion_matrix.png",
            description="Multispectral adapted normalized confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v4_ablation_rgb_resnet18_pretrained_adapted_seed42_confusion_matrix.png",
            description="V4 RGB confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v4_ablation_rgb_nir_resnet18_pretrained_adapted_seed42_confusion_matrix.png",
            description="V4 RGB+NIR confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v4_ablation_rgb_rededge_nir_resnet18_pretrained_adapted_seed42_confusion_matrix.png",
            description="V4 RGB+RedEdge+NIR confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_confusion_matrix.png",
            description="V4 RGB+RedEdge+NIR+SWIR confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v4_ablation_physical_bands_resnet18_pretrained_adapted_seed42_confusion_matrix.png",
            description="V4 physical-bands confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v4_ablation_full13_no_b10_resnet18_pretrained_adapted_seed42_confusion_matrix.png",
            description="V4 Full13-no-B10 confusion matrix",
            required=False,
        ),
        RequiredAsset(
            path="reports/figures/confusion_matrices/v4_ablation_full13_resnet18_pretrained_adapted_seed42_confusion_matrix.png",
            description="V4 Full13 confusion matrix",
            required=False,
        ),
    ]


def discover_assets(project_root: Path, pattern: str) -> list[Path]:
    return sorted(project_root.glob(pattern))


def check_asset(project_root: Path, asset: RequiredAsset) -> tuple[bool, Path]:
    full_path = project_root / asset.path
    return full_path.exists(), full_path


def print_asset_status(project_root: Path, assets: list[RequiredAsset]) -> tuple[int, int, int]:
    required_missing = 0
    optional_missing = 0
    present = 0

    print("\nReport asset check")
    print("=" * 80)

    for asset in assets:
        exists, full_path = check_asset(project_root, asset)

        if exists:
            present += 1
            status = "OK"
        elif asset.required:
            required_missing += 1
            status = "MISSING"
        else:
            optional_missing += 1
            status = "OPTIONAL MISSING"

        print(f"[{status}] {asset.path}")
        print(f"        {asset.description}")

        if not exists:
            print(f"        Expected at: {full_path}")

    return present, required_missing, optional_missing


def print_discovered_assets(project_root: Path) -> None:
    discovery_patterns = {
        "Training/loss curves": "reports/figures/**/*loss*curve*.png",
        "Macro-F1 curves": "reports/figures/**/*macro*f1*curve*.png",
        "Confusion matrices": "reports/figures/**/*confusion*matrix*.png",
        "Model comparison figures": "reports/figures/**/*comparison*.png",
        "Prediction CSVs": "reports/tables/predictions/*_predictions.csv",
        "Classwise reports": "reports/tables/predictions/*_classwise_report.csv",
    }

    print("\nDiscovered supporting assets")
    print("=" * 80)

    for title, pattern in discovery_patterns.items():
        paths = discover_assets(project_root, pattern)

        print(f"\n{title}: {len(paths)} found")

        for path in paths[:20]:
            print(f"  - {path.relative_to(project_root)}")

        if len(paths) > 20:
            print(f"  ... {len(paths) - 20} more")


def validate_report_sections(project_root: Path) -> list[str]:
    report_path = project_root / "reports" / "final_report_template.md"

    required_sections = [
        "Abstract",
        "Experimental Results",
        "Reliability Results",
        "Band Ablation Results",
        "Discussion",
        "Industrial Relevance",
        "Limitations",
        "Future Work",
        "Conclusion",
    ]

    missing_sections: list[str] = []

    if not report_path.exists():
        return required_sections

    text = report_path.read_text(encoding="utf-8", errors="ignore").lower()

    for section in required_sections:
        if section.lower() not in text:
            missing_sections.append(section)

    return missing_sections


def print_report_section_status(project_root: Path) -> int:
    missing_sections = validate_report_sections(project_root)

    print("\nFinal report section check")
    print("=" * 80)

    if not missing_sections:
        print("[OK] All required report section headings were found.")
        return 0

    print("[MISSING] The following required sections were not found:")
    for section in missing_sections:
        print(f"  - {section}")

    return len(missing_sections)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check whether required TerraSight report assets exist."
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any required asset or required report section is missing.",
    )

    parser.add_argument(
        "--show-discovered",
        action="store_true",
        help="List discovered supporting figures and tables.",
    )

    args = parser.parse_args()

    project_root = get_project_root()
    assets = build_required_assets()

    print(f"Project root: {project_root}")

    present, required_missing, optional_missing = print_asset_status(
        project_root=project_root,
        assets=assets,
    )

    missing_sections = print_report_section_status(project_root)

    if args.show_discovered:
        print_discovered_assets(project_root)

    print("\nSummary")
    print("=" * 80)
    print(f"Present assets: {present}")
    print(f"Missing required assets: {required_missing}")
    print(f"Missing optional assets: {optional_missing}")
    print(f"Missing report sections: {missing_sections}")

    if required_missing == 0 and missing_sections == 0:
        print("\nReport asset status: READY")
    else:
        print("\nReport asset status: NOT READY")

    if args.strict and (required_missing > 0 or missing_sections > 0):
        raise SystemExit(1)


if __name__ == "__main__":
    main()