# -*- coding: utf-8 -*-
"""
Aminsa 24/7 Autonomous Laptop Long-Form Broadcast Factory
=========================================================
Runs 100% independently on Laptop PC.
Exclusively Dedicated to Long-Form Videos & Epic Stories (10 Minutes to 1 Hour):
- 5 Productions Daily: 10-Minute Concept Films & Tech Stories (1920x1080 60FPS)
- 5 Productions Daily: 1-Hour Long-Form Epic AI Sagas & Documentaries (1920x1080 60FPS)
- Total: 10 Long-Form Productions per 24 hours.

Directly renders actual MP4 video files into exports/films_10min/ and exports/epics_1hr/,
updates Aminsa_Master_Production_Catalog.xlsx with timestamps, descriptions, and hashtags,
and syncs completed long-form media to OPPO A78 5G!
"""

import os
import sys
import time
import json
import random
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.laptop_master_avatar_studio import avatar_studio
from engines.rss_intelligence_hub import rss_hub, CATEGORIES
from engines.aminsa_catalog_engine import generate_master_excel, get_current_day_data
from engines.daily_master_face_engine import daily_face_engine

ADB_PATH = r"C:\platform-tools\adb.exe"
LOG_FILE = os.path.join(PROJECT_ROOT, "data", "autonomous_factory_audit.json")
os.makedirs(os.path.join(PROJECT_ROOT, "data"), exist_ok=True)

def check_oppo_device():
    try:
        res = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True)
        for line in res.stdout.strip().splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                return parts[0]
    except Exception:
        pass
    return None

def push_to_oppo_gallery(video_path):
    serial = check_oppo_device()
    if not serial:
        print("[!] OPPO A78 5G is not connected. Video preserved in local laptop exports.")
        return False
        
    print(f"[*] Detected OPPO A78 5G ({serial})")
    dest_dir = "/sdcard/DCIM/Aminsa/LongForm"
    subprocess.run([ADB_PATH, "shell", f"mkdir -p {dest_dir}"], capture_output=True)
    
    filename = os.path.basename(video_path)
    phone_dest = f"{dest_dir}/{filename}"
    print(f"[*] Pushing {filename} to {phone_dest}...")
    
    push_res = subprocess.run([ADB_PATH, "push", video_path, phone_dest], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("[✓] Long-form video pushed to OPPO A78 5G Gallery!")
        scan_cmd = f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{phone_dest}"
        subprocess.run([ADB_PATH, "shell", scan_cmd], capture_output=True)
        return True
    return False

def log_production(entry):
    entries = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            entries = []
    entries.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def run_longform_production_cycle(slot_idx=None, force_mode=None):
    now = datetime.now()
    cur_hour = now.hour

    _, laptop_slots = get_current_day_data(now)

    # Select slot based on current hour or provided index
    if slot_idx is None:
        slot_idx = (cur_hour // 2) % len(laptop_slots)
    target_slot = laptop_slots[slot_idx]

    # 1. Autonomous Daily Master Clean Face check (aminsa-360-day-bases-face-images)
    try:
        daily_face_engine.ensure_today_master_face()
        daily_face_engine.sync_to_phone()
    except Exception as e:
        print(f"[-] Daily face check note: {e}")

    mode = force_mode if force_mode else ("1h" if "1-Hour" in target_slot["format"] else "10m")

    print(f"\n{'='*75}")
    print(f"[*] [AMINSA LAPTOP LONG-FORM STUDIO] Production Run at {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Slot #{target_slot['slot']} ({target_slot['time']}) | Mode: {mode.upper()} | Format: {target_slot['format']}")
    print(f"[*] Title: {target_slot['title']}")
    print(f"{'='*75}")

    topic_item = {
        "title": target_slot["title"],
        "category": target_slot["category"],
        "link": "https://aminsa.official"
    }

    if mode == "10m":
        print("[*] Generating 10-Minute Concept Film Narrative Chapters...")
        chapters = rss_hub.generate_10min_script_chapters(topic_item)
        video_path = avatar_studio.render_10min_concept_explainer(topic_item, chapters)
    else:
        print("[*] Generating 1-Hour Epic Cinematic Saga Episodes...")
        episodes = rss_hub.generate_1hr_epic_story_chapters(topic_item)
        video_path = avatar_studio.render_1hr_epic_story(topic_item, episodes)

    video_size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)
    print(f"[✓] Successfully Rendered Video: {video_path} ({video_size_mb} MB)")

    pushed = push_to_oppo_gallery(video_path)

    log_entry = {
        "timestamp": now.isoformat(),
        "slot": target_slot["slot"],
        "time": target_slot["time"],
        "format": target_slot["format"],
        "title": target_slot["title"],
        "category": target_slot["category"],
        "video_path": video_path,
        "file_size_mb": video_size_mb,
        "pushed_to_oppo": pushed
    }
    log_production(log_entry)

    # Refresh Master Excel
    try:
        catalog_path = os.path.join(PROJECT_ROOT, "Aminsa_Master_Production_Catalog.xlsx")
        generate_master_excel(catalog_path)
    except Exception as e:
        print(f"[-] Catalog refresh note: {e}")

    print(f"[✓] Production record logged into data/autonomous_factory_audit.json")
    return log_entry

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Aminsa Autonomous Long-Form Broadcast Studio")
    parser.add_argument("--once", action="store_true", help="Run a single long-form production cycle and exit")
    parser.add_argument("--slot", type=int, default=None, help="Target specific slot number (1-10)")
    parser.add_argument("--mode", choices=["10m", "1h"], default=None, help="Force duration mode (10m or 1h)")
    parser.add_argument("--interval", type=int, default=8640, help="Interval in seconds between cycles (default: 8640s = 2.4 hrs)")
    args = parser.parse_args()

    if args.once:
        slot_idx = (args.slot - 1) if args.slot else None
        run_longform_production_cycle(slot_idx=slot_idx, force_mode=args.mode)
    else:
        print(f"[*] [AMINSA 24/7 LONG-FORM FACTORY] Daemon Started (Interval: {args.interval}s)...")
        while True:
            try:
                run_longform_production_cycle(force_mode=args.mode)
            except Exception as e:
                print(f"[-] Error in production cycle: {e}")
            print(f"[*] Sleeping for {args.interval}s until next long-form production slot...")
            time.sleep(args.interval)
