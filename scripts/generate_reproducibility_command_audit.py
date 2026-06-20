from __future__ import annotations

import ast
import csv
import importlib.util
import re
import shlex
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT_ROOT / "reports" / "tables" / "reproducibility_command_audit.csv"

COMMAND_SOURCES = [
    PROJECT_ROOT / "docs" / "reproducibility_report.md",
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "tests" / "test_reproducibility_commands.py",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def extract_python_module_commands(text: str) -> set[str]:
    commands = set(re.findall(r"python(?:3)? -m [^`\n]+", text))
    commands.update(re.findall(r"pytest(?: [^`\n]+)?", text))
    return {cmd.strip() for cmd in commands}


def module_name(command: str) -> str:
    parts = shlex.split(command)
    return parts[parts.index("-m") + 1] if "-m" in parts else ""


def used_options(command: str) -> set[str]:
    return {part for part in shlex.split(command) if part.startswith("--")}


def argparse_options(module: str) -> set[str]:
    spec = importlib.util.find_spec(module)
    if spec is None or spec.origin is None:
        return set()
    source = Path(spec.origin).read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(source)
    options: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value.startswith("--"):
                    options.add(arg.value)
    return options


def command_exists(command: str) -> bool:
    if command.startswith("pytest"):
        return True
    mod = module_name(command)
    return bool(mod and importlib.util.find_spec(mod) is not None)


def main() -> None:
    texts = {path.name: read(path) for path in COMMAND_SOURCES}
    commands = sorted(set().union(*(extract_python_module_commands(t) for t in texts.values())))
    rows = []
    for cmd in commands:
        mod = module_name(cmd) if " -m " in cmd else ""
        defined = argparse_options(mod) if mod else set()
        used = used_options(cmd)
        missing = sorted(used - defined) if mod else []
        rows.append(
            {
                "command": cmd,
                "module": mod,
                "command_exists_in_code": command_exists(cmd),
                "appears_in_README": cmd in texts.get("README.md", ""),
                "appears_in_reproducibility_report": cmd in texts.get("reproducibility_report.md", ""),
                "appears_in_test_file": cmd in texts.get("test_reproducibility_commands.py", ""),
                "argparse_accepts_all_options": not missing,
                "missing_argparse_options": ";".join(missing),
            }
        )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
