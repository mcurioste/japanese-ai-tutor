$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Test-Path '.\models\Qwen2.5-0.5B-Instruct-Q4_K_M.gguf')) {
    throw 'Missing model. Run: .\.venv\Scripts\python.exe download_model.py'
}
.\.venv\Scripts\python.exe -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller installation failed' }
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onedir --name JapaneseTutor --collect-all llama_cpp --add-data 'models\Qwen2.5-0.5B-Instruct-Q4_K_M.gguf;models' --add-data 'licenses;licenses' main.pyif ($LASTEXITCODE -ne 0) { throw 'Build failed' }
Write-Host 'Built dist\JapaneseTutor\JapaneseTutor.exe'
Write-Host 'Copy the WHOLE dist\JapaneseTutor folder to the other Windows PC, or run the Inno Setup script to make an installer.'
