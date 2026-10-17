#!/data/data/com.termux/files/usr/bin/bash
# Aminsa Mobile 24/7 Autonomous YouTube Create Scheduler
# Runs inside Termux on OnePlus phone with zero laptop connection needed

termux-wake-lock
echo "=========================================================="
echo "    AMINSA MOBILE 24/7 YOUTUBE CREATE ENGINE (TERMUX)    "
echo "=========================================================="
echo "[*] Autonomous Mobile Node initialized."
echo "[*] Destination: /sdcard/Movies/Aminsa_YT_Create/"
echo "=========================================================="

while true; do
    echo "[$(date)] Running Aminsa YouTube Create Generation..."
    python mobile_yt_create_engine.py
    echo "[$(date)] Cycle complete. Sleeping for 8640s (2.4 hours)..."
    sleep 8640
done
