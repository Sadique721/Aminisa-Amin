@echo off
TITLE Aminsa Laptop Long-Form Cinematic Studio
COLOR 0B
cd /d "%~dp0"

echo ======================================================================
echo          AMINSA LAPTOP LONG-FORM CINEMATIC STUDIO (10M / 1H)
echo ======================================================================
echo [*] Device: Laptop Master Studio Node
echo [*] Scope: 10-Minute Concept Films & Tech Stories / 1-Hour Epics
echo [*] Resolution: 1920x1080 60FPS High-Definition Audio-Visual Master
echo [*] Audio: 224 Hz Studio Mastered hi-IN-SwaraNeural
echo [*] Telemetry: Aminsa_Master_Production_Catalog.xlsx
echo ======================================================================
echo.
python master_orchestrator.py
echo.
echo ======================================================================
echo [✓] Long-Form Production Finished. Press any key to exit.
echo ======================================================================
pause
