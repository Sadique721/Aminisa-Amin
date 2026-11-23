# -*- coding: utf-8 -*-
"""
Aminsa IST Daily Slot Scheduler & Recovery Engine
=================================================
Manages timezone-aware scheduling across Asia/Kolkata (IST):
1. Content Cycle starts at 08:00 AM IST.
2. 10 Daily Slots (144 minutes / 2.4 hours each).
3. Slots 8, 9, 10 occur on the following calendar date (midnight rollover handling).
4. Durable idempotency keys: {cycle_date}:{slot_id}:{content_version}.
5. Safe restart recovery with configurable catch-up policy (zero duplicate generation).
"""

import os
import sys
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.production_ledger_db import ledger_db
from engines.daily_production_packager import packager

IST_TZ = timezone(timedelta(hours=5, minutes=30))

# Slot offsets from cycle start (08:00 AM IST) in minutes
SLOT_MINUTE_OFFSETS = {
    1: 0,     # 08:00 AM
    2: 144,   # 10:24 AM
    3: 288,   # 12:48 PM
    4: 432,   # 03:12 PM
    5: 576,   # 05:36 PM
    6: 720,   # 08:00 PM
    7: 864,   # 10:24 PM
    8: 1008,  # 12:48 AM (next calendar day)
    9: 1152,  # 03:12 AM (next calendar day)
    10: 1296  # 05:36 AM (next calendar day)
}


class ISTDailyScheduler:
    """Manages cycle dates, slot timings, and idempotent recovery."""

    def __init__(self, db=None, prod_packager=None):
        self.db = db or ledger_db
        self.packager = prod_packager or packager

    def get_current_ist_time(self) -> datetime:
        """Returns current time in Asia/Kolkata timezone."""
        return datetime.now(IST_TZ)

    def get_cycle_date_for_time(self, dt_ist: Optional[datetime] = None) -> str:
        """
        Determines the content cycle date for a given IST timestamp.
        Rule: Content cycle starts at 08:00 AM IST.
        Times from 00:00 to 07:59 AM belong to the cycle that started yesterday at 08:00 AM.
        """
        dt = dt_ist or self.get_current_ist_time()
        if dt.hour < 8:
            cycle_dt = dt - timedelta(days=1)
        else:
            cycle_dt = dt
        return cycle_dt.strftime("%Y-%m-%d")

    def get_active_slot_for_time(self, dt_ist: Optional[datetime] = None) -> Tuple[int, str]:
        """
        Determines current active slot index (1 to 10) based on elapsed time from 08:00 AM IST.
        """
        dt = dt_ist or self.get_current_ist_time()
        cycle_date_str = self.get_cycle_date_for_time(dt)

        cycle_start_dt = datetime.strptime(f"{cycle_date_str} 08:00:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=IST_TZ)
        elapsed_minutes = (dt - cycle_start_dt).total_seconds() / 60.0

        if elapsed_minutes < 0:
            elapsed_minutes = 0

        # Slot is determined by 144-minute windows
        slot_idx = int(elapsed_minutes // 144) + 1
        slot_idx = max(1, min(10, slot_idx))

        return slot_idx, cycle_date_str

    def run_slot_if_pending(self, slot_id: int, cycle_date: str) -> Dict[str, Any]:
        """
        Idempotently executes generation for a slot only if it has not yet been produced.
        Survives restarts and prevents duplicate generation.
        """
        existing = self.db.get_slot(cycle_date, slot_id)
        if existing and existing.get("production_status") != "PENDING":
            print(f"[Scheduler] Slot #{slot_id:02d} for cycle {cycle_date} already generated ({existing['youtube_title']}). Skipping duplicate execution.")
            return existing

        t_start = time.time()
        print(f"[Scheduler] Generating Slot #{slot_id:02d} for cycle {cycle_date}...")
        slot_data = self.packager.generate_slot_package(slot_id, cycle_date)
        duration_ms = int((time.time() - t_start) * 1000)

        # Record scheduler run
        with self.db.get_conn() as conn:
            conn.execute("""
            INSERT INTO scheduler_runs (cycle_date, slot_id, run_at_ist, run_type, status, notes, duration_ms)
            VALUES (?, ?, ?, 'SCHEDULED', 'SUCCESS', ?, ?);
            """, (
                cycle_date, slot_id,
                self.get_current_ist_time().strftime("%Y-%m-%d %H:%M:%S IST"),
                f"Generated {slot_data['youtube_title'][:50]}",
                duration_ms
            ))
            conn.commit()

        return slot_data

    def catch_up_missed_slots(self, cycle_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Checks all slots up to the active slot index for the current cycle.
        Generates any missing slots safely without re-generating completed slots.
        """
        current_dt = self.get_current_ist_time()
        active_slot, active_cycle = self.get_active_slot_for_time(current_dt)
        target_cycle = cycle_date or active_cycle

        self.db.ensure_cycle(target_cycle)
        results = []

        print(f"[Scheduler Catch-Up] Active Cycle: {target_cycle} | Active Slot: #{active_slot:02d}")
        for s_id in range(1, active_slot + 1):
            slot_res = self.run_slot_if_pending(s_id, target_cycle)
            results.append(slot_res)

        return results


ist_scheduler = ISTDailyScheduler()

if __name__ == "__main__":
    now_ist = ist_scheduler.get_current_ist_time()
    cycle = ist_scheduler.get_cycle_date_for_time(now_ist)
    slot, _ = ist_scheduler.get_active_slot_for_time(now_ist)
    print(f"Current IST Time: {now_ist.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Content Cycle:    {cycle}")
    print(f"Active Slot:      Slot #{slot:02d}")
    print("Running idempotent catch-up verification...")
    res = ist_scheduler.catch_up_missed_slots()
    print(f"Catch-up completed. Total slots verified: {len(res)}")
