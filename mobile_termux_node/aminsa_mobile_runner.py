# -*- coding: utf-8 -*-
"""
Aminsa Mobile Production Hub
============================
Runs automatically or when user types 'aminsa' in Termux on phone.
1. Generates updated Real-Time Master Excel (.xlsx) & ChatGPT-style HTML (.html)
2. Automatically launches Excel spreadsheet in LibreOffice Viewer
3. Auto-copies current active slot script & VIDEO prompt to phone clipboard
4. Prints daily 10 live real-time slots summary (Video Prompts ONLY)
5. Displays direct 1-tap [🌐DASH] button guidance & URL (http://127.0.0.1:8765/)
"""

import os
import sys
import shutil
import socket
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Ensure termux bin is in PATH
os.environ["PATH"] = "/data/data/com.termux/files/usr/bin:" + os.environ.get("PATH", "")

from aminsa_catalog_engine import (
    generate_master_excel,
    get_current_day_data
)

try:
    from build_chatgpt_style_html import build_chatgpt_html
except ImportError:
    build_chatgpt_html = None

WEB_PORT = 8765


def is_web_daemon_running():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", WEB_PORT)) == 0


def ensure_web_daemon():
    if is_web_daemon_running():
        return True
    daemon_script = os.path.join(SCRIPT_DIR, "aminsa_web_daemon.py")
    if not os.path.exists(daemon_script):
        daemon_script = os.path.expanduser("~/aminsa_web_daemon.py")
    if os.path.exists(daemon_script):
        try:
            subprocess.Popen(
                ["/data/data/com.termux/files/usr/bin/python", daemon_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True
        except Exception:
            pass
    return False


def copy_to_clipboard(text: str) -> bool:
    try:
        p = subprocess.run(
            ["termux-clipboard-set"],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=4
        )
        if p.returncode == 0:
            return True
    except Exception:
        pass

    bin_path = "/data/data/com.termux/files/usr/bin/termux-clipboard-set"
    if os.path.exists(bin_path):
        try:
            p = subprocess.run([bin_path], input=text.encode("utf-8"), capture_output=True, timeout=4)
            if p.returncode == 0:
                return True
        except Exception:
            pass
    return False


def get_current_active_slot(slots):
    now = datetime.now()
    cur_mins = now.hour * 60 + now.minute
    for s in slots:
        try:
            t_str = s["time"].strip()
            t_dt = datetime.strptime(t_str, "%I:%M %p")
            s_mins = t_dt.hour * 60 + t_dt.minute
            if cur_mins <= s_mins + 75:
                return s
        except Exception:
            continue
    return slots[0] if slots else None


def save_catalogs_safely():
    target_locations = [
        "/data/data/com.termux/files/home",
        "/data/data/com.termux",
        SCRIPT_DIR,
        "/sdcard/Download",
        "/sdcard/Documents",
        os.path.expanduser("~")
    ]

    # Generate fresh in SCRIPT_DIR first
    primary_excel = os.path.join(SCRIPT_DIR, "Aminsa_Master_Production_Catalog.xlsx")
    primary_html = os.path.join(SCRIPT_DIR, "Aminsa_Master_Production_Catalog.html")

    # 1. Generate Excel with Video Prompts ONLY
    try:
        generate_master_excel(primary_excel)
    except Exception as e:
        print(f"[-] Excel error: {e}")

    # 2. Generate ChatGPT-style HTML with Video Prompts ONLY
    date_str, slots, _ = get_current_day_data()
    if build_chatgpt_html:
        try:
            html_content = build_chatgpt_html(date_str, slots)
            with open(primary_html, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            print(f"[-] HTML error: {e}")

    # Mirror to all target directories
    for t_dir in target_locations:
        if os.path.exists(t_dir):
            try:
                dst_x = os.path.join(t_dir, "Aminsa_Master_Production_Catalog.xlsx")
                if dst_x != primary_excel and os.path.exists(primary_excel):
                    shutil.copyfile(primary_excel, dst_x)
                dst_h = os.path.join(t_dir, "Aminsa_Master_Production_Catalog.html")
                if dst_h != primary_html and os.path.exists(primary_html):
                    shutil.copyfile(primary_html, dst_h)
            except Exception:
                pass

    return primary_excel, primary_html, date_str, slots


def open_excel_on_device(excel_file):
    if not excel_file or not os.path.exists(excel_file):
        return False

    print("[*] Opening Excel Catalog in LibreOffice Viewer...")
    try:
        res = subprocess.run(["termux-open", excel_file], capture_output=True, timeout=5)
        if res.returncode == 0:
            print(f"[✓] Opened {os.path.basename(excel_file)} successfully!")
            return True
    except Exception:
        pass

    try:
        cmd = [
            "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", "file:///sdcard/Download/Aminsa_Master_Production_Catalog.xlsx",
            "-t", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "org.documentfoundation.libreoffice"
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=5)
        if res.returncode == 0:
            print("[✓] Opened in LibreOffice Viewer!")
            return True
    except Exception:
        pass

    return False


def format_slot_copy_text(s):
    lang_tag = s.get("language", "hinglish").upper()
    yt_post = s.get("yt_shorts_posting", "")
    return (
        f"[SLOT {s['slot']} | {s['time']}] {s['title']} ({lang_tag})\n"
        f"--------------------------------------------------\n"
        f"🗣️ SCRIPT:\n{s['script']}\n\n"
        f"🎬 VIDEO PROMPT:\n{s['video_prompt']}\n\n"
        f"✨ YOUTUBE SHORTS (TITLE & TAGS):\n{yt_post}\n\n"
        f"📱 CAPTION:\n{s['caption']}\n"
    )


def main():
    print("=" * 70)
    print("    🌟 AMINSA REAL-TIME DYNAMIC VIDEO HUB 🌟")
    print("=" * 70)
    print("[*] Harvesting live real-time topics & building Video Prompts...")

    excel_file, html_file, date_str, slots = save_catalogs_safely()
    ensure_web_daemon()

    # Automatically launch Excel
    open_excel_on_device(excel_file)

    # Auto-copy current active slot
    active_slot = get_current_active_slot(slots)
    if active_slot:
        clip_txt = format_slot_copy_text(active_slot)
        if copy_to_clipboard(clip_txt):
            lang_label = active_slot.get('language', 'hinglish').upper()
            print("\n" + "-" * 70)
            print(f"📋 [AUTO-COPIED TO PHONE CLIPBOARD]: Slot #{active_slot['slot']} ({active_slot['time']}) [{lang_label}]")
            print(f"   📌 Topic: {active_slot['title']}")
            print("   👉 Ready! Paste directly into YouTube Create or WhatsApp!")
            print("-" * 70)

    # Print 10 daily live slots (Video Prompts ONLY)
    print("\n" + "=" * 70)
    print(f"  📱 10 DAILY REAL-TIME VIDEO SLOTS ({date_str})")
    print("=" * 70)

    for slot in slots:
        is_active = (active_slot and slot["slot"] == active_slot["slot"])
        star = "⭐ [ACTIVE NOW] " if is_active else ""
        lang_str = slot.get('language', 'hinglish').upper()
        print(f"\n▶ {star}[SLOT {slot['slot']} | {slot['time']}] {slot['category'].upper()} [{lang_str}]")
        print(f"  📌 TOPIC   : {slot['title']}")
        print(f"  🗣️ SCRIPT  : {slot['script']}")
        print(f"  🎬 VIDEO PROMPT:")
        print(f"     \"{slot['video_prompt'][:95]}...\"")
        print("-" * 70)

    # 1-Tap Guidance & URL
    print("\n" + "=" * 70)
    print("🌐 CHATGPT-STYLED DASHBOARD (1-TAP OPEN IN CHROME):")
    print("   👉 1-TAP BUTTON : Tap the [🌐DASH] button above your keyboard!")
    print("   👉 1-KEY OPTION : Type 'd' and hit Enter")
    print(f"   👉 BROWSER URL  : http://127.0.0.1:{WEB_PORT}/")
    print("=" * 70)
    print("✅ All systems ready. Exiting cleanly.\n")


if __name__ == "__main__":
    main()
