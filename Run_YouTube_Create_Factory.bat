@echo off
chcp 65001 >nul
title MD_SADIQUE_AMIN — YouTube Create 24H Factory
color 0D

echo.
echo  =====================================================
echo   MD_SADIQUE_AMIN YOUTUBE CREATE AUTONOMOUS FACTORY
echo   10 Videos / 24 Hours  ^|  2.4 Hour Gaps
echo   YouTube Create → All Accounts Auto-Post
echo  =====================================================
echo.
echo  [06:00] Slot 01  [08:24] Slot 02  [10:48] Slot 03
echo  [13:12] Slot 04  [15:36] Slot 05  [18:00] Slot 06
echo  [20:24] Slot 07  [22:48] Slot 08  [01:12] Slot 09
echo  [03:36] Slot 10
echo.
echo  Each Slot: Topic → YT Create Image → YT Create Video
echo             → Instagram + Facebook + Threads + YouTube Shorts
echo.

cd /d "d:\current using file\1 social media automation handler file"

echo  [?] Choose mode:
echo  [1] Run Full 24H Autonomous Factory
echo  [2] Preview Today's 10 Topics (no execution)
echo  [3] Test Single Slot Now (Slot 1)
echo.
set /p choice=  Enter 1, 2 or 3: 

if "%choice%"=="1" (
    echo  [*] Starting 24H Factory...
    python youtube_create_factory.py
)
if "%choice%"=="2" (
    echo  [*] Previewing Today's Topics...
    python youtube_create_factory.py --preview-topics
    pause
)
if "%choice%"=="3" (
    echo  [*] Testing Slot 1...
    python youtube_create_factory.py --test-slot 1
)
pause
