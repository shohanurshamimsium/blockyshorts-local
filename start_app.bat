@echo off
cd /d "%~dp0"
title Blocky Video Maker
echo Starting Blocky Video Maker... (keep this window open; close it to stop)
python app.py
if errorlevel 1 (
  echo.
  echo Python failed to start the app. Try:  py app.py
  py app.py
)
pause
