
$ErrorActionPreference = 'Stop'

# Set working directory to the project folder
Set-Location $PSScriptRoot

$PythonPath = '.\.venv\Scripts\python.exe'
$ModelPath = '.\models\Qwen2.5-0.5B-Instruct-Q4_K_M.gguf'
$LicensePath = '.\licenses'

Write-Host 'Starting Japanese Tutor build...' -ForegroundColor Cyan

# Verify Python virtual environment exists
if (-not (Test-Path $PythonPath)) {
    throw 'Python environment not found. Create the .venv environment first.'
}

# Verify model exists
if (-not (Test-Path $ModelPath)) {
    throw 'Missing model. Run: .\.venv\Scripts\python.exe download_model.py'
}

# Verify license files exist
if (-not (Test-Path "$LicensePath\APACHE-2.0.txt")) {
    throw 'Missing APACHE-2.0.txt license file.'
}

if (-not (Test-Path "$LicensePath\MODEL-ATTRIBUTION.txt")) {
    throw 'Missing MODEL-ATTRIBUTION.txt file.'
}

# Install PyInstaller
Write-Host 'Installing PyInstaller...' -ForegroundColor Yellow

& $PythonPath -m pip install pyinstaller

if ($LASTEXITCODE -ne 0) {
    throw 'PyInstaller installation failed.'
}

# Build standalone Windows application
Write-Host 'Building Japanese Tutor...' -ForegroundColor Yellow

& $PythonPath -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onedir `
    --name JapaneseTutor `
    --collect-all llama_cpp `
    --add-data 'models\Qwen2.5-0.5B-Instruct-Q4_K_M.gguf;models' `
    --add-data 'licenses;licenses' `
    main.py

if ($LASTEXITCODE -ne 0) {
    throw "Build failed with exit code $LASTEXITCODE"
}

# Verify executable exists
if (-not (Test-Path '.\dist\JapaneseTutor\JapaneseTutor.exe')) {
    throw 'Build failed: JapaneseTutor.exe was not created.'
}

# Verify licenses were included
$BundledLicenses = '.\dist\JapaneseTutor\_internal\licenses'

if (-not (Test-Path "$BundledLicenses\APACHE-2.0.txt")) {
    throw 'Build failed: Apache license was not bundled.'
}

if (-not (Test-Path "$BundledLicenses\MODEL-ATTRIBUTION.txt")) {
    throw 'Build failed: Model attribution was not bundled.'
}

Write-Host ''
Write-Host 'BUILD SUCCESSFUL!' -ForegroundColor Green
Write-Host 'Executable: dist\JapaneseTutor\JapaneseTutor.exe'
Write-Host 'Model and license files included.'
Write-Host ''
Write-Host 'Next: Compile JapaneseTutor.iss using Inno Setup.'
