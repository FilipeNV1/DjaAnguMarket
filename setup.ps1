$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot

Write-Host '=== DjanGoMarket setup ===' -ForegroundColor Cyan

if (-not (Test-Path "$root\venv")) {
    Write-Host 'Creating virtual environment...'
    py -3 -m venv "$root\venv"
}

Write-Host 'Installing Python dependencies...'
& "$root\venv\Scripts\pip.exe" install -r "$root\django\requirements.txt" -q

if (-not (Test-Path "$root\django\.env")) {
    if (Test-Path "$root\.env") {
        Copy-Item "$root\.env" "$root\django\.env"
        Write-Host 'Copied .env to django/.env'
    } elseif (Test-Path "$root\django\.env.example") {
        Copy-Item "$root\django\.env.example" "$root\django\.env"
        Write-Host 'Created django/.env from example (edit SECRET_KEY!)'
    }
}

Write-Host 'Running migrations and seed data...'
& "$root\venv\Scripts\python.exe" "$root\django\manage.py" migrate
& "$root\venv\Scripts\python.exe" "$root\django\setup_groups.py"
& "$root\venv\Scripts\python.exe" "$root\django\populate_db.py"

Write-Host 'Installing Angular dependencies...'
Push-Location "$root\angular"
npm install --silent
Pop-Location

Write-Host 'Running API smoke test...'
& "$root\venv\Scripts\python.exe" "$root\django\smoke_test.py"

Write-Host ''
Write-Host 'Setup complete!' -ForegroundColor Green
Write-Host 'Start dev servers with: .\run-dev.ps1'