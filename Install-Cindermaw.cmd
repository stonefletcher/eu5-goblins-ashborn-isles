@echo off
title Install Cindermaw 0.2.0
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Cindermaw.ps1"
if errorlevel 1 (
  echo Installation stopped. See the error above.
  pause
  exit /b 1
)
echo Installation complete. Restart EU5 and start a NEW 1337 campaign with only Cindermaw enabled.
pause
