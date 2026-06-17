from __future__ import annotations

import argparse
import copy
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


def get_project_root() -> Path:
    return Path.cwd()


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def save_yaml(config: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(config, file, sort_keys=False)


def update_nested(config: dict[str, Any], keys: list[str], value: Any) -> None:
    cursor = config

    for key in keys[:-1]:
        cursor = cursor.setdefault(key, {})

    cursor[keys[-1]] = value


def get_nested(config: dict[str, Any], keys: list[str], default: Any = None) -> Any:
    cursor: Any = config

    for key in keys:
        if not isinstance(cursor, dict) or key not in cursor:
            return default
        cursor = cursor[key]

    return cursor


def infer_training_module(config: dict[str, Any]) -> str:
    input_type = get_nested(config, ["data", "input_type"])

    if input_type == "rgb":
        return "terrasight.pipelines.train_rgb"

    if input_type == "multispectral":
        return "terrasight.pipelines.train_multispectral"

    raise ValueError(
        f"Could not infer training module from data.input_type={input_type!r}. "
        "Expected 'rgb' or 'multispectral'."
    )


def make_seed_config(
    base_config: dict[str, Any],
    seed: int,
    output_dir: Path,
) -> dict[str, Any]:
    config = copy.deepcopy(base_config)

    experiment = config.setdefault("experiment", {})
    training = config.setdefault("training", {})

    base_id = str(experiment.get("id", "experiment"))

    if "_seed" in base_id:
        base_id = base_id.split("_seed")[0]

    seed_id = f"{base_id}_seed{seed}"

    experiment["id"] = seed_id
    experiment["seed"] = seed
    training["seed"] = seed

    # Support common alternative config conventions.
    config["seed"] = seed

    if "reproducibility" in config:
        config["reproducibility"]["seed"] = seed

    # Keep all multiseed outputs grouped if your setup_run reads these keys.
    experiment["output_dir"] = str(output_dir)
    experiment["run_dir"] = str(output_dir / seed_id)

    return config


def run_training(
    config_path: Path,
    module_name: str,
    dry_run: bool = False,
) -> None:
    command = [
        sys.executable,
        "-m",
        module_name,
        "--config",
        str(config_path),
    ]

    print("Running:", " ".join(command))

    if dry_run:
        return

    subprocess.run(command, check=True)


def find_run_dir_from_config(
    config: dict[str, Any],
    project_root: Path,
) -> Path | None:
    experiment_id = str(get_nested(config, ["experiment", "id"], ""))

    candidates: list[Path] = []

    configured_run_dir = get_nested(config, ["experiment", "run_dir"])
    if configured_run_dir:
        candidates.append(project_root / str(configured_run_dir))

    for version in ["v1", "v2", "v3", "v4", "multiseed"]:
        results_dir = project_root / "results" / version
        if results_dir.exists():
            candidates.extend(sorted(results_dir.glob(f"*{experiment_id}*")))

    results_dir = project_root / "results"
    if results_dir.exists():
        candidates.extend(sorted(results_dir.glob(f"**/*{experiment_id}*")))

    valid = [path for path in candidates if path.exists() and path.is_dir()]

    if not valid:
        return None

    valid = sorted(valid, key=lambda path: path.stat().st_mtime, reverse=True)
    return valid[0]


def load_metrics(run_dir: Path) -> dict[str, Any]:
    metrics_path = run_dir / "metrics.json"

    if not metrics_path.exists():
        return {}

    with metrics_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def collect_seed_result(
    seed: int,
    config: dict[str, Any],
    project_root: Path,
) -> dict[str, Any]:
    experiment_id = str(get_nested(config, ["experiment", "id"], f"seed{seed}"))
    run_dir = find_run_dir_from_config(config, project_root)

    row: dict[str, Any] = {
        "seed": seed,
        "experiment_id": experiment_id,
        "run_dir": str(run_dir) if run_dir else "",
        "status": "missing_run_dir" if run_dir is None else "completed",
    }

    if run_dir is None:
        return row

    metrics = load_metrics(run_dir)

    for key in [
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
        "macro_precision",
        "macro_recall",
        "loss",
        "epoch",
    ]:
        row[key] = metrics.get(key, "")

    return row


def write_summary_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "seed",
        "experiment_id",
        "status",
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
        "macro_precision",
        "macro_recall",
        "loss",
        "epoch",
        "run_dir",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def compute_mean_std(rows: list[dict[str, Any]]) -> dict[str, float]:
    metrics = [
        "accuracy",
        "macro_f1",
        "weighted_f1",
        "balanced_accuracy",
        "macro_precision",
        "macro_recall",
        "loss",
    ]

    summary: dict[str, float] = {}

    for metric in metrics:
        values: list[float] = []

        for row in rows:
            value = row.get(metric, "")
            if value == "" or value is None:
                continue
            values.append(float(value))

        if not values:
            continue

        mean = sum(values) / len(values)

        if len(values) > 1:
            variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
            std = variance ** 0.5
        else:
            std = 0.0

        summary[f"{metric}_mean"] = mean
        summary[f"{metric}_std"] = std

    return summary


def write_summary_json(rows: list[dict[str, Any]], output_path: Path) -> None:
    summary = compute_mean_std(rows)

    payload = {
        "n_completed": sum(row["status"] == "completed" for row in rows),
        "n_total": len(rows),
        "summary": summary,
        "runs": rows,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run TerraSight experiments with multiple random seeds."
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Base YAML config file, e.g. configs/v4_ablation_rgb_rededge_nir_swir.yaml.",
    )

    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=[42, 43, 44],
        help="Random seeds to run.",
    )

    parser.add_argument(
        "--generated-config-dir",
        default="experiments/generated_multiseed",
        help="Directory where generated seed-specific configs are saved.",
    )

    parser.add_argument(
        "--output-dir",
        default="results/multiseed",
        help="Base output directory requested for multiseed runs.",
    )

    parser.add_argument(
        "--summary-csv",
        default="reports/tables/multiseed_summary.csv",
        help="Output CSV summary path.",
    )

    parser.add_argument(
        "--summary-json",
        default="reports/tables/multiseed_summary.json",
        help="Output JSON summary path.",
    )

    parser.add_argument(
        "--module",
        default=None,
        help=(
            "Optional training module override. "
            "Examples: terrasight.pipelines.train_multispectral, terrasight.pipelines.train_rgb"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only generate configs and print commands.",
    )

    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue with remaining seeds if one training run fails.",
    )

    args = parser.parse_args()

    project_root = get_project_root()

    base_config_path = Path(args.config)
    generated_config_dir = Path(args.generated_config_dir)
    output_dir = Path(args.output_dir)

    base_config = load_yaml(base_config_path)

    module_name = args.module or infer_training_module(base_config)

    print(f"Training module: {module_name}")

    rows: list[dict[str, Any]] = []

    for seed in args.seeds:
        seed_config = make_seed_config(
            base_config=base_config,
            seed=seed,
            output_dir=output_dir,
        )

        seed_config_path = generated_config_dir / f"{base_config_path.stem}_seed{seed}.yaml"
        save_yaml(seed_config, seed_config_path)

        print(f"\nSeed {seed}")
        print(f"Saved seed config: {seed_config_path}")

        try:
            run_training(
                config_path=seed_config_path,
                module_name=module_name,
                dry_run=args.dry_run,
            )
            status = "completed" if not args.dry_run else "dry_run"
        except subprocess.CalledProcessError as exc:
            status = f"failed_exit_{exc.returncode}"
            print(f"Seed {seed} failed with exit code {exc.returncode}")

            if not args.continue_on_error:
                raise

        row = collect_seed_result(
            seed=seed,
            config=seed_config,
            project_root=project_root,
        )
        row["status"] = status if row["status"] == "missing_run_dir" else row["status"]
        rows.append(row)

        write_summary_csv(rows, project_root / args.summary_csv)
        write_summary_json(rows, project_root / args.summary_json)

        print(f"Updated summary: {args.summary_csv}")

    print("\nMulti-seed run complete.")
    print(f"CSV summary: {args.summary_csv}")
    print(f"JSON summary: {args.summary_json}")

    summary = compute_mean_std(rows)

    if summary:
        print("\nMean ± std:")
        for metric in ["accuracy", "macro_f1", "weighted_f1", "balanced_accuracy"]:
            mean_key = f"{metric}_mean"
            std_key = f"{metric}_std"
            if mean_key in summary:
                print(f"{metric}: {summary[mean_key]:.4f} ± {summary[std_key]:.4f}")


if __name__ == "__main__":
    main()