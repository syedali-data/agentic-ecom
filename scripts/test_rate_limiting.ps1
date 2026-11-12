# Rate Limiting Test Script
# Usage: .\test_rate_limiting.ps1

$BaseUrl = "http://127.0.0.1:8000"

Write-Host "Testing Rate Limiting" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan

# Test 1: Login to get token
Write-Host "`n1. Logging in..." -ForegroundColor Yellow
$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
    $token = $response.access_token
    $headers = @{ "Authorization" = "Bearer $token" }
    Write-Host "SUCCESS: Login successful" -ForegroundColor Green
} catch {
    Write-Host "FAILED: Login failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Test rate limiting on login endpoint (should be more restrictive)
Write-Host "`n2. Testing rate limiting on login endpoint..." -ForegroundColor Yellow
$rateLimitHit = $false
$attempts = 0

for ($i = 1; $i -le 15; $i++) {
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

# Test 3: Test rate limiting on safety status endpoint
Write-Host "`n3. Testing rate limiting on safety status endpoint..." -ForegroundColor Yellow
$rateLimitHit = $false
$attempts = 0

for ($i = 1; $i -le 50; $i++) {
    try {
        $attempts++
        $response = Invoke-RestMethod -Uri "$BaseUrl/safety/status" -Method Get -Headers $headers
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
    Start-Sleep -Milliseconds 50
}

if ($rateLimitHit) {
    Write-Host "Rate limiting working on safety status endpoint" -ForegroundColor Green
} else {
    Write-Host "Rate limiting not triggered on safety status endpoint (may need more attempts)" -ForegroundColor Yellow
}

# Test 4: Test rate limiting on trigger endpoint
Write-Host "`n4. Testing rate limiting on trigger endpoint..." -ForegroundColor Yellow
$rateLimitHit = $false
$attempts = 0

$triggerData = @{
    action = "test_action"
    count = 1
} | ConvertTo-Json

for ($i = 1; $i -le 15; $i++) {
    try {
        $attempts++
        $response = Invoke-RestMethod -Uri "$BaseUrl/trigger/sales-genie" -Method Post -Body $triggerData -ContentType "application/json" -Headers $headers
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
    Write-Host "Rate limiting working on trigger endpoint" -ForegroundColor Green
} else {
    Write-Host "Rate limiting not triggered on trigger endpoint (may need more attempts)" -ForegroundColor Yellow
}

# Test 5: Test normal read operation (should have higher limits)
Write-Host "`n5. Testing read operation (should have higher limits)..." -ForegroundColor Yellow
$successCount = 0

for ($i = 1; $i -le 50; $i++) {
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/products" -Method Get -Headers $headers
        $successCount++
        Write-Host "  Attempt $i`: SUCCESS" -ForegroundColor Gray
    } catch {
        if ($_.Exception.Response.StatusCode -eq 429) {
            Write-Host "  Attempt $i`: RATE LIMITED after $successCount successful requests" -ForegroundColor Yellow
            break
        } else {
            Write-Host "  Attempt $i`: FAILED - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    Start-Sleep -Milliseconds 50
}

Write-Host "Read operations completed: $successCount successful requests" -ForegroundColor Green

Write-Host "`nRate limiting testing completed!" -ForegroundColor Green
Write-Host "Note: Rate limits may vary based on configuration and environment." -ForegroundColor Gray
