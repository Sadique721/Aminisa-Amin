# -*- coding: utf-8 -*-
"""
Aminsa Unified CLI & Excel Launcher
Runs when user types 'aminsa' in terminal or double clicks aminsa.bat.
"""

import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.aminsa_catalog_engine import generate_master_excel, MOBILE_SLOTS

def main():
    print("=" * 75)
    print("           🌟 AMINSA MASTER PRODUCTION & SCRIPT CATALOG 🌟           ")
    print("=" * 75)
    print("[*] Generating & refreshing Master Excel Spreadsheet...")
    excel_path = generate_master_excel()

    print("\n[+] TOP 5 MOBILE YOUTUBE CREATE PRODUCTION SCRIPTS:")
    print("-" * 75)
    for s in MOBILE_SLOTS[:5]:
        print(f"  • [Slot {s['slot']} | {s['time']}] {s['title']}")
        print(f"    Category: {s['category']}")
        print(f"    Script  : {s['script']}")
        print(f"    Image   : {s['img_prompt'][:70]}...")
        print()

    print("=" * 75)
    print(f"[✓] Opening Excel Sheet: {excel_path}")
    print("=" * 75)

    if sys.platform == "win32":
        try:
            os.startfile(excel_path)
        except Exception:
            subprocess.run(["cmd", "/c", "start", "", excel_path], shell=True)
    elif sys.platform == "darwin":
        subprocess.run(["open", excel_path])
    else:
        # Linux / Android Termux
        if os.path.exists("/data/data/com.termux"):
            subprocess.run(["termux-open", excel_path])
        else:
            subprocess.run(["xdg-open", excel_path])

if __name__ == "__main__":
    main()
