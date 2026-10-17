#!/data/data/com.termux/files/usr/bin/bash
echo "==================================================" > /sdcard/DCIM/Aminsa/termux_verification.log
echo "📱 AMINSA MOBILE NODE HEALTH VERIFICATION (OPPO A78 5G)" >> /sdcard/DCIM/Aminsa/termux_verification.log
echo "==================================================" >> /sdcard/DCIM/Aminsa/termux_verification.log
echo "[*] Date: $(date)" >> /sdcard/DCIM/Aminsa/termux_verification.log
echo "[*] Python: $(python3 --version 2>&1)" >> /sdcard/DCIM/Aminsa/termux_verification.log

# Ensure edge-tts is installed
python3 -c "import edge_tts" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[*] Installing edge-tts in Termux..." >> /sdcard/DCIM/Aminsa/termux_verification.log
    pip install edge-tts requests >> /sdcard/DCIM/Aminsa/termux_verification.log 2>&1
fi

echo "[*] Testing edge-tts import..." >> /sdcard/DCIM/Aminsa/termux_verification.log
python3 -c "import edge_tts; print('EDGE_TTS_READY')" >> /sdcard/DCIM/Aminsa/termux_verification.log 2>&1

echo "[*] Executing 1 Aminsa mobile cycle..." >> /sdcard/DCIM/Aminsa/termux_verification.log
cd /sdcard/DCIM/Aminsa/
python3 /sdcard/DCIM/Aminsa/termux_autonomous_agent.py --once >> /sdcard/DCIM/Aminsa/termux_verification.log 2>&1

echo "==================================================" >> /sdcard/DCIM/Aminsa/termux_verification.log
echo "✅ MOBILE NODE VERIFICATION COMPLETE" >> /sdcard/DCIM/Aminsa/termux_verification.log
echo "==================================================" >> /sdcard/DCIM/Aminsa/termux_verification.log
