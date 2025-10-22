#!/usr/bin/env pwsh

$winVenvPath = "..\kraken_env\Scripts\Activate.ps1"
$linuxVenvPath = "../kraken_env/bin/activate"

if (-not $env:VIRTUAL_ENV) {
    Write-Host "Virtual environment not active. Activating..."

    if (Test-Path $winVenvPath) {
        Write-Host "Windows environment detected. Activating virtual environment..."
        & $winVenvPath
        Write-Host "Virtual environment activated."

    } elseif (Test-Path $linuxVenvPath) {
        Write-Host "Linux environment detected. Activating virtual environment..."
        sh $linuxVenvPath
        Write-Host "Virtual environment activated."

    } else {
        Write-Host "Virtual environment not found, creating one under kraken_env name."
        python -m venv kraken_venv
        . $linuxVenvPath
        python -m pip install -r requirements.txt

    }

} else {
    Write-Host "Virtual environment is already active."
}

python -m app