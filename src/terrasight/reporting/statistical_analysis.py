from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score


METRICS = ("accuracy", "macro_f1", "balanced_accuracy")


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def compute_metric(y_true: np.ndarray, y_pred: np.ndarray, metric: str) -> float:
    if metric == "accuracy":
        return float(accuracy_score(y_true, y_pred))
    if metric == "macro_f1":
        return float(f1_score(y_true, y_pred, average="macro"))
    if metric == "balanced_accuracy":
        return float(balanced_accuracy_score(y_true, y_pred))
    raise ValueError(f"Unsupported metric: {metric}")


def bootstrap_metric_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metric: str,
    n_bootstrap: int,
    seed: int,
) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(y_true)
    values: list[float] = []

    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        values.append(compute_metric(y_true[idx], y_pred[idx], metric))

    arr = np.asarray(values, dtype=float)
    return (
        float(np.mean(arr)),
        float(np.percentile(arr, 2.5)),
        float(np.percentile(arr, 97.5)),
    )


def bootstrap_delta_ci(
    y_true: np.ndarray,
    pred_a: np.ndarray,
    pred_b: np.ndarray,
    metric: str,
    n_bootstrap: int,
    seed: int,
) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(y_true)
    deltas: list[float] = []

    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        score_a = compute_metric(y_true[idx], pred_a[idx], metric)
        score_b = compute_metric(y_true[idx], pred_b[idx], metric)
        deltas.append(score_b - score_a)

    arr = np.asarray(deltas, dtype=float)
    return (
        float(np.mean(arr)),
        float(np.percentile(arr, 2.5)),
        float(np.percentile(arr, 97.5)),
    )


