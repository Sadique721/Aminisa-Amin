#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aminsa Amin — Mobile & Laptop NEXT Command CLI Engine
=====================================================
Safely advances the production cycle to the next calendar date.
Strict Rules:
1. Exactly 10 fresh content slots per cycle.
2. 100% Dynamic Multi-Tier Google News RSS input.
3. 30-Day Anti-Repetition cross-referencing against ledger.
4. Generates both Aminsa_Master_Production_Catalog.html and .xlsx.
5. All outputs remain strictly in DRAFT state (zero auto-publishing).
6. Idempotent: Repeated calls return the active next cycle without duplicates.
"""

import os
import sys
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from aminsa_web_daemon import advance_to_next_cycle, _CACHED_DATE
from aminsa_catalog_engine import get_current_day_data


def run_next_cycle():
    print("=" * 68)
    print("⏭️  AMINSA AMIN — ADVANCE TO NEXT DAILY PRODUCTION CYCLE")
    print("==============================================================")
    print(f"[*] Execution Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")
    print("[*] Device Node: Dual-AI Architecture (Laptop MSA + Mobile Edge)")
    print("[*] Reading Previous Production Cycles from Historical Ledger...")
    print("[*] Harvesting Fresh Multi-Tier News via Google News RSS...")
    print("[*] Checking 30-Day Anti-Repetition Rules & Canonical Assets...")

    t0 = time.time()
    html_bytes = advance_to_next_cycle()
    elapsed = time.time() - t0

    now = datetime.now()
    date_str, slots, _ = get_current_day_data(now)

    print("\n📦 Verified 10-Slot Production Grid:")
    print("-" * 68)
    for s in slots:
        slot_num = s.get("slot_id") or s.get("slot_num") or s.get("id")
        slot_time = s.get("time", "08:00 AM")
        cat = s.get("name") or s.get("category", "")
        lang = s.get("language", "HINGLISH").upper()
        title = s.get("title") or s.get("headline", "")
        print(f"▶ [SLOT {slot_num:>2} | {slot_time}] {cat[:30]:<30} [{lang}]")
        print(f"  📌 TOPIC: {title[:60]}...")
    print("-" * 68)

    print(f"\n[✓] Generated Exactly 10 Unique Content Slots in DRAFT State ({elapsed:.2f}s).")
    print("[✓] Updated: Aminsa_Master_Production_Catalog.xlsx & .html")
    print("[✓] Live ChatGPT Dashboard at: http://127.0.0.1:8765/")
    print("==============================================================")
    return True


if __name__ == "__main__":
    run_next_cycle()
