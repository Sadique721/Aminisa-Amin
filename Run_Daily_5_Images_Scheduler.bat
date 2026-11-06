@echo off
TITLE Aminsa Daily 5-Image Autonomous Production
cd /d "D:\current using file\Mine\1 social media automation handler file"
"C:\Python314\python.exe" "engines\daily_5_images_scheduler.py" --run-now >> "logs\daily_5_images_scheduler.log" 2>&1
