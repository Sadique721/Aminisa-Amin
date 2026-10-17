@echo off
TITLE Push Aminsa Repository to GitHub
COLOR 0A
cd /d "%~dp0"

echo ======================================================================
echo             PUSHING AMINSA REPOSITORY TO GITHUB
echo ======================================================================
echo [*] Target: https://github.com/Sadique721/Aminisa-Amin.git
echo [*] Branch: main
echo.
echo [*] Launching Git Push... If prompted, select "Sign in with your browser".
echo.
git push -u origin main
echo.
echo ======================================================================
if %ERRORLEVEL% EQU 0 (
    echo [OK] Push completed successfully to GitHub!
) else (
    echo [!] Push encountered an error or was cancelled.
)
echo ======================================================================
pause
