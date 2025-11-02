# Test signup endpoint directly
Write-Host "Testing Signup Endpoint" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

$testEmail = "testuser@example.com"
$testPassword = "test123456"

Write-Host "`nAttempting signup with:" -ForegroundColor Yellow
Write-Host "  Email: $testEmail"
Write-Host "  Password: $testPassword"

try {
    $body = @{
        email = $testEmail
        password = $testPassword
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/auth/signup" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -ErrorAction Stop

    Write-Host "`n[SUCCESS] Account created!" -ForegroundColor Green
    Write-Host "User ID: $($response.id)" -ForegroundColor Green
    Write-Host "Email: $($response.email)" -ForegroundColor Green
    Write-Host "Role: $($response.role)" -ForegroundColor Green
    
    if ($response.role -eq "admin") {
        Write-Host "`n[INFO] This is the first user - you are now an ADMIN!" -ForegroundColor Cyan
    }
} catch {
    Write-Host "`n[ERROR] Signup failed!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        $errorDetail = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "Error Message: $($errorDetail.detail)" -ForegroundColor Red
    } else {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure backend is running (http://localhost:8000)" -ForegroundColor Yellow
    Write-Host "2. Check backend terminal for error messages" -ForegroundColor Yellow
    Write-Host "3. Verify database is initialized" -ForegroundColor Yellow
}
