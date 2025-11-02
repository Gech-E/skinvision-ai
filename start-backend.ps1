# Start Backend Server with Swagger
Write-Host "Starting SkinVision AI Backend..." -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = Join-Path $PSScriptRoot "backend"

# Check if virtual environment exists
if (-not (Test-Path (Join-Path $backendPath ".venv"))) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    cd $backendPath
    python -m venv .venv
}

# Start backend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'SkinVision AI Backend Server' -ForegroundColor Cyan; Write-Host '=================================' -ForegroundColor Cyan; Write-Host ''; .\.venv\Scripts\Activate.ps1; Write-Host 'Starting server on http://localhost:8000' -ForegroundColor Green; Write-Host 'Swagger UI: http://localhost:8000/docs' -ForegroundColor Yellow; Write-Host ''; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

Write-Host ""
Write-Host "Backend server is starting in a new window..." -ForegroundColor Green
Write-Host ""
Write-Host "Swagger UI will be available at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "API Root:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Opening Swagger UI in 5 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
Start-Process "http://localhost:8000/docs"
