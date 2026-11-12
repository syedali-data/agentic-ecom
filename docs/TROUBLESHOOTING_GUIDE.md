# Troubleshooting Guide for Agentic-Ecom API

## Common Issues and Solutions

### 1. Port Conflict (Error 10048)

**Problem**: Port 8003 is already in use by another process.

**Solutions**:

#### Option A: Check and Kill Process Using Port 8003
```powershell
# Run the port checker script
.\scripts\setup\check_ports.ps1

# Or manually check
Get-NetTCPConnection -LocalPort 8003

# Kill the process if needed
Stop-Process -Id <PROCESS_ID> -Force
```

#### Option B: Use a Different Port
1. Edit `api/fastapi_api.py` line 462:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change to 8000 or another available port
```

2. Update `test_auth.py` line 10:
```python
BASE_URL = "http://127.0.0.1:8000"  # Change to match new port
```

### 2. PowerShell curl Command Issues

**Problem**: Unix/Linux curl syntax doesn't work in PowerShell.

**Solutions**:

#### Use PowerShell Native Commands
```powershell
# Instead of: curl -X POST http://127.0.0.1:8003/auth/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin123"}'

# Use:
$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8003/auth/login" -Method Post -Body $loginData -ContentType "application/json"
```

#### Use the Provided PowerShell Script
```powershell
# Run the test script
.\test_api_powershell.ps1
```

### 3. bcrypt Version Compatibility Issue

**Problem**: `passlib` and `bcrypt` version incompatibility.

**Solution**:
```bash
# Update dependencies
pip install --upgrade bcrypt>=4.0.0
pip install --upgrade passlib[bcrypt]>=1.7.4
```

### 4. Authentication Testing

#### Test Public Endpoints
```powershell
# Test public endpoint
Invoke-RestMethod -Uri "http://127.0.0.1:8003/" -Method Get
```

#### Test Login
```powershell
# Login and get token
$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8003/auth/login" -Method Post -Body $loginData -ContentType "application/json"
$token = $response.access_token
```

#### Test Protected Endpoints
```powershell
# Use token to access protected endpoints
$headers = @{
    "Authorization" = "Bearer $token"
}

# Test products endpoint
Invoke-RestMethod -Uri "http://127.0.0.1:8003/products" -Method Get -Headers $headers

# Test analytics endpoint
Invoke-RestMethod -Uri "http://127.0.0.1:8003/analytics/performance" -Method Get -Headers $headers
```

### 5. Available User Accounts

The system comes with these pre-configured accounts:

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| admin | admin123 | admin | Full access |
| analyst | analyst123 | analytics | Analytics and reporting |
| support | support123 | support | Customer support |
| sales | sales123 | sales | Sales and product management |

### 6. API Endpoints

#### Public Endpoints (No Auth Required)
- `GET /` - Health check
- `GET /health` - System status

#### Protected Endpoints (Auth Required)
- `GET /products` - List all products
- `GET /products/{id}` - Get specific product
- `POST /products/generate-listing` - Generate AI listing
- `GET /analytics/performance` - Performance analytics
- `GET /customers` - Customer list
- `GET /orders` - Order list
- `GET /support/tickets` - Support tickets

### 7. Quick Start Commands

```powershell
# 1. Check port availability
.\scripts\setup\check_ports.ps1

# 2. Start the API (if port is available)
python api/fastapi_api.py

# 3. Test the API
.\test_api_powershell.ps1

# 4. Or test manually
Invoke-RestMethod -Uri "http://127.0.0.1:8003/" -Method Get
```

### 8. Environment Variables

Make sure these environment variables are set (optional):
```bash
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 9. Logs and Debugging

- Check `logs/` directory for application logs
- API logs are displayed in the console when running
- Use `--log-level debug` for more verbose logging

### 10. Common Error Codes

- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Insufficient permissions for the requested action
- `404 Not Found` - Endpoint or resource not found
- `500 Internal Server Error` - Server-side error (check logs)

## Need Help?

If you're still experiencing issues:

1. Check the logs in the `logs/` directory
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure no other processes are using the required ports
4. Try using a different port if 8003 is busy
5. Use the provided PowerShell scripts for testing
