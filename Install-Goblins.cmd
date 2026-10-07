@echo off
setlocal
title Install Goblins of the Ashborn Isles
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Goblins.ps1"
if errorlevel 1 (
 echo Installation stopped. See the error above.
 pause
 exit /b 1
)
echo Ready. Restart EU5 and start a NEW 1337 campaign with Goblins of the Ashborn Isles.
pause
