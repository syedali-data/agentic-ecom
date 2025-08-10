# Simple PowerShell script to test Agentic-Ecom API
# Usage: .\test_api_simple.ps1

$BaseUrl = "http://127.0.0.1:8000"

Write-Host "Testing Agentic-Ecom API" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

# Test 1: Public endpoints
Write-Host "`n1. Testing public endpoints..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/" -Method Get
    Write-Host "SUCCESS: Public endpoint accessible" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "ERROR: Public endpoint error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Protected endpoints (should fail)
Write-Host "`n2. Testing protected endpoints (should fail without auth)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/products" -Method Get
    Write-Host "ERROR: Protected endpoint should require auth but didn't" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "SUCCESS: Protected endpoint correctly requires authentication" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Protected endpoint error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 3: Login
Write-Host "`n3. Testing login..." -ForegroundColor Yellow
$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
    Write-Host "SUCCESS: Login successful" -ForegroundColor Green
    Write-Host "Token: $($response.access_token.Substring(0, 20))..." -ForegroundColor Gray
    Write-Host "Role: $($response.user_role)" -ForegroundColor Gray
    Write-Host "Expires in: $($response.expires_in) seconds" -ForegroundColor Gray
    
    # Test 4: Use token to access protected endpoints
    Write-Host "`n4. Testing protected endpoints with token..." -ForegroundColor Yellow
    $headers = @{
        "Authorization" = "Bearer $($response.access_token)"
    }
    
    # Test products endpoint
    try {
        $productsResponse = Invoke-RestMethod -Uri "$BaseUrl/products" -Method Get -Headers $headers
        Write-Host "SUCCESS: Products endpoint accessible with token" -ForegroundColor Green
        Write-Host "Found $($productsResponse.Count) products" -ForegroundColor Gray
    } catch {
        Write-Host "ERROR: Products endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test analytics endpoint
    try {
        $analyticsResponse = Invoke-RestMethod -Uri "$BaseUrl/analytics/performance" -Method Get -Headers $headers
        Write-Host "SUCCESS: Analytics endpoint accessible with token" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Analytics endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "ERROR: Login failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nAPI testing completed!" -ForegroundColor Green
