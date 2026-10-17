# -*- coding: utf-8 -*-
"""
Aminsa Mobile Orchestrator (OPPO A78 5G)
Runs on Termux when typing 'aminsa-orchestrator'
"""
import os
import sys
import json
import time
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
    print("=" * 65)
    print("  🚀 AMINSA MOBILE ORCHESTRATOR (OPPO A78 5G NODE)")
    print("=" * 65)
    now = datetime.now()
    print(f"[*] Cycle Started at {now.strftime('%Y-%m-%d %I:%M %p')}")
    
    slot_idx = (now.hour // 2) % len(MOBILE_SLOTS)
    active_slot = MOBILE_SLOTS[slot_idx]
    
    print(f"\n[+] ACTIVE SLOT: #{active_slot['slot']} ({active_slot['time']})")
    print(f"  📌 CATEGORY : {active_slot['category']}")
    print(f"  🎯 HEADLINE : {active_slot['title']}")
    print(f"  🗣️ SCRIPT   : {active_slot['script']}")
    print(f"  🎨 IMAGE    : {active_slot['img_prompt'][:75]}...")
    print(f"  🎬 YT MOTION: {active_slot['video_prompt']}")
    
    print("\n[*] Refreshing Mobile Excel Catalog...")
    save_catalog_safely()
        
    print("=" * 65)
    print("✅ MOBILE ORCHESTRATION CYCLE READY FOR YOUTUBE CREATE!")
    print("=" * 65)

if __name__ == "__main__":
    main()
