Set-Location -Path $PSScriptRoot
Write-Host "-------------------------"
Write-Host "Linting Ruff..."
ruff format .
Write-Host "-------------------------"
Write-Host "Linting Isort..."
isort . --profile black
Write-Host "-------------------------"
Write-Host "Black..."
black .