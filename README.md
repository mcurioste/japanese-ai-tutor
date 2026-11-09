# Japanese Tutor — Offline AI demo

A tiny Windows desktop Japanese-language tutor built with Python/Tkinter, `llama-cpp-python` and Qwen2.5-0.5B-Instruct GGUF. Each submitted question is independent: **no saved conversations or memory**. AI answers may be wrong; this is a packaging demo, not a validated learning curriculum.

## Run on your development PC (Windows x64)

1. Install Python **3.11 (64-bit)** and open PowerShell in this project folder.
2. Create a virtual environment: `py -3.11 -m venv .venv`
3. Install the inference library using the CPU prebuilt-wheel index (does not require activating the environment):
   ```powershell
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install --only-binary=:all: --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu "llama-cpp-python>=0.3,<0.4"
   ```
   If the Windows wheel isn't available for your Python version and architecture, consult the [llama-cpp-python installation docs](https://github.com/abetlen/llama-cpp-python#installation) for supported wheels/build tools. Avoid compiling from source for the first demo.
4. Download the model (approximately 398 MB):
   ```powershell
   .\.venv\Scripts\python.exe download_model.py
   ```
5. Run the tutor:
   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```

The model download script checks the SHA-256 listed on the Hugging Face model page as of November 2026. If upstream changes the file, update the URL and checksum before trusting it.

## Build a portable Windows application

On your Windows development PC, after completing the preceding steps:

```powershell
.\build_windows.ps1
```

The result is `dist\JapaneseTutor\JapaneseTutor.exe`. **Copy the entire `dist\JapaneseTutor` directory**, including its `_internal` folder, to the other Windows PC and run the EXE. The other computer should not need Python, internet access, or the model downloaded separately. This CPU build is intended for Windows x64, and should be tested on the target PC. Windows security software may warn about unsigned executables.

## Build a Windows installer

Install [Inno Setup](https://jrsoftware.org/isinfo.php) on the build PC. Open `JapaneseTutor.iss` in Inno Setup and click Compile. It produces `installer\JapaneseTutor-Setup-0.1.0.exe` containing the entire packaged app and model. Publish **that installer** using **GitHub Releases**, rather than committing the GGUF file or build artifacts into the normal Git repository. GitHub Releases have asset-size and account constraints; verify the current limits before publishing.

**Note:** Model redistribution is governed by its license (Qwen2.5-0.5B-Instruct is Apache 2.0); retain the license and attribution/notice files applicable to the redistributed model and software. This starter ZIP intentionally excludes the model binary and built installer. The final installer must be built on your Windows PC.

## Architecture

`main.py` → `llama-cpp-python` → `models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` → answer in Tkinter.

No cloud calls are made for inference. Only `download_model.py` makes a network request to retrieve the model during setup.
