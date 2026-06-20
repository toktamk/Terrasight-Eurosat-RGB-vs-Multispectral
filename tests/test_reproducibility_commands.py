"""
Pytest checks for TerraSight reproducibility one-line commands.

Purpose
-------
This test file validates the reproducibility commands without launching expensive
training or reporting jobs. It checks that:

1. each `python -m ...` module exists;
2. each module source contains a `main()` entry point when used as a CLI;
3. command-line options used in the reproducibility commands are defined by the
   module's argparse parser;
4. file inputs such as config files and probability CSVs exist, unless they are
   intentionally written as placeholders such as <BEST_RUN_DIR> or <EXPERIMENT_ID>;
5. output parent directories can be created;
6. key function-level dependencies referenced by the source-code dependency map
   are import-resolvable.

How to use
----------
Save this file as:

    tests/test_reproducibility_commands.py

Then run:

    pytest tests/test_reproducibility_commands.py -q

These tests are intentionally static/safety tests. They do not train models.
"""

from __future__ import annotations

import ast
import importlib.util
import os
import shlex
from dataclasses import dataclass
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ReproCommand:
    name: str
    command: str
    requires_existing_inputs: bool = True
    allow_placeholders: bool = True


COMMANDS: list[ReproCommand] = [
    ReproCommand("create split", "python -m terrasight.data.split --config configs/v1_rgb_baseline.yaml"),
    ReproCommand("train rgb pretrained", "python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_baseline.yaml"),
    ReproCommand("train rgb scratch", "python -m terrasight.pipelines.train_rgb --config configs/v1_rgb_scratch.yaml"),
    ReproCommand("train ms scratch", "python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_scratch.yaml"),
    ReproCommand("train ms adapted", "python -m terrasight.pipelines.train_multispectral --config configs/v1_multispectral_pretrained_adapted.yaml"),
    ReproCommand("train v4 rgb", "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb.yaml"),
    ReproCommand("train v4 rgb nir", "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_nir.yaml"),
    ReproCommand("train v4 rgb rededge nir", "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_rededge_nir.yaml"),
    ReproCommand("train v4 rgb rededge nir swir", "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_rgb_rededge_nir_swir.yaml"),
    ReproCommand("train v4 physical bands", "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_physical_bands.yaml"),
    ReproCommand("train v4 full13 no b10", "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_full13_no_b10.yaml"),
    ReproCommand("train v4 full13", "python -m terrasight.pipelines.train_multispectral --config configs/v4_ablation_full13.yaml"),
    ReproCommand("multiseed best ms", "python -m terrasight.experiments.run_multiseed --config configs/v4_ablation_rgb_rededge_nir_swir.yaml --seeds 42 43 44 --continue-on-error"),
    ReproCommand("confusion matrices", "python -m terrasight.reporting.generate_confusion_matrices --results-root results --versions v1 v4 --output-figures reports/figures/confusion_matrices --output-tables reports/tables/predictions", requires_existing_inputs=False),
    ReproCommand("comparison figures", "python -m terrasight.reporting.generate_comparison_figures", requires_existing_inputs=False),
    ReproCommand("comparison table", "python -m terrasight.reporting.comparison --registry experiments/registry.csv --output reports/tables/comparison_table.csv", requires_existing_inputs=False),
    ReproCommand("final model comparison", "python -m terrasight.reporting.final_model_comparison", requires_existing_inputs=False),
    ReproCommand("class level analysis", "python -m terrasight.reporting.generate_class_level_analysis", requires_existing_inputs=False),
    ReproCommand("per class f1", "python -m terrasight.reporting.plot_per_class_f1", requires_existing_inputs=False),
    ReproCommand("v4 conclusions", "python -m terrasight.reporting.v4_scientific_conclusions", requires_existing_inputs=False),
    ReproCommand("prediction probabilities", "python -m terrasight.reporting.generate_prediction_probabilities --results-root results --versions v1 v4 --output-dir reports/tables/probabilities", requires_existing_inputs=False),
    ReproCommand("reliability analysis", "python -m terrasight.reporting.generate_reliability_analysis --input-dir reports/tables/probabilities --output-dir reports", requires_existing_inputs=False),
    ReproCommand(name="robustness analysis",command="python -m terrasight.reporting.generate_robustness_analysis --run-dir results/v4/<BEST_RUN_DIR> --output-table-dir reports/tables/robustness --output-figure-dir reports/figures/robustness",requires_existing_inputs=False),
    ReproCommand("band occlusion", "python -m terrasight.reporting.generate_band_occlusion --run-dir results/v4/<BEST_RUN_DIR> --output-dir reports/tables/band_occlusion", requires_existing_inputs=False),
    ReproCommand("class-specific importance", "python -m terrasight.reporting.generate_class_specific_importance --input reports/tables/band_occlusion/<EXPERIMENT_ID>_band_occlusion_details.csv --output-dir reports/tables/class_specific_importance --top-k 3", requires_existing_inputs=False),
    ReproCommand("failure cases", "python -m terrasight.reporting.generate_failure_cases --probabilities reports/tables/probabilities/<EXPERIMENT_ID>_probabilities.csv --output-dir reports/figures/failure_cases --max-examples 16", requires_existing_inputs=False),
    ReproCommand("gradcam correct", "python -m terrasight.reporting.generate_gradcam_examples --run-dir results/v4/<BEST_RUN_DIR> --selection-mode correct_high_confidence --target-layer layer3 --num-examples 8", requires_existing_inputs=False),
    ReproCommand("gradcam failure", "python -m terrasight.reporting.generate_gradcam_examples --run-dir results/v4/<BEST_RUN_DIR> --selection-mode high_confidence_failure --target-layer layer3 --num-examples 8", requires_existing_inputs=False),
    ReproCommand("feature space", "python -m terrasight.reporting.generate_feature_space_plots --run-dir results/v4/<BEST_RUN_DIR> --method both --max-samples 3000", requires_existing_inputs=False),
    ReproCommand("spectral signatures", "python -m terrasight.explainability.spectral_signatures --data-dir data/raw/multispectral --output-dir reports/figures/spectral_signatures", requires_existing_inputs=False),
    ReproCommand("architecture sensitivity", "python -m terrasight.reporting.generate_architecture_sensitivity", requires_existing_inputs=False),
    ReproCommand("model profile", "python -m terrasight.reporting.generate_model_profile", requires_existing_inputs=False),
    ReproCommand("industrial discussion", "python -m terrasight.reporting.generate_industrial_discussion", requires_existing_inputs=False),
    ReproCommand(name="statistical validation",
                 command='python -m terrasight.reporting.statistical_analysis --model-a reports/tables/probabilities/v4_ablation_rgb_resnet18_pretrained_adapted_seed42_probabilities.csv --model-b reports/tables/probabilities/v4_ablation_rgb_rededge_nir_swir_resnet18_pretrained_adapted_seed42_probabilities.csv --model-a-name "RGB ResNet18" --model-b-name "RGB+RedEdge+NIR+SWIR ResNet18" --output reports/tables/statistical_tests/statistical_analysis.csv --summary reports/tables/statistical_tests/statistical_summary.md --bootstrap 1000 --seed 42',
                 requires_existing_inputs=True,allow_placeholders=True),
    ReproCommand(
        name="spectral separability analysis",
        command="python -m terrasight.reporting.generate_spectral_separability --data-dir <MULTISPECTRAL_DATASET_DIR> --tables-dir reports/tables/spectral_analysis --figures-dir reports/figures/spectral_analysis",
        requires_existing_inputs=True,
        allow_placeholders=True,
    ),
    ReproCommand("report asset check", "python -m terrasight.reporting.check_report_assets --show-discovered --strict", requires_existing_inputs=False),
]


