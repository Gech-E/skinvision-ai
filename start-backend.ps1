# Start Backend Server
Write-Host "🚀 Starting Backend Server..." -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

cd $PSScriptRoot\backend

# Create venv if doesn't exist
if (-not (Test-Path .venv)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Start server
Write-Host "`n✅ Starting server on http://localhost:8000`n" -ForegroundColor Green
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000