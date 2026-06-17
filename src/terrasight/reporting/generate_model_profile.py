from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_registry(project_root: Path) -> pd.DataFrame:
    candidates = [
        project_root / "experiments" / "registry.csv",
        project_root / "registry.csv",
    ]

    for path in candidates:
        if path.exists():
            return pd.read_csv(path)

    raise FileNotFoundError("Could not find registry.csv")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in out.columns]
    return out


def add_architecture_group(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    def group_row(row: pd.Series) -> str:
        experiment_id = str(row.get("experiment_id", "")).lower()
        bands = str(row.get("bands", "")).lower()
        input_type = str(row.get("input_type", "")).lower()

        if "rgb_rededge_nir_swir" in experiment_id:
            return "best_multispectral_subset"
        if "rgb_nir" in experiment_id:
            return "rgb_nir"
        if "rgb_rededge_nir" in experiment_id:
            return "rgb_rededge_nir"
        if input_type == "rgb" or bands in {"b4,b3,b2", "rgb"}:
            return "rgb"
        if "full13" in experiment_id:
            return "full13"

        return "other"

    out["architecture_group"] = out.apply(group_row, axis=1)

    return out


def generate_sensitivity_table(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "experiment_id",
        "model",
        "input_channels",
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
        "bands",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Registry is missing columns: {missing}")

    df = add_architecture_group(df)

    keep_cols = [
        "architecture_group",
        "experiment_id",
        "model",
        "input_channels",
        "bands",
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
    ]

    result = df[keep_cols].copy()

    result = result.sort_values(
        by=["architecture_group", "macro_f1"],
        ascending=[True, False],
    )

    return result


def generate_missing_architecture_plan(df: pd.DataFrame) -> pd.DataFrame:
    df = add_architecture_group(df)

    existing_models = set(df["model"].astype(str).str.lower().unique())

    target_models = ["resnet18", "resnet50", "efficientnet_b0"]

    rows = []

    for group in ["rgb", "best_multispectral_subset"]:
        for model in target_models:
            exists = not df[
                (df["architecture_group"] == group)
                & (df["model"].astype(str).str.lower() == model)
            ].empty

            rows.append(
                {
                    "architecture_group": group,
                    "model": model,
                    "status": "available" if exists else "missing",
                    "recommended": model in {"resnet18", "resnet50", "efficientnet_b0"},
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate architecture sensitivity summary from registry.csv."
    )

    parser.add_argument(
        "--output",
        default="reports/tables/architecture_sensitivity.csv",
    )

    parser.add_argument(
        "--missing-output",
        default="reports/tables/architecture_sensitivity_missing_plan.csv",
    )
    parser.add_argument(
        "--versions",
        nargs="+",
    )
    args = parser.parse_args()

    project_root = get_project_root()

    registry = load_registry(project_root)
    registry = normalize_columns(registry)

    sensitivity = generate_sensitivity_table(registry)
    missing_plan = generate_missing_architecture_plan(registry)

    output_path = project_root / args.output
    missing_path = project_root / args.missing_output

    output_path.parent.mkdir(parents=True, exist_ok=True)

    sensitivity.to_csv(output_path, index=False)
    missing_plan.to_csv(missing_path, index=False)

    print(f"Saved: {output_path}")
    print(f"Saved: {missing_path}")

    print("\nArchitecture availability:")
    print(missing_plan.to_string(index=False))


if __name__ == "__main__":
    main()