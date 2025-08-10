# PowerShell script to check and resolve port conflicts
# Usage: .\check_ports.ps1

param(
    [int]$Port = 8003
)

Write-Host "🔍 Checking port $Port usage..." -ForegroundColor Yellow

# Check if port is in use
$portInUse = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue

if ($portInUse) {
    Write-Host "❌ Port $Port is already in use by:" -ForegroundColor Red
    foreach ($connection in $portInUse) {
        $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
        Write-Host "   Process ID: $($connection.OwningProcess)" -ForegroundColor Red
        Write-Host "   Process Name: $($process.ProcessName)" -ForegroundColor Red
        Write-Host "   Local Address: $($connection.LocalAddress):$($connection.LocalPort)" -ForegroundColor Red
        Write-Host "   State: $($connection.State)" -ForegroundColor Red
        Write-Host ""
    }
    
    $choice = Read-Host "Do you want to kill the process(es) using port $Port? (y/n)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        foreach ($connection in $portInUse) {
            try {
                Stop-Process -Id $connection.OwningProcess -Force
                Write-Host "✅ Killed process $($connection.OwningProcess)" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to kill process $($connection.OwningProcess): $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "ℹ️  You can manually kill the process or use a different port" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Port $Port is available" -ForegroundColor Green
}

# Check for alternative ports
Write-Host "`n🔍 Checking alternative ports..." -ForegroundColor Yellow
$alternativePorts = @(8000, 8001, 8002, 8004, 8005)
$availablePorts = @()

foreach ($altPort in $alternativePorts) {
    $altPortInUse = Get-NetTCPConnection -LocalPort $altPort -ErrorAction SilentlyContinue
    if (-not $altPortInUse) {
        $availablePorts += $altPort
    }
}

if ($availablePorts.Count -gt 0) {
    Write-Host "✅ Available alternative ports: $($availablePorts -join ', ')" -ForegroundColor Green
} else {
    Write-Host "❌ No alternative ports available in range 8000-8005" -ForegroundColor Red
}
