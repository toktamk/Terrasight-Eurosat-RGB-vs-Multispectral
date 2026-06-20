from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "docs" / "reproducibility_status.md"


CHECKS = [
    {
        "name": "Package import",
        "command": ["python", "-c", "import terrasight; print('TerraSight import successful')"],
    },
    {
        "name": "Unit tests",
        "command": ["pytest"],
    },
    {
        "name": "Reproducibility command tests",
        "command": ["pytest", "tests/test_reproducibility_commands.py"],
    },
    {
        "name": "Report asset validation",
        "command": [
            "python",
            "-m",
            "terrasight.reporting.check_report_assets",
            "--show-discovered",
            "--strict",
        ],
    },
]


EXPECTED_PATHS = [
    "experiments/registry.csv",
    "reports/tables/statistical_tests/statistical_analysis.csv",
    "reports/tables/statistical_tests/statistical_summary.md",
    "reports/tables/spectral_analysis/class_mean_signatures.csv",
    "reports/tables/spectral_analysis/bhattacharyya_distances.csv",
    "reports/tables/spectral_analysis/spectral_angles.csv",
    "reports/figures/spectral_analysis/bhattacharyya_heatmap.png",
    "reports/figures/spectral_analysis/spectral_angle_heatmap.png",
    "reports/figures/reliability",
    "reports/figures/gradcam",
    "reports/figures/robustness",
    "reports/figures/failure_cases",
]


def run_command(command: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode == 0, output[-3000:]
    except Exception as exc:
        return False, str(exc)


def check_path(path: str) -> bool:
    return (PROJECT_ROOT / path).exists()


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    command_results = []
    for check in CHECKS:
        passed, output = run_command(check["command"])
        command_results.append(
            {
                "name": check["name"],
                "command": " ".join(check["command"]),
                "passed": passed,
                "output": output,
            }
        )

    path_results = [
        {"path": path, "exists": check_path(path)}
        for path in EXPECTED_PATHS
    ]

    all_commands_passed = all(item["passed"] for item in command_results)
    all_paths_exist = all(item["exists"] for item in path_results)
    overall_status = "PASSED" if all_commands_passed and all_paths_exist else "PARTIAL / FAILED"

    lines = [
        "# Reproducibility Status",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Overall status: **{overall_status}**",
        "",
        "## Command Verification",
        "",
        "| Check | Status | Command |",
        "|---|---:|---|",
    ]

    for item in command_results:
        status = "✓" if item["passed"] else "✗"
        lines.append(f"| {item['name']} | {status} | `{item['command']}` |")

    lines.extend(
        [
            "",
            "## Artifact Verification",
            "",
            "| Artifact | Status |",
            "|---|---:|",
        ]
    )

    for item in path_results:
        status = "✓" if item["exists"] else "✗"
        lines.append(f"| `{item['path']}` | {status} |")

    lines.extend(
        [
            "",
            "## Command Outputs",
            "",
        ]
    )

    for item in command_results:
        lines.append(f"### {item['name']}")
        lines.append("")
        lines.append("```text")
        lines.append(item["output"] if item["output"] else "No output.")
        lines.append("```")
        lines.append("")

    lines.extend(
        [
            "## Conclusion",
            "",
            "This file records the reproducibility verification status for the TerraSight submission package.",
            "It should be regenerated immediately before final submission.",
            "",
        ]
    )

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved reproducibility status to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()