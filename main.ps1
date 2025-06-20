# Requires admin privileges for full setup
$ErrorActionPreference = "Stop"

Write-Host "🔍 Checking for Python..."
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "⚠️ Python not found. Installing Python 3.12.3..."
    $installerUrl = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
    $installerPath = "$env:TEMP\python_installer.exe"
    Invoke-WebRequest $installerUrl -OutFile $installerPath

    Start-Process -FilePath $installerPath -Wait -ArgumentList `
        "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1"

    Remove-Item $installerPath
    Write-Host "✅ Python installed."
} else {
    Write-Host "✅ Python is already installed."
}

# Refresh session with python in PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")

Write-Host "🐍 Ensuring pip is available..."
python -m ensurepip --upgrade

Write-Host "📦 Installing required packages..."
$packages = @("requests", "playsound3", "pillow", "pystray")

foreach ($pkg in $packages) {
    Write-Host "→ Installing $pkg..."
    python -m pip install --upgrade $pkg
}

Write-Host "`n✅ Setup complete!"
python main.py
