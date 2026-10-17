#!/data/data/com.termux/files/usr/bin/bash
# Aminsa Aliases + Shortcut Setup — add to .bashrc
cat >> /data/data/com.termux/files/home/.bashrc << 'AMINSA_ALIASES'

# ===================== AMINSA ECOSYSTEM SHORTCUTS =====================
alias aminsa-start='bash /data/data/com.termux/files/home/aminsa_mobile_ecosystem/start_daemon.sh'
alias aminsa-stop='bash /data/data/com.termux/files/home/aminsa_mobile_ecosystem/stop_daemon.sh'
alias aminsa-status='bash /data/data/com.termux/files/home/aminsa_mobile_ecosystem/status.sh'
alias aminsa-test='python3 /data/data/com.termux/files/home/aminsa_mobile_ecosystem/test_suite.py'
alias aminsa-log='tail -f /sdcard/DCIM/Aminsa/aminsa_daemon.log'
alias cd-aminsa='cd /data/data/com.termux/files/home/aminsa_mobile_ecosystem'
# ======================================================================
AMINSA_ALIASES

echo "[OK] Aminsa shortcuts added to .bashrc"
grep -c "aminsa-start" /data/data/com.termux/files/home/.bashrc && echo "[OK] Verified in .bashrc"
