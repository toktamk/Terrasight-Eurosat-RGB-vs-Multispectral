$env:KMP_DUPLICATE_LIB_OK="TRUE"

Write-Host "Creating stratified train/test split..."
python -m terrasight.data.split --config configs\v1_rgb_baseline.yaml

Write-Host "Running RGB baseline..."
python -m terrasight.pipelines.train_rgb --config configs\v1_rgb_baseline.yaml

Write-Host "Running multispectral baseline..."
python -m terrasight.pipelines.train_multispectral --config configs\v1_multispectral.yaml

Write-Host "Generating comparison table..."
python -m terrasight.reporting.comparison --registry experiments\registry.csv --output reports\tables\comparison_table.csv

Write-Host "V1 reproducibility pipeline complete."