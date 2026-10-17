#!/data/data/com.termux/files/usr/bin/bash
# -------------------------------------------------------------
# Aminsa Standalone Mobile Daemon Launcher
# -------------------------------------------------------------
export HOME=/data/data/com.termux/files/home
export PREFIX=/data/data/com.termux/files/usr
export PATH=/data/data/com.termux/files/usr/bin:$PATH
export TMPDIR=/data/data/com.termux/files/usr/tmp
export LD_PRELOAD=/data/data/com.termux/files/usr/lib/libtermux-exec.so

# Create required dirs (Termux-internal fallbacks if sdcard unavailable)
mkdir -p $TMPDIR 2>/dev/null
mkdir -p $HOME/aminsa_logs 2>/dev/null
mkdir -p $HOME/aminsa_audio 2>/dev/null
# Try to create sdcard dirs too (may silently fail in run-as context, OK)
mkdir -p /sdcard/DCIM/Aminsa/audio 2>/dev/null
mkdir -p /sdcard/DCIM/Aminsa/generated_media 2>/dev/null

# Log destination — prefer sdcard, fallback to home
if [ -w /sdcard/DCIM/Aminsa ]; then
    LOG_PATH=/sdcard/DCIM/Aminsa/aminsa_daemon.log
else
    LOG_PATH=$HOME/aminsa_logs/aminsa_daemon.log
fi

cd /data/data/com.termux/files/home/aminsa_mobile_ecosystem

# Ensure ADB is listening and connected
echo "[*] Connecting local ADB..."
adb connect 127.0.0.1:5555 >/dev/null 2>&1

# Acquire wake lock
termux-wake-lock 2>/dev/null
echo "[+] Termux wake-lock acquired."

# Check if already running
PID=$(pgrep -f "aminsa_daemon.py")
if [ -n "$PID" ]; then
    echo "[!] Aminsa daemon is already running (PID: $PID)"
    exit 0
fi

# Launch in background with nohup
nohup python3 /data/data/com.termux/files/home/aminsa_mobile_ecosystem/aminsa_daemon.py > $LOG_PATH 2>&1 &
NEW_PID=$!

echo "=========================================================="
echo "🌟 AMINSA STANDALONE MOBILE DAEMON STARTED"
echo "🌟 PID: $NEW_PID"
echo "🌟 Log: $LOG_PATH"
echo "=========================================================="

termux-notification --title "Aminsa AI Active" --content "24/7 Mobile Ecosystem running in background!" 2>/dev/null
