#!/data/data/com.termux/files/usr/bin/bash
echo "=========================================================="
echo "📊 AMINSA STANDALONE MOBILE NODE STATUS"
echo "=========================================================="
echo "[*] Date: $(date)"
PID=$(pgrep -f "aminsa_daemon.py")
if [ -n "$PID" ]; then
    echo "🟢 DAEMON STATUS: RUNNING (PID: $PID)"
else
    echo "🔴 DAEMON STATUS: STOPPED"
fi

echo ""
echo "📱 ADB BRIDGE STATUS:"
/data/data/com.termux/files/usr/bin/adb devices 2>/dev/null

echo ""
echo "📝 RECENT LOG ENTRIES:"
if [ -f /sdcard/DCIM/Aminsa/aminsa_daemon.log ]; then
    tail -n 15 /sdcard/DCIM/Aminsa/aminsa_daemon.log
else
    echo "No log file found at /sdcard/DCIM/Aminsa/aminsa_daemon.log"
fi
echo "=========================================================="
