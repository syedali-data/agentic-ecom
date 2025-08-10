# Simple Login Test
$BaseUrl = "http://127.0.0.1:8000"

Write-Host "Testing Simple Login" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan

$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method Post -Body $loginData -ContentType "application/json"
    Write-Host "SUCCESS: Login works!" -ForegroundColor Green
    Write-Host "Token: $($response.access_token)" -ForegroundColor Gray
} catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
}
