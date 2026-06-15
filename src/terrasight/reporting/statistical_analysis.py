from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def bootstrap_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metric: str,
    n_bootstrap: int = 1000,
    seed: int = 42,
) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    values = []

    n = len(y_true)

    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        yt = y_true[idx]
        yp = y_pred[idx]

        if metric == "accuracy":
            value = accuracy_score(yt, yp)
        elif metric == "macro_f1":
            value = f1_score(yt, yp, average="macro")
        else:
            raise ValueError(metric)

        values.append(value)

    values = np.array(values)

    return (
        float(np.mean(values)),
        float(np.percentile(values, 2.5)),
        float(np.percentile(values, 97.5)),
    )


def mcnemar_test(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    a_correct = df_a["correct"].to_numpy().astype(bool)
    b_correct = df_b["correct"].to_numpy().astype(bool)

    b01 = int(np.sum(a_correct & ~b_correct))
    b10 = int(np.sum(~a_correct & b_correct))

    total = b01 + b10

    if total == 0:
        return {
            "b01_a_correct_b_wrong": b01,
            "b10_a_wrong_b_correct": b10,
            "statistic": 0.0,
            "p_value": 1.0,
        }

    statistic = (abs(b01 - b10) - 1) ** 2 / total
    p_value = math.erfc(math.sqrt(statistic / 2))

    return {
        "b01_a_correct_b_wrong": b01,
        "b10_a_wrong_b_correct": b10,
        "statistic": statistic,
        "p_value": p_value,
    }


def load_model(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.sort_values("path").reset_index(drop=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-a", required=True)
    parser.add_argument("--model-b", required=True)
    parser.add_argument("--output", default="reports/tables/statistical_analysis.csv")
    parser.add_argument("--bootstrap", type=int, default=1000)
    args = parser.parse_args()

    project_root = get_project_root()

    model_a_path = project_root / args.model_a
    model_b_path = project_root / args.model_b
    output_path = project_root / args.output

    df_a = load_model(model_a_path)
    df_b = load_model(model_b_path)

    if len(df_a) != len(df_b):
        raise ValueError("Model prediction files have different lengths.")

    rows = []

    for model_label, df in [("model_a", df_a), ("model_b", df_b)]:
        y_true = df["true_label"].to_numpy()
        y_pred = df["predicted_label"].to_numpy()

        for metric in ["accuracy", "macro_f1"]:
            mean, low, high = bootstrap_ci(
                y_true,
                y_pred,
                metric=metric,
                n_bootstrap=args.bootstrap,
            )

            rows.append(
                {
                    "analysis": "bootstrap_ci",
                    "model": model_label,
                    "metric": metric,
                    "mean": mean,
                    "ci_low": low,
                    "ci_high": high,
                }
            )

    mc = mcnemar_test(df_a, df_b)

    rows.append(
        {
            "analysis": "mcnemar",
            "model": "model_a_vs_model_b",
            "metric": "paired_correctness",
            "mean": mc["statistic"],
            "ci_low": "",
            "ci_high": "",
            "b01_a_correct_b_wrong": mc["b01_a_correct_b_wrong"],
            "b10_a_wrong_b_correct": mc["b10_a_wrong_b_correct"],
            "p_value": mc["p_value"],
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print("McNemar result:")
    print(mc)


if __name__ == "__main__":
    main()