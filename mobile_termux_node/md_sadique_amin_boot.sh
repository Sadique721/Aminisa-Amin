#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================
# AMINSA AUTO-BOOT SCRIPT (Termux:Boot)
# Runs automatically when mobile boots/restarts.
# ==============================================================

# Wait for system services to settle
sleep 15

# Connect local ADB
/data/data/com.termux/files/usr/bin/adb connect 127.0.0.1:5555 >/dev/null 2>&1

# Start Aminsa 24/7 Daemon
bash /data/data/com.termux/files/home/aminsa_mobile_ecosystem/start_daemon.sh
