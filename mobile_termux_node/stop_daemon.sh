#!/data/data/com.termux/files/usr/bin/bash
# Stop Aminsa Unified Service
pkill -9 -f "aminsa_unified_service.py" 2>/dev/null
pkill -9 -f "aminsa_daemon.py" 2>/dev/null
pkill -9 -f "aminsa_web_daemon.py" 2>/dev/null
termux-wake-unlock 2>/dev/null
echo "[+] Aminsa services stopped & Termux wake-lock released."
