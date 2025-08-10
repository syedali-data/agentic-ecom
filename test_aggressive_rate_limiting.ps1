# Aggressive Rate Limiting Test
$BaseUrl = "http://127.0.0.1:8000"

Write-Host "Testing Aggressive Rate Limiting" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Test 1: Login with aggressive rate limiting (5 requests per 15 minutes)
Write-Host "`n1. Testing aggressive rate limiting (5 requests per 15 minutes)..." -ForegroundColor Yellow

$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$successCount = 0
$rateLimitedCount = 0

for ($i = 1; $i -le 10; $i++) {
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
        $successCount++
        Write-Host "  Attempt $i`: SUCCESS" -ForegroundColor Green
    } catch {
        if ($_.Exception.Response.StatusCode -eq 429) {
            $rateLimitedCount++
            Write-Host "  Attempt $i`: RATE LIMITED (429)" -ForegroundColor Red
        } else {
            Write-Host "  Attempt $i`: ERROR - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    Start-Sleep -Milliseconds 100
}

Write-Host "`nResults:" -ForegroundColor Yellow
Write-Host "  Successful requests: $successCount" -ForegroundColor Green
Write-Host "  Rate limited requests: $rateLimitedCount" -ForegroundColor Red

# Test 2: Check rate limiting headers (if implemented)
Write-Host "`n2. Testing rate limiting headers..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
    Write-Host "  Headers test: SUCCESS" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 429) {
        Write-Host "  Headers test: RATE LIMITED (Expected)" -ForegroundColor Yellow
    } else {
        Write-Host "  Headers test: ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 3: Test different endpoints for rate limiting
Write-Host "`n3. Testing other endpoints for rate limiting..." -ForegroundColor Yellow

# Test safety status endpoint
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/safety/status" -Method Get
    Write-Host "  Safety status: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "  Safety status: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# Test health endpoint (should not be rate limited)
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
    Write-Host "  Health check: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "  Health check: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nAggressive Rate Limiting Test Completed!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
