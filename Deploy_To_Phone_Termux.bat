@echo off
TITLE Deploy Aminsa YouTube Create Engine to Phone Termux
COLOR 0B
cd /d "%~dp0"

echo ======================================================================
echo    DEPLOY AMINSA INDEPENDENT YOUTUBE CREATE ENGINE TO TERMUX
echo ======================================================================
echo [*] Target: OPPO A78 5G (Android 15 / Termux Node)
echo [*] Destination: /data/data/com.termux/files/home/aminsa_mobile_ecosystem/
echo ======================================================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0deploy_to_phone.ps1"

echo.
echo ======================================================================
pause
