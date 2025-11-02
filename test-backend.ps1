# Quick Backend Connection Test
Write-Host "Testing Backend Connection..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Basic connection
Write-Host "1. Testing backend health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 2
    Write-Host "   ✓ Backend is running!" -ForegroundColor Green
    Write-Host "   Response: $($response.message)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Backend not accessible!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "SOLUTION: Make sure backend is running:" -ForegroundColor Cyan
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  python -m uvicorn app.main:app --reload" -ForegroundColor White
    exit
}

Write-Host ""

# Test 2: Signup endpoint
Write-Host "2. Testing signup endpoint..." -ForegroundColor Yellow
$testEmail = "test$(Get-Random)@example.com"
$testBody = @{
    email = $testEmail
    password = "test123456"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "http://localhost:8000/auth/signup" `
        -Method POST `
        -ContentType "application/json" `
        -Body $testBody
    
    Write-Host "   ✓ Signup endpoint works!" -ForegroundColor Green
    Write-Host "   Created user: $($result.email) (Role: $($result.role))" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Signup endpoint error" -ForegroundColor Red
    $errorResponse = $_.ErrorDetails.Message
    Write-Host "   Error: $errorResponse" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "If both tests pass, your backend is working correctly!" -ForegroundColor Green
Write-Host "The signup issue is likely in the frontend connection." -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Check browser console (F12) when signing up" -ForegroundColor White
Write-Host "  2. Verify VITE_API_BASE in frontend/.env.local" -ForegroundColor White
Write-Host "  3. Restart frontend server" -ForegroundColor White
