"""
Md Sadique Amin 24/7 Autonomous Background Scheduler Daemon
Runs continuously in the background on your laptop:
- Executes a full content generation cycle every 2.5 hours (±15 mins random jitter)
- Night sleep window: 01:30 AM to 06:30 AM IST (humanized behavior to prevent account fatigue)
- Auto-harvests viral trends, synthesizes 224 Hz voice, renders 9:16 vertical reels
- Logs complete telemetry into reports/daily_performance.xlsx
"""

import os
import sys
import time
import random
import asyncio
from datetime import datetime

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from master_orchestrator import run_pipeline

INTERVAL_HOURS = 2.5
JITTER_MINUTES = 15

def is_night_sleep_window():
    now = datetime.now()
    # 01:30 AM to 06:30 AM
    if now.hour == 1 and now.minute >= 30:
        return True
    if 2 <= now.hour < 6:
        return True
    if now.hour == 6 and now.minute < 30:
        return True
    return False

async def daemon_loop():
    print("=" * 80)
    print("🤖 MD_SADIQUE_AMIN 24/7 AUTONOMOUS BACKGROUND SCHEDULER: ACTIVATED")
    print("=" * 80)
    print(f"[*] Base Interval: Every {INTERVAL_HOURS} hours (± {JITTER_MINUTES} mins jitter)")
    print("[*] Humanized Sleep Window: 01:30 AM - 06:30 AM IST (Paused during late night)")
    print("[*] Continuous Telemetry: Logged to reports/daily_performance.xlsx\n")
    
    cycle_counter = 1
    while True:
        try:
            if is_night_sleep_window():
                print(f"[*] [Night Window] Resting persona Md Sadique Amin until 06:30 AM IST...")
                time.sleep(1800)  # Check every 30 mins
                continue
                
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Initiating Autonomous Scheduled Cycle #{cycle_counter}...")
            await run_pipeline()
            cycle_counter += 1
            
        except Exception as e:
            print(f"[!] Cycle error encountered: {e}")
            
        # Calculate next execution time with random jitter
        jitter_sec = random.randint(-JITTER_MINUTES * 60, JITTER_MINUTES * 60)
        sleep_sec = max(int(INTERVAL_HOURS * 3600 + jitter_sec), 3600)
        next_run = datetime.fromtimestamp(time.time() + sleep_sec)
        print(f"\n💤 Cycle completed! Md Sadique Amin resting for {sleep_sec / 3600:.2f} hours.")
        print(f"⏰ Next autonomous cycle scheduled at: {next_run.strftime('%Y-%m-%d %H:%M:%S IST')}")
        print("=" * 80)
        
        await asyncio.sleep(sleep_sec)

if __name__ == "__main__":
    asyncio.run(daemon_loop())
