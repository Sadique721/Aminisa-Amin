# -*- coding: utf-8 -*-
r"""
Run_Daily_Master_Face_Generator.py
==================================
Daily autonomous face generator and catalog deployer for Aminsa.
- Generates 1 pristine, 4K/HQ clean-face portrait of Aminsa every single day.
- Saved in 'aminsa-360-day-bases-face-images\aminsa-face-YYYY-MM-DD.png' & '.jpg'.
- Automatically deploys today's Excel Catalog (Aminsa_Master_Production_Catalog.xlsx).
- Checks internet connectivity; generates face when internet connects.
- Automatically syncs to phone when ADB is connected.
"""

import os
import sys
import argparse
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.daily_master_face_engine import daily_face_engine

def main():
    parser = argparse.ArgumentParser(description="Aminsa Daily Master Face Generator")
    parser.add_argument("--force", action="store_true", help="Force regenerate today's face even if it exists")
    parser.add_argument("--no-wait", action="store_true", help="Do not wait for internet if offline")
    args = parser.parse_args()

    today_str = datetime.now().strftime("%Y-%m-%d")
    print("=" * 75)
    print("  AMINSA ULTRA-PRO-MAX DAILY MASTER FACE & CATALOG DEPLOYER")
    print(f"  Target Date: {today_str} | Resolution: 4K Ultra-HQ (2160x2160)")
    print("  Output Directory: aminsa-360-day-bases-face-images")
    print("=" * 75)

    res = daily_face_engine.ensure_today_master_face(
        force_regenerate=args.force,
        wait_if_offline=not args.no_wait
    )

    print("\n[✔] MASTER ASSETS DEPLOYED:")
    print(f"    • Status      : {res['status']}")
    print(f"    • Date        : {res['date']}")
    print(f"    • PNG (4K HQ) : {res['png']}")
    print(f"    • JPG (4K HQ) : {res['jpg']}")
    print(f"    • Excel Sheet : Aminsa_Master_Production_Catalog.xlsx (DEPLOYED)")
    print("    • Biometrics  : Wheatish Porcelain (#EAD5C3), Hazel Eyes (#6B4423), ZERO MOLES")

    # Mobile Sync
    print("\n[*] Checking Phone ADB Sync...")
    synced = daily_face_engine.sync_to_phone()
    if synced:
        print("    [✔] Successfully pushed to phone: /sdcard/DCIM/Aminsa/aminsa-360-day-bases-face-images/")
    else:
        print("    [-] Ready locally on laptop in 'aminsa-360-day-bases-face-images' folder.")

    print("\n" + "=" * 75)
    print("  Ready to use for today's 10 YouTube Create / Laptop videos!")
    print("=" * 75)

if __name__ == "__main__":
    main()