DEPENDENCY_MODULES = [
    "terrasight.data.band_registry",
    "terrasight.data.dataset",
    "terrasight.data.preprocessing",
    "terrasight.features.band_selection",
    "terrasight.models.backbone_factory",
    "terrasight.models.model_utils",
    "terrasight.models.rgb_model",
    "terrasight.models.multispectral_model",
    "terrasight.training.trainer",
    "terrasight.training.losses",
    "terrasight.training.optimizer_factory",
    "terrasight.training.scheduler_factory",
    "terrasight.evaluation.metrics",
    "terrasight.experiments.experiment_tracker",
    "terrasight.utils.config",
    "terrasight.utils.run_setup",
    "terrasight.reporting.generate_confusion_matrices",
    "terrasight.reporting.generate_prediction_probabilities",
    "terrasight.explainability.band_occlusion",
    "terrasight.explainability.class_specific_importance",
    "terrasight.explainability.spectral_attribution",
    "terrasight.reliability.high_confidence_failures",
    "terrasight.reliability.robustness_testing",
]


INPUT_OPTIONS = {
    "--config",
    "--run-dir",
    "--registry",
    "--input",
    "--probabilities",
    "--input-dir",
    "--results-root",
    "--data-dir",
}

OUTPUT_OPTIONS = {
    "--output",
    "--output-dir",
    "--output-figures",
    "--output-tables",
    "--table-output-dir",
    "--metadata-output",
    "--summary-csv",
    "--summary-json",
    "--generated-config-dir",
    "--missing-output",
}

OPTIONS_WITH_MULTIPLE_VALUES = {"--seeds", "--versions"}


def has_placeholder(value: str) -> bool:
    return "<" in value and ">" in value


def project_path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else PROJECT_ROOT / p


def module_to_source_path(module_name: str) -> Path:
    spec = importlib.util.find_spec(module_name)
    assert spec is not None, f"Module is not import-resolvable: {module_name}"
    assert spec.origin is not None, f"Module has no source origin: {module_name}"
    return Path(spec.origin)


def parse_source(module_name: str) -> ast.Module:
    source_path = module_to_source_path(module_name)
    return ast.parse(source_path.read_text(encoding="utf-8"))


