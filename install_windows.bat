@echo off
REM One-click installer for the blocky video workflow (Windows 10/11). Installs only what is missing.
REM Needs winget (included with Windows 11 and updated Windows 10). Right-click > Run as administrator if a step asks.
echo === Blocky workflow installer ===
where winget >nul 2>nul || (echo winget not found. Install "App Installer" from the Microsoft Store, then run this again. & pause & exit /b 1)

where node >nul 2>nul && (echo Node.js already installed) || (echo Installing Node.js LTS... & winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements)
where ffmpeg >nul 2>nul && (echo ffmpeg already installed) || (echo Installing ffmpeg... & winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements)
where python >nul 2>nul && (echo Python already installed) || (echo Installing Python... & winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (echo Chrome already installed) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (echo Chrome already installed) else (echo Installing Chrome... & winget install -e --id Google.Chrome --accept-package-agreements --accept-source-agreements)

echo Installing numpy...
python -m pip install numpy
echo.
echo Done. CLOSE this window, open a NEW terminal, then run:
echo   python setup_check.py
pause
