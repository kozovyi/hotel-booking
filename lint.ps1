Set-Location -Path $PSScriptRoot
Write-Host "-------------------------"
Write-Host "Black..."
black .
Write-Host "-------------------------"
Write-Host "Mypy..."
mypy src
Write-Host "-------------------------"
Write-Host "Linting Ruff..."
ruff check src