def function_names(tree: ast.Module) -> set[str]:
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


def argparse_options(tree: ast.Module) -> set[str]:
    options: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value.startswith("--"):
                    options.add(arg.value)
    return options


def extract_module_name(command: str) -> str:
    parts = shlex.split(command)
    assert len(parts) >= 3, f"Command is too short: {command}"
    assert parts[0].endswith("python") or parts[0] in {"python", "python3"}, f"Command should start with python: {command}"
    assert parts[1] == "-m", f"Command should use module execution with -m: {command}"
    return parts[2]


def command_options_and_values(command: str) -> tuple[set[str], dict[str, list[str]]]:
    parts = shlex.split(command)
    args = parts[3:]
    options: set[str] = set()
    values: dict[str, list[str]] = {}
    i = 0
    while i < len(args):
        token = args[i]
        if not token.startswith("--"):
            i += 1
            continue
        options.add(token)
        values[token] = []
        i += 1
        while i < len(args) and not args[i].startswith("--"):
            values[token].append(args[i])
            if token not in OPTIONS_WITH_MULTIPLE_VALUES:
                i += 1
                break
            i += 1
    return options, values


@pytest.mark.parametrize("cmd", COMMANDS, ids=lambda c: c.name)
def test_cli_module_exists_and_has_main(cmd: ReproCommand) -> None:
    module_name = extract_module_name(cmd.command)
    tree = parse_source(module_name)
    funcs = function_names(tree)
    assert "main" in funcs, f"CLI module has no main() function: {module_name}"


@pytest.mark.parametrize("cmd", COMMANDS, ids=lambda c: c.name)
def test_command_uses_defined_argparse_options(cmd: ReproCommand) -> None:
    module_name = extract_module_name(cmd.command)
    tree = parse_source(module_name)
    defined_options = argparse_options(tree)
    used_options, _values = command_options_and_values(cmd.command)
    missing = sorted(used_options - defined_options)
    assert not missing, f"Command uses undefined argparse options for {module_name}: {missing}"


@pytest.mark.parametrize("cmd", COMMANDS, ids=lambda c: c.name)
def test_required_input_paths_exist_or_are_placeholders(cmd: ReproCommand) -> None:
    _options, values = command_options_and_values(cmd.command)
    for option, option_values in values.items():
        if option not in INPUT_OPTIONS:
            continue
        for value in option_values:
            if has_placeholder(value):
                assert cmd.allow_placeholders, f"Unexpected placeholder in {cmd.name}: {value}"
                continue
            if not cmd.requires_existing_inputs:
                continue
            p = project_path(value)
            assert p.exists(), f"Input for {cmd.name} does not exist: {option} {p}"


@pytest.mark.parametrize("cmd", COMMANDS, ids=lambda c: c.name)
def test_output_parent_directories_can_be_created(cmd: ReproCommand, tmp_path: Path) -> None:
    _options, values = command_options_and_values(cmd.command)
    for option, option_values in values.items():
        if option not in OUTPUT_OPTIONS:
            continue
        for value in option_values:
            if has_placeholder(value):
                continue
            p = project_path(value)
            parent = p if option.endswith("dir") or option in {"--output-dir", "--output-figures", "--output-tables", "--table-output-dir", "--generated-config-dir"} else p.parent
            parent.mkdir(parents=True, exist_ok=True)
            assert parent.exists() and os.access(parent, os.W_OK), f"Output parent is not writable: {parent}"


@pytest.mark.parametrize("module_name", DEPENDENCY_MODULES)
def test_dependency_modules_are_import_resolvable(module_name: str) -> None:
    spec = importlib.util.find_spec(module_name)
    assert spec is not None, f"Dependency module is not import-resolvable: {module_name}"
    assert spec.origin is not None and Path(spec.origin).exists(), f"Dependency source file missing: {module_name}"


def test_config_files_are_yaml_and_have_required_sections() -> None:
    config_paths = sorted((PROJECT_ROOT / "configs").glob("*.yaml"))
    assert config_paths, "No YAML configuration files found in configs/."

    required_top_level = {"experiment", "data", "model", "training"}
    for path in config_paths:
        text = path.read_text(encoding="utf-8")
        for key in required_top_level:
            assert f"{key}:" in text, f"Config {path} is missing top-level section: {key}"


def test_training_commands_reference_existing_config_files() -> None:
    training_commands = [cmd for cmd in COMMANDS if "train_" in cmd.command or "run_multiseed" in cmd.command or "data.split" in cmd.command]
    for cmd in training_commands:
        _options, values = command_options_and_values(cmd.command)
        for config_path in values.get("--config", []):
            p = project_path(config_path)
            assert p.exists(), f"Training/split command references missing config: {cmd.name}: {p}"


def test_no_command_uses_known_unstable_figuresnew_module() -> None:
    used_modules = {extract_module_name(cmd.command) for cmd in COMMANDS}
    assert "terrasight.reporting.figuresnew" not in used_modules, "Do not use figuresnew.py in the reproducibility workflow."
