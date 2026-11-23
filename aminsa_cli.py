# -*- coding: utf-8 -*-
"""
Aminsa Unified Cross-Device CLI & Production Hub Launcher
=========================================================
Runs automatically when user types 'aminsa' in cmd.exe / terminal or double-clicks aminsa.bat.
1. Generates fresh Master Excel Spreadsheet & ChatGPT-Style Dark UI
2. Automatically ensures Web Daemon on port 8765 is running (laptop daemon + ADB bridge)
3. Displays all 10 real-time dynamic daily slots in console
4. Automatically opens Aminsa ChatGPT-styled Dashboard in browser (http://127.0.0.1:8765/)
5. Automatically opens Master Excel Spreadsheet
"""

import os
import sys
import time
import socket
import webbrowser
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
MOBILE_NODE_DIR = os.path.join(PROJECT_ROOT, "mobile_termux_node")
if MOBILE_NODE_DIR not in sys.path:
    sys.path.insert(0, MOBILE_NODE_DIR)

from engines.aminsa_catalog_engine import generate_master_excel, get_current_day_data

PORT = 8765


def is_port_listening(port=PORT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False


def ensure_web_daemon_running():
    """Ensures port 8765 is actively serving (via ADB bridge or native laptop daemon)."""
    if is_port_listening(PORT):
        return True

    # 1. Try ADB bridge forward if phone is attached
    try:
        adb_paths = [
            "adb",
            r"C:\platform-tools\adb.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
        ]
        for adb in adb_paths:
            try:
                res = subprocess.run([adb, "forward", f"tcp:{PORT}", f"tcp:{PORT}"], capture_output=True, timeout=2)
                if res.returncode == 0 and is_port_listening(PORT):
                    return True
            except Exception:
                continue
    except Exception:
        pass

    # 2. Launch native background Web Daemon on laptop
    daemon_script = os.path.join(MOBILE_NODE_DIR, "aminsa_web_daemon.py")
    if os.path.exists(daemon_script):
        try:
            flags = 0
            if sys.platform == "win32":
                flags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            subprocess.Popen(
                [sys.executable, daemon_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=flags
            )
            # Give daemon up to 3 seconds to bind
            for _ in range(6):
                time.sleep(0.5)
                if is_port_listening(PORT):
                    return True
        except Exception as e:
            print(f"[-] Could not spawn background daemon: {e}")

    return is_port_listening(PORT)


def main():
    print("=" * 75)
    print("           🌟 AMINSA MASTER PRODUCTION & SCRIPT CATALOG 🌟           ")
    print("=" * 75)
    print("[*] Harvesting live real-time topics & building Video Prompts...")

    now = datetime.now()
    excel_path = os.path.join(PROJECT_ROOT, "Aminsa_Master_Production_Catalog.xlsx")
    generate_master_excel(excel_path)
    date_str, slots, _ = get_current_day_data(now)

    # Ensure Web Daemon on port 8765
    daemon_online = ensure_web_daemon_running()

    print("\n" + "=" * 75)
    print(f"  📱 10 DAILY REAL-TIME PRODUCTION SLOTS ({date_str})")
    print("=" * 75)

    for s in slots:
        slot_num = s["slot"]
        slot_time = s["time"]
        cat = s["category"]
        lang = s.get("language", "hinglish").upper()
        title = s["title"]
        script = s.get("script", "")
        v_prompt = s.get("video_prompt", "")

        print(f"\n▶ [SLOT {slot_num} | {slot_time}] {cat.upper()} [{lang}]")
        print(f"  📌 TOPIC   : {title}")
        print(f"  🗣️ SCRIPT  : {script[:110]}...")
        if v_prompt:
            print(f"  🎬 VIDEO   : \"{v_prompt[:95]}...\"")
        print("-" * 75)

    # Open Master Excel Sheet
    print("\n" + "=" * 75)
    print(f"[✓] Opening Excel Sheet: {excel_path}")
    if sys.platform == "win32":
        try:
            os.startfile(excel_path)
        except Exception:
            subprocess.run(["cmd", "/c", "start", "", excel_path], shell=True)
    elif sys.platform == "darwin":
        subprocess.run(["open", excel_path])
    else:
        if os.path.exists("/data/data/com.termux"):
            subprocess.run(["termux-open", excel_path])
        else:
            subprocess.run(["xdg-open", excel_path])

    # Open Web Browser to Port 8765
    url = f"http://127.0.0.1:{PORT}/"
    print(f"[✓] Opening ChatGPT-Styled Dashboard in Browser: {url}")
    print("=" * 75)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    if daemon_online:
        print(f"🟢 [ONLINE] Dashboard running at {url}")
    else:
        print(f"🟡 [NOTICE] Web daemon binding in progress. Visit {url} in browser.")
    print("✅ All systems ready. Exiting cleanly.\n")


if __name__ == "__main__":
    main()
