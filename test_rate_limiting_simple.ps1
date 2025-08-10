# Simple Rate Limiting Test
# Usage: .\test_rate_limiting_simple.ps1

$BaseUrl = "http://127.0.0.1:8000"

Write-Host "Simple Rate Limiting Test" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Test 1: Basic login test
Write-Host "`n1. Testing basic login..." -ForegroundColor Yellow
$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
    Write-Host "SUCCESS: Login successful" -ForegroundColor Green
    Write-Host "  Token: $($response.access_token)" -ForegroundColor Gray
    $token = $response.access_token
    $headers = @{ "Authorization" = "Bearer $token" }
} catch {
    Write-Host "FAILED: Login failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    exit 1
}

# Test 2: Test rate limiting by making multiple requests
Write-Host "`n2. Testing rate limiting on login endpoint..." -ForegroundColor Yellow
$rateLimitHit = $false
$attempts = 0

for ($i = 1; $i -le 20; $i++) {
    try {
        $attempts++
        $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
        Write-Host "  Attempt $i`: SUCCESS" -ForegroundColor Gray
    } catch {
        if ($_.Exception.Response.StatusCode -eq 429) {
            Write-Host "  Attempt $i`: RATE LIMITED (Expected after $attempts attempts)" -ForegroundColor Yellow
            $rateLimitHit = $true
            break
        } else {
            Write-Host "  Attempt $i`: FAILED - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    Start-Sleep -Milliseconds 100
}

if ($rateLimitHit) {
    Write-Host "Rate limiting working on login endpoint" -ForegroundColor Green
} else {
    Write-Host "Rate limiting not triggered on login endpoint (may need more attempts)" -ForegroundColor Yellow
}

Write-Host "`nRate limiting test completed!" -ForegroundColor Green
