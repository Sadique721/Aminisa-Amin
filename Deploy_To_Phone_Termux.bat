@echo off
TITLE Deploy Aminsa YouTube Create Engine to Phone Termux
COLOR 0B
cd /d "%~dp0"

echo ======================================================================
echo    DEPLOY AMINSA INDEPENDENT YOUTUBE CREATE ENGINE TO TERMUX
echo ======================================================================
echo [*] Target: OnePlus Nord CE 3 Lite 5G (Termux Node)
echo [*] Destination: /data/data/com.termux/files/home/aminsa_mobile_ecosystem/
echo ======================================================================
echo.

set ADB="C:\platform-tools\adb.exe"

echo [*] Checking connected ADB devices...
%ADB% devices

echo.
echo [*] Pushing mobile engines to Termux storage...
%ADB% push engines\mobile_node\mobile_yt_create_engine.py /sdcard/mobile_yt_create_engine.py
%ADB% push engines\mobile_node\mobile_youtube_create_scheduler.sh /sdcard/mobile_youtube_create_scheduler.sh

echo [*] Moving files into Termux private ecosystem home...
%ADB% shell "run-as com.termux cp /sdcard/mobile_yt_create_engine.py /data/data/com.termux/files/home/aminsa_mobile_ecosystem/"
%ADB% shell "run-as com.termux cp /sdcard/mobile_youtube_create_scheduler.sh /data/data/com.termux/files/home/aminsa_mobile_ecosystem/"
%ADB% shell "run-as com.termux chmod +x /data/data/com.termux/files/home/aminsa_mobile_ecosystem/mobile_youtube_create_scheduler.sh"

echo [*] Cleaning up temporary sdcard files...
%ADB% shell "rm -f /sdcard/mobile_yt_create_engine.py /sdcard/mobile_youtube_create_scheduler.sh"

echo.
echo ======================================================================
echo [✓] SUCCESS: Mobile Autonomous Node is 100% Deployed in Termux!
echo.
echo [*] HOW TO RUN INDEPENDENTLY ON YOUR PHONE:
echo     1. Open Termux on your OnePlus phone.
echo     2. Run: cd ~/aminsa_mobile_ecosystem
echo     3. Run: ./mobile_youtube_create_scheduler.sh
echo.
echo [*] It will generate YouTube Create videos 24/7 directly into:
echo     /sdcard/Movies/Aminsa_YT_Create/
echo ======================================================================
pause
