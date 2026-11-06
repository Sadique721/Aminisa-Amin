@echo off
TITLE Aminsa Amin Daily 5-Image Autonomous Scheduler
COLOR 0D
cd /d "%~dp0"

echo ======================================================================
echo    🌸 AMINSA AMIN DAILY 5-IMAGE AUTONOMOUS SCHEDULER
echo ======================================================================
echo [*] Mode: 5 Unique Multi-Shot Images / Day (Square 4K + 9:16 Vertical)
echo [*] Shot Types: Full-Body Standing, Dynamic Selfies, 3/4 Editorial, Cultural
echo [*] Biometric Lock: Identical Face Anchor (#EAD5C3, Hazel Eyes #6B4423)
echo [*] Dynamic Wardrobe: 100%% Unique Modern Outfits (365 Days Procedural)
echo [*] Festivals & Places: Real-Time Calendar Integration
echo [*] Destination: daily_generated_images\YYYY-MM-DD\
echo ======================================================================
echo.

python engines\daily_5_images_scheduler.py --run-now

echo.
echo ======================================================================
echo [✔] Execution complete. To run as continuous 24/7 background daemon:
echo     python engines\daily_5_images_scheduler.py --daemon
echo ======================================================================
pause
