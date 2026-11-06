# -*- coding: utf-8 -*-
"""
Aminsa Amin Daily 5-Image Autonomous Scheduler
==============================================
Orchestrates automated daily production of 5 pristine Aminsa images:
- Automatically creates daily_generated_images/YYYY-MM-DD/ every single day.
- Generates 5 unique modern outfits, diverse locations, and festival topics.
- Strict Biometric Lock: Cosine similarity >= 0.70 (typically 0.93-0.96).
- Checks and syncs to phone via ADB when phone is connected.
- Runs 24/7 in background or via Windows Task Scheduler.
"""

import os
import sys
import time
import json
import argparse
import subprocess
from datetime import datetime
import datetime as dt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.daily_5_images_generator import daily_image_generator

SCHEDULER_CONFIG_PATH = os.path.join(PROJECT_ROOT, "state", "image_scheduler_config.json")
ADB_PATH = r"C:\platform-tools\adb.exe"

class Daily5ImageScheduler:
    def __init__(self):
        self.config_path = SCHEDULER_CONFIG_PATH
        self.load_config()

    def load_config(self):
        default_cfg = {
            "status": "ARMED_ACTIVE",
            "daily_target_count": 5,
            "scheduled_slots": ["07:00", "11:00", "15:00", "19:00", "22:00"],
            "last_run_date": None,
            "auto_phone_sync": True,
            "face_similarity_threshold": 0.70,
            "output_directory": "daily_generated_images"
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = default_cfg
        else:
            self.config = default_cfg
            self.save_config()

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def arm_scheduler(self):
        """Arms and activates the scheduler permanently."""
        self.config["status"] = "ARMED_ACTIVE"
        self.save_config()
        print("\n[✔] SCHEDULER STATUS: ARMED & ACTIVE!")
        print("    Daily 5-Image production will execute automatically every day.")

    def disarm_scheduler(self):
        """Puts scheduler into standby/unarmed mode."""
        self.config["status"] = "UNARMED_READY"
        self.save_config()
        print("\n[i] SCHEDULER STATUS: UNARMED / STANDBY.")

    def sync_to_phone(self, date_str):
        """Pushes today's dated folder to phone if ADB is connected."""
        dated_dir = os.path.join(PROJECT_ROOT, "daily_generated_images", date_str)
        if not os.path.exists(dated_dir) or not os.path.exists(ADB_PATH):
            return False

        try:
            res = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True, timeout=5)
            lines = res.stdout.strip().splitlines()[1:]
            devices = [l.split()[0] for l in lines if "\tdevice" in l]
            if not devices:
                return False

            phone_dest = f"/sdcard/DCIM/Aminsa/daily_generated_images/{date_str}"
            subprocess.run([ADB_PATH, "shell", f"mkdir -p {phone_dest}"], check=True, timeout=10)
            subprocess.run([ADB_PATH, "push", dated_dir, f"/sdcard/DCIM/Aminsa/daily_generated_images/"], check=True, timeout=30)
            print(f"[✔] Successfully synced {date_str} pack to Phone: {phone_dest}")
            return True
        except Exception:
            return False

    def catch_up_missed_days(self, days_back=7):
        """Checks past days; if laptop was OFF, automatically generates missing dates."""
        today = dt.date.today()
        for i in range(days_back, 0, -1):
            past_date = today - dt.timedelta(days=i)
            past_str = past_date.strftime("%Y-%m-%d")
            dated_dir = os.path.join(PROJECT_ROOT, "daily_generated_images", past_str)
            if not os.path.exists(dated_dir):
                print(f"[*] Auto Catch-Up: Generating missing pack for offline day ({past_str})...")
                try:
                    daily_image_generator.generate_daily_pack(past_str)
                    if self.config.get("auto_phone_sync"):
                        self.sync_to_phone(past_str)
                except Exception as e:
                    print(f"[-] Catch-up error on {past_str}: {e}")

    def run_daily_cycle(self, force=False):
        """Runs the 5-image production cycle for today with auto catch-up for offline days."""
        # 1. Auto Catch-Up for any days laptop was turned off
        self.catch_up_missed_days(days_back=7)

        # 2. Today's cycle
        today_str = datetime.now().strftime("%Y-%m-%d")
        if not force and self.config.get("last_run_date") == today_str:
            print(f"[i] Today's pack ({today_str}) already generated. Use --force to regenerate.")
            return True

        print(f"\n[*] Executing Aminsa Daily 5-Image Production Cycle for {today_str}...")
        manifest = daily_image_generator.generate_daily_pack(today_str)

        self.config["last_run_date"] = today_str
        self.save_config()

        # Phone Sync
        if self.config.get("auto_phone_sync"):
            self.sync_to_phone(today_str)

        return manifest

    def run_daemon_loop(self):
        """Runs continuous background daemon that triggers new pack when date changes."""
        print("=" * 65)
        print("🌟 AMINSA AMIN 24/7 DAILY 5-IMAGE SCHEDULER DAEMON ACTIVE")
        print("=" * 65)
        self.arm_scheduler()

        # Ensure today's pack exists
        self.run_daily_cycle()

        while True:
            try:
                today_str = datetime.now().strftime("%Y-%m-%d")
                if self.config.get("last_run_date") != today_str:
                    print(f"\n[*] New day detected: {today_str}! Starting 5-image generation...")
                    self.run_daily_cycle()
                
                # Sleep for 10 minutes before next check
                time.sleep(600)
            except KeyboardInterrupt:
                print("\n[!] Daemon stopped by user.")
                break
            except Exception as e:
                print(f"[!] Scheduler error: {e}")
                time.sleep(60)

daily_scheduler = Daily5ImageScheduler()

def main():
    parser = argparse.ArgumentParser(description="Aminsa Daily 5-Image Scheduler")
    parser.add_argument("--run-now", action="store_true", help="Generate today's 5 images immediately")
    parser.add_argument("--force", action="store_true", help="Force regenerate today's images")
    parser.add_argument("--arm", action="store_true", help="Arm/Activate scheduler permanently")
    parser.add_argument("--disarm", action="store_true", help="Disarm/Standby scheduler")
    parser.add_argument("--daemon", action="store_true", help="Run as continuous background daemon")
    parser.add_argument("--status", action="store_true", help="Check scheduler configuration and status")
    args = parser.parse_args()

    if args.arm:
        daily_scheduler.arm_scheduler()
    elif args.disarm:
        daily_scheduler.disarm_scheduler()
    elif args.daemon:
        daily_scheduler.run_daemon_loop()
    elif args.status:
        print("\n" + "=" * 60)
        print("📊 AMINSA DAILY 5-IMAGE SCHEDULER STATUS")
        print("=" * 60)
        print(json.dumps(daily_scheduler.config, indent=2))
    elif args.run_now:
        daily_scheduler.run_daily_cycle(force=args.force)
    else:
        # Default behavior: Ensure today is generated and arm
        daily_scheduler.arm_scheduler()
        daily_scheduler.run_daily_cycle(force=False)

if __name__ == "__main__":
    main()
