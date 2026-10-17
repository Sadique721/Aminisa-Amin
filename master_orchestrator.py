# -*- coding: utf-8 -*-
"""
Aminsa Master Long-Form Orchestrator (Laptop Studio)
===================================================
Produces full-length 10-Minute Concept Films & Tech Stories directly on Laptop PC.
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
from engines.rss_intelligence_hub import rss_hub
from engines.aminsa_catalog_engine import generate_master_excel, LAPTOP_LONGFORM_SLOTS

ADB_PATH = r"C:\platform-tools\adb.exe"

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

def run_master_orchestrator():
    start_time = time.time()
    cycle_id = f"CYC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print("=" * 80)
    print(f"🚀 AMINSA MASTER LONG-FORM ORCHESTRATOR: CYCLE [{cycle_id}]")
    print("=" * 80)

    # Pick a random long-form concept film slot
    chosen = random.choice(LAPTOP_LONGFORM_SLOTS[:5]) # 10-Minute Concept Film
    print(f"  🎬 Target Film : {chosen['title']}")
    print(f"  📂 Category    : {chosen['category']}")
    print(f"  ⏱️ Format      : {chosen['format']} ({chosen['duration']})")

    topic_item = {
        "title": chosen["title"],
        "category": chosen["category"],
        "link": "https://aminsa.official"
    }

    print("\n[Step 1/3] Generating Narrative Chapters...")
    chapters = rss_hub.generate_10min_script_chapters(topic_item)

    print("\n[Step 2/3] Rendering Full 10-Minute Concept Film (1920x1080 60FPS)...")
    video_path = avatar_studio.render_10min_concept_explainer(topic_item, chapters)
    video_size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)
    print(f"  🟢 Rendered MP4: {video_path} ({video_size_mb} MB)")

    print("\n[Step 3/3] Synchronizing to OPPO A78 5G & Updating Excel Catalog...")
    pushed = push_to_oppo_gallery(video_path)
    catalog_path = os.path.join(PROJECT_ROOT, "Aminsa_Master_Production_Catalog.xlsx")
    generate_master_excel(catalog_path)

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"🎉 MASTER LONG-FORM FILM PRODUCTION COMPLETED IN {elapsed:.1f}s!")
    print(f"  🎬 Video File  : {video_path}")
    print(f"  📱 Mobile Sync : {'SUCCESS' if pushed else 'LOCAL ONLY'}")
    print(f"  📊 Catalog     : {catalog_path}")
    print("=" * 80)

if __name__ == "__main__":
    run_master_orchestrator()
