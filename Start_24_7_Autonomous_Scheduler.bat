@echo off
TITLE Aminsa 24/7 Autonomous Long-Form Broadcast Factory
COLOR 0A
cd /d "%~dp0"

echo ======================================================================
echo      AMINSA 24/7 AUTONOMOUS LONG-FORM BROADCAST FACTORY (LAPTOP)
echo ======================================================================
echo [*] Schedule: 10 Long-Form Productions Daily (5 x 10m Films + 5 x 1h Epics)
echo [*] Output: 1920x1080 60FPS MP4 Videos in exports/films_10min/ & exports/epics_1hr/
echo [*] Ledger: Aminsa_Master_Production_Catalog.xlsx (Laptop_Long_Form_Studio Tab)
echo [*] Interval: Every 2.4 Hours (8640s) Autonomous Production Cycle
echo ======================================================================
echo.

:LOOP
echo [%DATE% %TIME%] Starting Aminsa Long-Form Studio Factory...
python Run_Unified_Autonomous_24_7_Factory.py --interval 8640
echo [%DATE% %TIME%] Studio stopped or crashed. Restarting in 10 seconds...
timeout /t 10 /nobreak >nul
goto LOOP
