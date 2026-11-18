#!/data/data/com.termux/files/usr/bin/bash
# -------------------------------------------------------------
# Aminsa Standalone Unified Mobile Service Launcher
# -------------------------------------------------------------
export HOME=/data/data/com.termux/files/home
export PREFIX=/data/data/com.termux/files/usr
export PATH=/data/data/com.termux/files/usr/bin:$PATH
export TMPDIR=/data/data/com.termux/files/usr/tmp
export LD_PRELOAD=/data/data/com.termux/files/usr/lib/libtermux-exec.so

mkdir -p $TMPDIR 2>/dev/null
mkdir -p $HOME/aminsa_logs 2>/dev/null
mkdir -p $HOME/aminsa_audio 2>/dev/null
mkdir -p /sdcard/DCIM/Aminsa/audio 2>/dev/null
mkdir -p /sdcard/DCIM/Aminsa/generated_media 2>/dev/null

if [ -w /sdcard/DCIM/Aminsa ]; then
    LOG_PATH=/sdcard/DCIM/Aminsa/aminsa_daemon.log
else
    LOG_PATH=$HOME/aminsa_logs/aminsa_daemon.log
fi

cd /data/data/com.termux/files/home/aminsa_mobile_ecosystem

# Ensure local ADB bridge
echo "[*] Connecting local ADB..."
adb connect 127.0.0.1:5555 >/dev/null 2>&1

# Acquire wake lock
termux-wake-lock 2>/dev/null
echo "[+] Termux wake-lock acquired."

# Kill any conflicting old standalone daemons
pkill -f "aminsa_daemon.py" 2>/dev/null
pkill -f "aminsa_web_daemon.py" 2>/dev/null

# Check if unified service is already running
PID=$(pgrep -f "aminsa_unified_service.py")
if [ -n "$PID" ]; then
    echo "[!] Aminsa Unified Service already running (PID: $PID)"
    exit 0
fi

# Launch unified service (Production scheduler + Dynamic Web Hub)
nohup python3 /data/data/com.termux/files/home/aminsa_mobile_ecosystem/aminsa_unified_service.py > $LOG_PATH 2>&1 &
NEW_PID=$!

echo "=========================================================="
echo "🌟 AMINSA UNIFIED 24/7 MOBILE SERVICE STARTED"
echo "🌟 PID: $NEW_PID"
echo "🌟 Web Dashboard: http://127.0.0.1:8765/"
echo "🌟 Log: $LOG_PATH"
echo "=========================================================="

termux-notification --title "Aminsa Unified Active" --content "24/7 Production + Web Hub running at port 8765" 2>/dev/null
