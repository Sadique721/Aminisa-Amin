# -*- coding: utf-8 -*-
"""
Aminsa Mobile 24/7 Autonomous Scheduler (OPPO A78 5G)
Runs continuous 2.4-hour content generation loop inside Termux.
"""
import os
import sys
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from aminsa_catalog_engine import generate_master_excel, MOBILE_SLOTS

INTERVAL = 8640 # 2.4 hours in seconds

def cycle():
    now = datetime.now()
    slot_idx = (now.hour // 2) % len(MOBILE_SLOTS)
    s = MOBILE_SLOTS[slot_idx]
    print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] [AMINSA 24/7 MOBILE SCHEDULER] Slot #{s['slot']}: {s['title']}")
    try:
        generate_master_excel("/sdcard/Documents/Aminsa_Master_Production_Catalog.xlsx")
        print("[✓] Updated /sdcard/Documents/Aminsa_Master_Production_Catalog.xlsx")
    except Exception as e:
        print(f"[-] Scheduler cycle error: {e}")

def main():
    print("=" * 65)
    print("  ⏰ AMINSA 24/7 MOBILE AUTONOMOUS SCHEDULER (OPPO A78 5G)")
    print("=" * 65)
    print(f"[*] Loop Interval: {INTERVAL}s (10 slots/day every 2.4 hours)")
    print("[*] Ensuring Termux wake lock...")
    os.system("termux-wake-lock 2>/dev/null")
    
    while True:
        cycle()
        print(f"[*] Sleeping {INTERVAL}s until next production slot...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
