# -*- coding: utf-8 -*-
"""
================================================================================
AMINSA MASTER PLAN v2 — UNIFIED 24/7 SCHEDULER (scheduler.py)
================================================================================
Orchestrates both Image Pipeline (File 1) and Reel Pipeline (File 2)
using APScheduler in Asia/Kolkata timezone with job overlap locks,
30-minute misfire grace time, and Excel audit logging.
================================================================================
"""

import os
import sys
import time
import json
import threading
import datetime as dt
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from image_pipeline.image_factory import image_factory, SLOTS as IMAGE_SLOTS
from reel_pipeline.reel_factory import reel_factory, REEL_SLOTS
from shared.publish.token_refresh import refresh_threads_token

# Single reentrant execution lock to prevent overlapping runs
EXECUTION_LOCK = threading.Lock()

def scheduled_image_job(slot_time):
    if not EXECUTION_LOCK.acquire(blocking=False):
        print(f"[WARN] Job overlap prevented! Previous job is still processing. Skipping image slot {slot_time}.")
        return

    try:
        print(f"\n{'='*75}\n[TRIGGER] Scheduled Image Slot: {slot_time} IST\n{'='*75}")
        image_factory.run_slot(slot=slot_time)
    except Exception as e:
        print(f"[-] Error in image job {slot_time}: {e}")
    finally:
        EXECUTION_LOCK.release()

def scheduled_reel_job(slot_time):
    if not EXECUTION_LOCK.acquire(blocking=False):
        print(f"[WARN] Job overlap prevented! Previous job is still processing. Skipping reel slot {slot_time}.")
        return

    try:
        print(f"\n{'='*75}\n[TRIGGER] Scheduled Reel Slot: {slot_time} IST\n{'='*75}")
        reel_factory.run_slot(slot=slot_time)
    except Exception as e:
        print(f"[-] Error in reel job {slot_time}: {e}")
    finally:
        EXECUTION_LOCK.release()

def scheduled_midnight_state_reset():
    """Resets daily OOTD and festival status at 00:01 midnight."""
    print("\n[MIDNIGHT] Refreshing Aminsa World State & OOTD for new day...")
    state_file = os.path.join(PROJECT_ROOT, "state", "today.json")
    today_str = dt.date.today().isoformat()
    new_state = {
        "date": today_str,
        "ootd": {
            "style_category": "Western Modest",
            "outfit": "Sharp tailored charcoal blazer, cream silk blouse, tailored trousers",
            "shoes": "Italian block-heel nude pumps",
            "hair": "Sleek low chignon with face-framing natural tendrils",
            "frozen_until": "23:59:59"
        },
        "daily_post_count": {"images": 0, "reels": 0}
    }
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(new_state, f, indent=2)
    # Refresh tokens
    refresh_threads_token()


# ------------------------------------------------------------------------------
# AMINSA 360-DAY DAILY MASTER FACE & EXCEL WATCHER
# ------------------------------------------------------------------------------
def run_daily_face_and_excel_initialization():
    """Executes on startup and when internet connects to deploy today's face & catalog."""
    def _worker():
        try:
            from engines.daily_master_face_engine import daily_face_engine
            print("[*] [STARTUP HOOK] Deploying today's Excel Catalog & 4K Master Face (aminsa-face-YYYY-MM-DD.png)...")
            res = daily_face_engine.ensure_today_master_face(wait_if_offline=True)
            print(f"[✔] [STARTUP HOOK] Master Face Status: {res.get('status')} | File: {res.get('png')}")
            daily_face_engine.sync_to_phone()
        except Exception as e:
            print(f"[-] [STARTUP HOOK] Daily face initialization notice: {e}")

    t = threading.Thread(target=_worker, name="DailyFaceInitializer", daemon=True)
    t.start()

def main():
    print("=" * 80)
    print("STARTING AMINSA MASTER PLAN v2 — UNIFIED 24/7 SCHEDULER")
    print("Timezone: Asia/Kolkata | Image Slots: 4/day | Reel Slots: 3/day")
    print("=" * 80)

    scheduler = BlockingScheduler(timezone="Asia/Kolkata")

    # 1. Schedule Image Slots: 07:30, 11:30, 15:30, 19:30 IST
    for s in IMAGE_SLOTS:
        hr, mn = s.split(":")
        scheduler.add_job(
            scheduled_image_job,
            CronTrigger(hour=int(hr), minute=int(mn), timezone="Asia/Kolkata"),
            args=[s],
            id=f"image_slot_{s.replace(':', '')}",
            name=f"Image Factory Slot {s}",
            misfire_grace_time=1800, # 30 minutes grace
            coalesce=True
        )
        print(f"[+] Scheduled Image Job: {s} IST")

    # 2. Schedule Reel Slots: 09:30, 13:30, 17:30 IST
    for s in REEL_SLOTS:
        hr, mn = s.split(":")
        scheduler.add_job(
            scheduled_reel_job,
            CronTrigger(hour=int(hr), minute=int(mn), timezone="Asia/Kolkata"),
            args=[s],
            id=f"reel_slot_{s.replace(':', '')}",
            name=f"Reel Factory Slot {s}",
            misfire_grace_time=1800, # 30 minutes grace
            coalesce=True
        )
        print(f"[+] Scheduled Reel Job: {s} IST")

    # 3. Schedule Daily Midnight State Reset & Token Refresh at 00:01
    scheduler.add_job(
        scheduled_midnight_state_reset,
        CronTrigger(hour=0, minute=1, timezone="Asia/Kolkata"),
        id="midnight_reset",
        name="Midnight State Reset",
        misfire_grace_time=3600
    )
    print("[+] Scheduled Midnight State Reset & Token Refresh at 00:01 IST")

        # 4. Schedule Daily 00:00 Master Face & Catalog Generation
    scheduler.add_job(
        run_daily_face_and_excel_initialization,
        CronTrigger(hour=0, minute=0, timezone="Asia/Kolkata"),
        id="daily_face_generator_job",
        name="Daily Aminsa Master Face & Catalog Deployer",
        misfire_grace_time=3600,
        coalesce=True
    )
    print("[+] Scheduled Daily 00:00 Master Face & Catalog Generator (Asia/Kolkata)")

    print("\n[READY] Scheduler initialized with 8 daily cron events. Listening...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("[!] Scheduler stopped cleanly.")

if __name__ == "__main__":
    main()
