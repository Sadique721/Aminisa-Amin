#!/data/data/com.termux/files/usr/bin/bash
echo "=========================================================="
echo "📊 AMINSA STANDALONE MOBILE NODE STATUS"
echo "=========================================================="
echo "[*] Date: $(date)"

PID_UNIFIED=$(pgrep -f "aminsa_unified_service.py")
PID_WEB=$(pgrep -f "aminsa_web_daemon.py")

if [ -n "$PID_UNIFIED" ]; then
    echo "🟢 UNIFIED SERVICE: RUNNING (PID: $PID_UNIFIED)"
elif [ -n "$PID_WEB" ]; then
    echo "🟡 WEB DAEMON: RUNNING (PID: $PID_WEB)"
else
    echo "🔴 SERVICE STATUS: STOPPED"
fi

echo ""
echo "📱 ADB BRIDGE STATUS:"
/data/data/com.termux/files/usr/bin/adb devices 2>/dev/null

echo ""
echo "🌐 WEB PORT CHECK (8765):"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://127.0.0.1:8765/ 2>/dev/null || echo "Web server not responding on port 8765"

echo ""
echo "📝 RECENT LOG ENTRIES:"
if [ -f /sdcard/DCIM/Aminsa/aminsa_daemon.log ]; then
    tail -n 12 /sdcard/DCIM/Aminsa/aminsa_daemon.log
else
    echo "No log file found at /sdcard/DCIM/Aminsa/aminsa_daemon.log"
fi
echo "=========================================================="