def mcnemar_test(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict[str, float | int]:
    a_correct = df_a["correct"].to_numpy().astype(bool)
    b_correct = df_b["correct"].to_numpy().astype(bool)

    b01 = int(np.sum(a_correct & ~b_correct))
    b10 = int(np.sum(~a_correct & b_correct))
    total = b01 + b10

    if total == 0:
        statistic = 0.0
        p_value = 1.0
    else:
        statistic = (abs(b01 - b10) - 1) ** 2 / total
        p_value = math.erfc(math.sqrt(statistic / 2))

    return {
        "b01_model_a_correct_model_b_wrong": b01,
        "b10_model_a_wrong_model_b_correct": b10,
        "statistic": float(statistic),
        "p_value": float(p_value),
    }


def load_predictions(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    required = {"path", "true_label", "predicted_label"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    if "correct" not in df.columns:
        df["correct"] = df["true_label"] == df["predicted_label"]

    return df.sort_values("path").reset_index(drop=True)

def validate_pairing(df_a: pd.DataFrame, df_b: pd.DataFrame) -> None:
    if len(df_a) != len(df_b):
        raise ValueError("Prediction files have different lengths.")

    if not df_a["path"].equals(df_b["path"]):
        raise ValueError(
            "Prediction files do not contain the same ordered samples after sorting by path."
        )

    if not df_a["true_label"].equals(df_b["true_label"]):
        raise ValueError("Prediction files have inconsistent true labels.")


def percentage(value: float) -> float:
    return 100.0 * value


def write_markdown_summary(
    path: Path,
    model_a_name: str,
    model_b_name: str,
    result_df: pd.DataFrame,
    mcnemar: dict[str, float | int],
) -> None:
    delta_rows = result_df[result_df["analysis"] == "bootstrap_delta_ci"]

    lines = [
        "# Statistical Validation Summary",
        "",
        f"Comparison: **{model_a_name}** vs **{model_b_name}**.",
        "",
        "Both models were evaluated on the same paired test samples. "
        "Bootstrap confidence intervals estimate metric uncertainty, while McNemar's test "
        "evaluates whether the two models make significantly different paired errors.",
        "",
        "## Bootstrap Improvement Confidence Intervals",
        "",
        "| Metric | Mean Difference, B-A (%) | 95% CI Low (%) | 95% CI High (%) | Interpretation |",
        "|---|---:|---:|---:|---|",
    ]

    for _, row in delta_rows.iterrows():
        metric = str(row["metric"])
        mean = percentage(float(row["mean"]))
        low = percentage(float(row["ci_low"]))
        high = percentage(float(row["ci_high"]))

        if low > 0:
            interpretation = "favours model B; CI excludes zero"
        elif high < 0:
            interpretation = "favours model A; CI excludes zero"
        else:
            interpretation = "CI overlaps zero"

        lines.append(
            f"| {metric} | {mean:.3f} | {low:.3f} | {high:.3f} | {interpretation} |"
        )

    p_value = float(mcnemar["p_value"])
    significance = "statistically significant" if p_value < 0.05 else "not statistically significant"

    lines.extend(
        [
            "",
            "## McNemar Test",
            "",
            "| Quantity | Value |",
            "|---|---:|",
            f"| Model A correct / Model B wrong | {mcnemar['b01_model_a_correct_model_b_wrong']} |",
            f"| Model A wrong / Model B correct | {mcnemar['b10_model_a_wrong_model_b_correct']} |",
            f"| McNemar statistic | {float(mcnemar['statistic']):.6f} |",
            f"| p-value | {p_value:.6f} |",
            "",
            f"Conclusion: the paired prediction difference is **{significance}** at p < 0.05.",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run paired statistical analysis between two prediction files."
    )
    parser.add_argument("--model-a", required=True, help="Prediction CSV for model A.")
    parser.add_argument("--model-b", required=True, help="Prediction CSV for model B.")
    parser.add_argument("--model-a-name", default="model_a")
    parser.add_argument("--model-b-name", default="model_b")
    parser.add_argument(
        "--output",
        default="reports/tables/statistical_tests/statistical_analysis.csv",
    )
    parser.add_argument(
        "--summary",
        default="reports/tables/statistical_tests/statistical_summary.md",
    )
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    project_root = get_project_root()

    df_a = load_predictions(project_root / args.model_a)
    df_b = load_predictions(project_root / args.model_b)
    validate_pairing(df_a, df_b)

    y_true = df_a["true_label"].to_numpy()
    pred_a = df_a["predicted_label"].to_numpy()
    pred_b = df_b["predicted_label"].to_numpy()

    rows: list[dict[str, object]] = []

    for model_name, pred in [
        (args.model_a_name, pred_a),
        (args.model_b_name, pred_b),
    ]:
        for metric in METRICS:
            mean, low, high = bootstrap_metric_ci(
                y_true=y_true,
                y_pred=pred,
                metric=metric,
                n_bootstrap=args.bootstrap,
                seed=args.seed,
            )
            rows.append(
                {
                    "analysis": "bootstrap_ci",
                    "model": model_name,
                    "metric": metric,
                    "mean": mean,
                    "ci_low": low,
                    "ci_high": high,
                    "p_value": "",
                    "b01_model_a_correct_model_b_wrong": "",
                    "b10_model_a_wrong_model_b_correct": "",
                }
            )

    for metric in METRICS:
        mean, low, high = bootstrap_delta_ci(
            y_true=y_true,
            pred_a=pred_a,
            pred_b=pred_b,
            metric=metric,
            n_bootstrap=args.bootstrap,
            seed=args.seed,
        )
        rows.append(
            {
                "analysis": "bootstrap_delta_ci",
                "model": f"{args.model_b_name} - {args.model_a_name}",
                "metric": metric,
                "mean": mean,
                "ci_low": low,
                "ci_high": high,
                "p_value": "",
                "b01_model_a_correct_model_b_wrong": "",
                "b10_model_a_wrong_model_b_correct": "",
            }
        )

    mc = mcnemar_test(df_a, df_b)

    rows.append(
        {
            "analysis": "mcnemar",
            "model": f"{args.model_a_name}_vs_{args.model_b_name}",
            "metric": "paired_correctness",
            "mean": mc["statistic"],
            "ci_low": "",
            "ci_high": "",
            "p_value": mc["p_value"],
            "b01_model_a_correct_model_b_wrong": mc[
                "b01_model_a_correct_model_b_wrong"
            ],
            "b10_model_a_wrong_model_b_correct": mc[
                "b10_model_a_wrong_model_b_correct"
            ],
        }
    )

    output_path = project_root / args.output
    summary_path = project_root / args.summary

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result_df = pd.DataFrame(rows)
    result_df.to_csv(output_path, index=False)

    write_markdown_summary(
        path=summary_path,
        model_a_name=args.model_a_name,
        model_b_name=args.model_b_name,
        result_df=result_df,
        mcnemar=mc,
    )

    print(f"Saved CSV: {output_path}")
    print(f"Saved summary: {summary_path}")
    print("McNemar result:")
    print(mc)


if __name__ == "__main__":
    main()