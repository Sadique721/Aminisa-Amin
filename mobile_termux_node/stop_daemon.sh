#!/data/data/com.termux/files/usr/bin/bash
# Stop Aminsa daemon
PID=$(pgrep -f "aminsa_daemon.py")
if [ -n "$PID" ]; then
    kill -9 $PID
    echo "[+] Aminsa daemon stopped (Killed PID: $PID)"
    termux-wake-unlock
    echo "[+] Termux wake-lock released."
else
    echo "[-] No running Aminsa daemon found."
fi
