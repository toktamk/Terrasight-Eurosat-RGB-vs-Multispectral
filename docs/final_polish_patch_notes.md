# TerraSight Final Polish Patch Notes

Generated deliverables:

- `reports/tables/reproducibility_command_audit.csv`
- `scripts/generate_reproducibility_command_audit.py`
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `docs/docker_usage.md`
- `scripts/generate_rgb_failure_ms_success_gallery.py`
- `docs/rgb_failure_ms_success_case_study.md`

## Immediate Use

Copy these files into the repository root, then run:

```bash
python scripts/generate_reproducibility_command_audit.py
docker build -t terrasight .
docker run --rm terrasight python -c "import terrasight; print('Installation successful')"
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/reports:/app/reports" -v "$(pwd)/results:/app/results" -v "$(pwd)/experiments:/app/experiments" terrasight python -m terrasight.reporting.check_report_assets --show-discovered --strict
```

## Audit Summary

Commands audited from `tests/test_reproducibility_commands.py`: 36

Any row marked `CHECK` should be manually inspected before final submission.
