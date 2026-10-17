#!/data/data/com.termux/files/usr/bin/bash
# -------------------------------------------------------------
# Aminsa Mobile Node One-Click Installer for Termux (Android 15)
# -------------------------------------------------------------
echo "=========================================================="
echo "  Setting up Aminsa Autonomous AI Agent on OPPO A78 5G"
echo "=========================================================="

pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg git termux-api

pip install --upgrade pip
pip install edge-tts requests openpyxl

termux-wake-lock
echo "[+] Aminsa Mobile Environment configured successfully!"
echo "[*] To start the 24/7 background agent, run: python termux_autonomous_agent.py"
