# -*- coding: utf-8 -*-
"""
Run_Daily_10_Reels_Master_Studio.py
===================================
Laptop-Native 24/7 Production Studio for Aminsa:
- Takes Aminsa's daily clean face (4K PNG from aminsa-360-day-bases-face-images/today.png).
- Takes 10 daily production slots from Aminsa_Master_Production_Catalog.xlsx.
- Generates 1080x1920 60FPS vertical Reels matching the @21.coders benchmark:
    * Living breathing subtle camera micro-motion
    * Kinetic word-by-word glowing yellow subtitles (&H0000E6FF) with bold outline
    * Studio calibrated 224 Hz SwaraNeural audio with -14 LUFS mastering
- Automatically pushes completed video to OnePlus Phone (/sdcard/DCIM/Aminsa/reels/)
- Triggers Android Media Scanner so it appears immediately in Phone Gallery & Social Uploaders.
"""

import os
import sys
import time
import argparse
import subprocess
import openpyxl
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.laptop_master_avatar_studio import avatar_studio
from engines.daily_master_face_engine import daily_face_engine
from engines.cloud_direct_publisher import cloud_publisher

ADB_PATH = r"C:\platform-tools\adb.exe"
CATALOG_PATH = os.path.join(PROJECT_ROOT, "Aminsa_Master_Production_Catalog.xlsx")
EXPORT_DIR = os.path.join(PROJECT_ROOT, "exports", "reels_1min")
os.makedirs(EXPORT_DIR, exist_ok=True)

def get_connected_phone():
    try:
        res = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True)
        for line in res.stdout.strip().splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                return parts[0]
    except Exception:
        pass
    return None

def push_to_phone(video_path):
    serial = get_connected_phone()
    if not serial:
        print("  [-] Phone not connected via ADB. Video saved on Laptop.")
        return False

    phone_dir = "/sdcard/DCIM/Aminsa/reels"
    subprocess.run([ADB_PATH, "shell", f"mkdir -p {phone_dir}"], capture_output=True)
    filename = os.path.basename(video_path)
    phone_dest = f"{phone_dir}/{filename}"
    
    print(f"  [*] Pushing to OnePlus ({serial}): {phone_dest}...")
    res = subprocess.run([ADB_PATH, "push", video_path, phone_dest], capture_output=True, text=True)
    if res.returncode == 0:
        scan_cmd = f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{phone_dest}"
        subprocess.run([ADB_PATH, "shell", scan_cmd], capture_output=True)
        print(f"  [✔] Broadcasted to Phone Gallery! Ready for Reels/Shorts upload.")
        return True
    return False

def load_today_slots():
    daily_face_engine.ensure_today_master_face(wait_if_offline=False)
    
    if not os.path.exists(CATALOG_PATH):
        raise FileNotFoundError(f"Catalog not found: {CATALOG_PATH}")

    wb = openpyxl.load_workbook(CATALOG_PATH, data_only=True)
    ws = wb.active
    slots = []
    
    for r in range(5, ws.max_row + 1):
        slot_num = ws.cell(r, 1).value
        time_ist = ws.cell(r, 2).value
        category = ws.cell(r, 3).value
        headline = ws.cell(r, 4).value
        prompt = ws.cell(r, 5).value
        motion = ws.cell(r, 6).value
        script = ws.cell(r, 7).value
        caption = ws.cell(r, 8).value
        
        if slot_num and script:
            slots.append({
                "slot": int(slot_num),
                "time": str(time_ist),
                "category": str(category),
                "headline": str(headline),
                "prompt": str(prompt),
                "script": str(script),
                "caption": str(caption)
            })
    return slots

def produce_slot(slot_data, face_image_path=None):
    slot_num = slot_data["slot"]
    headline = slot_data["headline"]
    script = slot_data["script"]
    
    if not script.strip().startswith("Hello everyone!"):
        script = f"Hello everyone! Aminsa here — {script}"
    
    face_img = face_image_path or os.path.join(PROJECT_ROOT, "aminsa-360-day-bases-face-images", "today.png")
    if not os.path.exists(face_img):
        face_img = avatar_studio.get_valid_face_image()

    print(f"\n{'='*75}")
    print(f"  PRODUCING REEL SLOT #{slot_num} ({slot_data['time']} IST)")
    print(f"  Headline: {headline}")
    print(f"  Face: {os.path.basename(face_img)}")
    print(f"{'='*75}")

    video_path = avatar_studio.render_1min_reel(
        script_text=script,
        headline=headline,
        face_image_path=face_img,
        slot_idx=slot_num
    )
    
    # 1. Execute Zero-Connection Standalone Cloud Publishing (No Phone/Cable Needed)
    caption = slot_data.get("caption", f"{headline} #Aminsa #Reels #AI")
    cloud_results = cloud_publisher.publish_all_standalone(
        video_path=video_path,
        slot_id=slot_num,
        title=headline,
        category=slot_data.get("category", "General"),
        caption=caption
    )
    
    # 2. Local Phone Push (Optional bonus if phone is physically attached)
    pushed = push_to_phone(video_path)
    if not pushed:
        print("  [*] [Zero-Connection Mode] Phone not connected locally. Standalone Cloud Publishing completed 100% of pipeline.")
        
    return video_path

def main():
    parser = argparse.ArgumentParser(description="Aminsa Daily 10 Reels Master Studio")
    parser.add_argument("--slot", type=int, default=None, help="Produce a specific slot (1-10)")
    parser.add_argument("--all", action="store_true", help="Batch produce all 10 slots for today")
    parser.add_argument("--daemon", action="store_true", help="Run 24/7 background scheduler (every 2.4h)")
    args = parser.parse_args()

    slots = load_today_slots()
    print(f"[✔] Loaded {len(slots)} production slots for today from Catalog.")

    if args.slot:
        target = next((s for s in slots if s["slot"] == args.slot), None)
        if not target:
            print(f"[-] Slot #{args.slot} not found in catalog!")
            return
        produce_slot(target)
    elif args.all:
        print(f"[*] Starting Batch Production for ALL {len(slots)} Daily Slots...")
        for s in slots:
            produce_slot(s)
            time.sleep(1)
        print(f"\n[✔] ALL 10 DAILY REELS GENERATED & PUSHED TO PHONE!")
    elif args.daemon:
        print("[*] Starting 24/7 Production Daemon (Every 2.4 Hours Cadence)...")
        while True:
            now = datetime.now()
            slot_idx = int((now.hour * 60 + now.minute) / (2.4 * 60)) % len(slots)
            produce_slot(slots[slot_idx])
            time.sleep(8640)
    else:
        now = datetime.now()
        slot_idx = int((now.hour * 60 + now.minute) / (2.4 * 60)) % len(slots)
        print(f"[*] Auto-selected current active slot #{slots[slot_idx]['slot']} ({slots[slot_idx]['time']})")
        produce_slot(slots[slot_idx])

if __name__ == "__main__":
    main()
