# Docker Usage for TerraSight

This document provides container-based commands for verifying and running the TerraSight submission package without relying on the host Python environment.

## Build the image

```bash
docker build -t terrasight .
```

## Verify package installation

```bash
docker run --rm terrasight python -c "import terrasight; print('Installation successful')"
```

## Run the report asset checker

```bash
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/reports:/app/reports" -v "$(pwd)/results:/app/results" -v "$(pwd)/experiments:/app/experiments" terrasight python -m terrasight.reporting.check_report_assets --show-discovered --strict
```

## Run the test suite

```bash
docker run --rm -v "$(pwd):/app" terrasight pytest
```

## Run the reproducibility command tests only

```bash
docker run --rm -v "$(pwd):/app" terrasight pytest tests/test_reproducibility_commands.py
```

## Docker Compose shortcuts

```bash
docker compose run --rm terrasight
docker compose run --rm asset-check
```

## Notes

- Raw EuroSAT data, generated reports, model outputs, and experiment logs are mounted as volumes rather than copied into the Docker image.
- This keeps the image lightweight and avoids distributing large datasets or trained checkpoints inside the container.
- The Dockerfile installs the local package in editable mode so CLI entry points such as `python -m terrasight.reporting.check_report_assets` are available inside the container.
