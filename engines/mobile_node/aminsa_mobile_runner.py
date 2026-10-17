# -*- coding: utf-8 -*-
"""
Aminsa Mobile Interactive Runner & Excel Launcher (OPPO A78 5G)
Runs when user types 'aminsa' in Termux.
"""

import os
import sys
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from aminsa_catalog_engine import generate_master_excel, MOBILE_SLOTS

def save_catalog_safely():
    candidate_paths = [
        "/data/user/0/com.termux/storage/shared/Documents/Aminsa_Master_Production_Catalog.xlsx",
        os.path.expanduser("~/storage/shared/Documents/Aminsa_Master_Production_Catalog.xlsx"),
        "/sdcard/Documents/Aminsa_Master_Production_Catalog.xlsx",
        os.path.expanduser("~/Aminsa_Master_Production_Catalog.xlsx")
    ]
    for p in candidate_paths:
        try:
            d = os.path.dirname(p)
            if d and not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
            generate_master_excel(p)
            print(f"[✓] Excel Catalog successfully saved at:\n    {p}")
            return p
        except Exception:
            continue
    return None

def main():
    print("=" * 70)
    print("    🌟 AMINSA MOBILE YOUTUBE CREATE HUB (OPPO A78 5G) 🌟")
    print("=" * 70)
    print("[*] Generating updated Master Production Excel Catalog...")
    
    excel_file = save_catalog_safely()
    
    print("\n" + "=" * 70)
    print("  📱 10 DAILY DESI AI COMEDY & HUMOR SLOTS (YOUTUBE CREATE READY)")
    print("=" * 70)
    
    for slot in MOBILE_SLOTS:
        print(f"\n▶ [SLOT {slot['slot']} | {slot['time']}] {slot['category'].upper()}")
        print(f"  📌 TOPIC   : {slot['title']}")
        print(f"  🗣️ SCRIPT  : {slot['script']}")
        print(f"  🎨 IMAGE PROMPT (<900 chars):")
        print(f"     \"{slot['img_prompt']}\"")
        print(f"  🎬 VIDEO PROMPT:")
        print(f"     \"{slot['video_prompt']}\"")
        print(f"  📢 FB/IG POST:")
        print(f"     \"{slot['fb_description'][:100]}...\"")
        print("-" * 70)

    print("\n[*] Opening Excel file on your phone screen...")
    opened = False
    
    if excel_file:
        try:
            res = subprocess.run(["termux-open", excel_file], capture_output=True)
            if res.returncode == 0:
                opened = True
                print(f"[✓] Opened {os.path.basename(excel_file)} in Office/Excel app!")
        except Exception:
            pass
            
        if not opened:
            try:
                cmd = ["am", "start", "-a", "android.intent.action.VIEW",
                       "-d", f"file://{excel_file}",
                       "-t", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
                subprocess.run(cmd, capture_output=True)
                print(f"[✓] Sent Android launch intent for {os.path.basename(excel_file)}")
            except Exception:
                pass

    print("=" * 70)
    print("✅ COPY ANY PROMPT ABOVE & PASTE INTO YOUTUBE CREATE APP!")
    print("=" * 70)

if __name__ == "__main__":
    main()
