# -*- coding: utf-8 -*-
"""
Aminsa Unified Mobile Service (24/7 Production + Dynamic Web Hub)
=================================================================
Single unified background process for Termux on Android (OPPO A78 5G).
Eliminates disconnect between web server and production daemon:
1. Runs the 2.4-Hour Autonomous Production Loop (Slot Production, Speech, Prompts, Social Triggers).
2. Runs the Dynamic Real-Time Web Server on port 8765 in a lightweight concurrent thread.
3. Automatically regenerates both Web Dashboard and Excel Catalog on slot change & midnight rollover.
4. Full Android Wake-Lock and Local ADB Bridge persistence.
"""

import os
import sys
import time
import socket
import threading
import datetime
import traceback
from http.server import HTTPServer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Ensure Termux bin is in PATH
os.environ["PATH"] = "/data/data/com.termux/files/usr/bin:" + os.environ.get("PATH", "")

from config import (
    SDCARD_DIR, LOG_FILE, TOTAL_DAILY_SLOTS, CYCLE_HOURS,
    CATEGORIES, PERSONA_NAME
)
from topic_engine import get_slot_topic_and_prompts
from tts_engine import generate_voice
from adb_bridge import bridge
from youtube_create_driver import yt_driver
from social_poster import social_poster
from aminsa_web_daemon import AminsaWebHandler, ensure_fresh_catalog, PORT as WEB_PORT


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass


def get_current_slot_index():
    now = datetime.datetime.now()
    minutes_since_midnight = now.hour * 60 + now.minute
    total_slot_minutes = 24 * 60 / TOTAL_DAILY_SLOTS  # 144 mins = 2.4 hours
    return int(minutes_since_midnight // total_slot_minutes) % TOTAL_DAILY_SLOTS


def execute_slot_cycle(slot_idx=None, skip_yt_generation=False):
    """Executes a single autonomous production and publishing cycle."""
    if slot_idx is None:
        slot_idx = get_current_slot_index()

    log("=" * 65)
    log(f"🚀 EXECUTING AMINSA AMIN UNIFIED CYCLE — SLOT #{slot_idx + 1}/{TOTAL_DAILY_SLOTS}")
    log("=" * 65)

    # 1. Ensure ADB bridge is connected (localhost loopback)
    connected, info = bridge.ensure_connected()
    if connected:
        log(f"[✓] ADB Local Bridge Connected: {info}")
    else:
        log(f"[!] Note: ADB Local Bridge: {info}")

    # 2. Fetch Topic & Generate Dynamic 250-300 char Prompt + 10s Statement
    log("[*] Generating master context, dynamic 7-day attire, setting & prompts...")
    data = get_slot_topic_and_prompts(slot_idx)
    log(f"[+] Category: {data['slot_name']} ({data['category']})")
    log(f"[+] Dynamic Attire: {data['look']['attire']}")
    log(f"[+] Dynamic Setting: {data['look']['setting']}")
    log(f"[+] Video Prompt ({len(data['yt_create_prompt'])} chars): {data['yt_create_prompt']}")
    log(f"[+] Speech Script: {data['speech_script']}")
    log(f"[+] YouTube Shorts Title ({len(data.get('yt_shorts_posting', ''))} chars): {data.get('yt_shorts_posting', '')}")

    # 3. Synchronize Web Dashboard & Excel Catalog Immediately
    try:
        log("[*] Updating Live Web Dashboard & Excel Catalog for this slot...")
        ensure_fresh_catalog(force_refresh=True)
        log("[✓] Web Dashboard & Excel Catalog 100% in sync.")
    except Exception as e:
        log(f"[!] Catalog sync warning: {e}")

    # 4. Synthesize Aminsa Signature Voice (hi-IN-SwaraNeural)
    audio_path = None
    try:
        log("[*] Synthesizing Aminsa Amin signature voice (hi-IN-SwaraNeural)...")
        audio_name = f"aminsa_slot_{slot_idx + 1}_{int(time.time())}.mp3"
        audio_path = generate_voice(data["speech_script"], audio_name)
        log(f"[✓] Voice synthesized: {audio_path}")
    except Exception as e:
        log(f"[!] Voice error: {e}")

    # 5. YouTube Create 2-Step Automation (Image -> Video)
    if not skip_yt_generation and connected:
        try:
            log("[*] [YouTube Create] Executing Step 1 (Locked Face Image) -> Step 2 (Video from Image)...")
            res = yt_driver.run_full_two_step_cycle(data["yt_create_prompt"], data["yt_video_prompt"])
            log(f"[✓] Step 1 Image proof: {res['image_proof']}")
            log(f"[✓] Step 2 Video proof: {res['video_proof']}")
        except Exception as e:
            log(f"[!] YouTube Create error: {e}")
    else:
        log("[i] YouTube Create execution skipped (dry-run or awaiting user action).")

    # 6. Android Notification
    bridge.notify(
        title=f"Aminsa AI: Slot #{slot_idx + 1} Ready!",
        message=f"{data['slot_name']}: {data['yt_shorts_posting']}"
    )
    log(f"[✓] Slot #{slot_idx + 1} cycle complete!")
    log("=" * 65)
    return True


def start_web_server_thread():
    """Runs the dynamic web daemon in a daemon thread."""
    try:
        server_address = ("0.0.0.0", WEB_PORT)
        httpd = HTTPServer(server_address, AminsaWebHandler)
        log(f"[✓] [Web Daemon] Serving dynamic dashboard at http://127.0.0.1:{WEB_PORT}/")
        httpd.serve_forever()
    except Exception as e:
        log(f"[-] [Web Daemon] Error: {e}")


def run_unified_service():
    """Main 24/7 unified loop."""
    log("=" * 65)
    log("🌟 AMINSA UNIFIED 24/7 MOBILE SERVICE STARTING")
    log(f"[*] Schedule: 10 dynamic slots / 24 hours (every {CYCLE_HOURS}h)")
    log(f"[*] Web Server Port: {WEB_PORT}")
    log("=" * 65)

    bridge.acquire_wake_lock()
    log("[+] Termux wake-lock active — service running continuously with screen off.")

    # Start Web Server in concurrent thread
    web_thread = threading.Thread(target=start_web_server_thread, daemon=True)
    web_thread.start()

    # Pre-warm catalog
    try:
        ensure_fresh_catalog()
    except Exception:
        pass

    last_slot = -1
    while True:
        try:
            curr_slot = get_current_slot_index()
            if curr_slot != last_slot:
                log(f"[*] New slot detected: #{curr_slot + 1}")
                execute_slot_cycle(curr_slot)
                last_slot = curr_slot
            else:
                time.sleep(120)  # Check every 2 minutes
        except KeyboardInterrupt:
            log("[!] Unified service stopped by user.")
            bridge.release_wake_lock()
            break
        except Exception as e:
            log(f"[!] Service loop exception: {e}")
            log(traceback.format_exc())
            time.sleep(60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        execute_slot_cycle(skip_yt_generation=False)
    elif len(sys.argv) > 1 and sys.argv[1] == "--slot":
        slot_num = int(sys.argv[2])
        execute_slot_cycle(slot_idx=slot_num, skip_yt_generation=False)
    else:
        run_unified_service()
