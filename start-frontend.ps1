# Start Frontend Server
Write-Host "⚛️  Starting Frontend Server..." -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

cd $PSScriptRoot\frontend

# Install dependencies if needed
if (-not (Test-Path node_modules)) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Start dev server
Write-Host "`n✅ Starting server on http://localhost:3000`n" -ForegroundColor Green
npm run dev
