# Test script for Safety Integration
# Usage: .\test_safety_integration.ps1

$BaseUrl = "http://127.0.0.1:8000"

Write-Host "🔒 Testing Safety Integration" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

# Test 1: Login to get token
Write-Host "`n1. Logging in..." -ForegroundColor Yellow
$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
    $token = $response.access_token
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    Write-Host "✅ Login successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Check safety status
Write-Host "`n2. Checking safety status..." -ForegroundColor Yellow
try {
    $safetyStatus = Invoke-RestMethod -Uri "$BaseUrl/safety/status" -Method Get -Headers $headers
    Write-Host "✅ Safety status retrieved" -ForegroundColor Green
    Write-Host "   Environment: $($safetyStatus.data.environment)" -ForegroundColor Gray
    Write-Host "   Daily spend: $($safetyStatus.data.daily_spend)" -ForegroundColor Gray
    Write-Host "   Max budget: $($safetyStatus.data.max_budget)" -ForegroundColor Gray
    Write-Host "   Dry run mode: $($safetyStatus.data.dry_run_mode)" -ForegroundColor Gray
    Write-Host "   Kill switch: $($safetyStatus.data.kill_switch_active)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Safety status failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Check safety for an action
Write-Host "`n3. Checking safety for action..." -ForegroundColor Yellow
try {
    $safetyCheck = Invoke-RestMethod -Uri "$BaseUrl/safety/check?action=generate_product_listing&platform=shopify" -Method Get -Headers $headers
    Write-Host "✅ Safety check completed" -ForegroundColor Green
    Write-Host "   Action: $($safetyCheck.action)" -ForegroundColor Gray
    Write-Host "   Safe: $($safetyCheck.safe)" -ForegroundColor Gray
    Write-Host "   Reason: $($safetyCheck.reason)" -ForegroundColor Gray
    Write-Host "   Requires approval: $($safetyCheck.requires_approval)" -ForegroundColor Gray
    Write-Host "   Dry run: $($safetyCheck.dry_run)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Safety check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Test write operation (should be gated)
Write-Host "`n4. Testing write operation (should be gated)..." -ForegroundColor Yellow
$productData = @{
    name = "Test Product"
    description = "Test product for safety check"
    category = "electronics"
    price = 99.99
} | ConvertTo-Json

try {
    $writeResponse = Invoke-RestMethod -Uri "$BaseUrl/products/generate-listing" -Method Post -Body $productData -ContentType "application/json" -Headers $headers
    Write-Host "✅ Write operation completed" -ForegroundColor Green
    Write-Host "   Response: $($writeResponse | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    if ($_.Exception.Response.StatusCode -eq 403) {
        Write-Host "✅ Write operation correctly blocked by safety check" -ForegroundColor Green
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    } else {
        Write-Host "❌ Write operation failed unexpectedly: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 5: Test trigger operation
Write-Host "`n5. Testing trigger operation..." -ForegroundColor Yellow
try {
    $triggerData = @{
        action = "test_action"
        count = 1
    } | ConvertTo-Json

    $triggerResponse = Invoke-RestMethod -Uri "$BaseUrl/trigger/sales-genie" -Method Post -Body $triggerData -ContentType "application/json" -Headers $headers
    Write-Host "✅ Trigger operation completed" -ForegroundColor Green
    Write-Host "   Response: $($triggerResponse | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    if ($_.Exception.Response.StatusCode -eq 403) {
        Write-Host "✅ Trigger operation correctly blocked by safety check" -ForegroundColor Green
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    } else {
        Write-Host "❌ Trigger operation failed unexpectedly: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 6: Test read operation (should work normally)
Write-Host "`n6. Testing read operation (should work normally)..." -ForegroundColor Yellow
try {
    $readResponse = Invoke-RestMethod -Uri "$BaseUrl/products" -Method Get -Headers $headers
    Write-Host "✅ Read operation completed" -ForegroundColor Green
    Write-Host "   Found $($readResponse.Count) products" -ForegroundColor Gray
} catch {
    Write-Host "❌ Read operation failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Safety integration testing completed!" -ForegroundColor Green
