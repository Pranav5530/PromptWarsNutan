# FoodLoop Full-Stack Development Launcher
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "   🌱 FoodLoop: Starting Development Environment          " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

$root = $PSScriptRoot
$backendDir = Join-Path $root "backend"
$frontendDir = Join-Path $root "frontend"

Write-Host "`n[1/3] Verifying Backend Service..." -ForegroundColor Cyan
try {
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✓ Backend is already running on http://127.0.0.1:8000" -ForegroundColor Green
} catch {
    Write-Host "Starting Backend FastAPI server in background..." -ForegroundColor Yellow
    Start-Process -FilePath "uv" -ArgumentList "run uvicorn app.main:app --port 8000 --reload" -WorkingDirectory $backendDir
    Start-Sleep -Seconds 3
}

Write-Host "`n[2/3] Verified Backend Endpoints:" -ForegroundColor Cyan
Write-Host "  • API Base:      http://127.0.0.1:8000/api/v1" -ForegroundColor Gray
Write-Host "  • Swagger Docs:  http://127.0.0.1:8000/docs" -ForegroundColor Gray
Write-Host "  • ReDoc:         http://127.0.0.1:8000/redoc" -ForegroundColor Gray

Write-Host "`n[3/3] Starting Next.js Frontend Server on http://localhost:3000..." -ForegroundColor Cyan
Set-Location $frontendDir
npm.cmd run dev
