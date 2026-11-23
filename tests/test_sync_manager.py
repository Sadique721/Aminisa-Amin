# -*- coding: utf-8 -*-
"""
Unit Tests for Aminsa Multi-Node Synchronization & Job Leasing Engine
"""

import os
import sys
import unittest

_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_DIR)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from engines.sync_manager import (
    SyncManager,
    DEFAULT_LAPTOP_NODE,
    DEFAULT_MOBILE_NODE,
    get_cycle_date_str
)
from engines.production_ledger_db import ledger_db


class TestSyncManager(unittest.TestCase):

    def setUp(self):
        self.sm = SyncManager()

    def test_default_nodes_and_heartbeat(self):
        """Test default node registration and heartbeat recording."""
        self.assertTrue(self.sm.record_heartbeat(DEFAULT_LAPTOP_NODE))
        self.assertTrue(self.sm.record_heartbeat(DEFAULT_MOBILE_NODE, ip_address="192.168.1.100"))
        self.assertTrue(self.sm.is_node_online(DEFAULT_LAPTOP_NODE))
        self.assertTrue(self.sm.is_node_online(DEFAULT_MOBILE_NODE))

    def test_job_lifecycle_leasing_and_completion(self):
        """Test job creation, atomic lease acquisition, and completion."""
        import time
        cycle_date = get_cycle_date_str()
        slot_id = 1
        job_type = f"TTS_SYNTHESIS_{int(time.time() * 1000)}"
        payload = {"script": "Namaste India", "voice": "hi-IN-SwaraNeural"}

        # Create job
        idemp_key = self.sm.create_generation_job(
            node_id=DEFAULT_LAPTOP_NODE,
            job_type=job_type,
            cycle_date=cycle_date,
            slot_id=slot_id,
            payload=payload,
            version=1
        )
        self.assertIn(f"{cycle_date}:{slot_id}:1:{job_type}", idemp_key)

        # Acquire lease by mobile node
        lease = self.sm.acquire_job_lease(node_id=DEFAULT_MOBILE_NODE, job_type=job_type, lease_seconds=60)
        self.assertIsNotNone(lease)
        self.assertEqual(lease["job_type"], job_type)
        self.assertEqual(lease["slot_id"], slot_id)

        # Complete job
        result = {"audio_path": "/sdcard/Aminsa/audio_1.mp3", "duration": 11.2}
        completed = self.sm.complete_job(lease["job_id"], DEFAULT_MOBILE_NODE, result)
        self.assertTrue(completed)

    def test_sync_package_export_and_checkpoint(self):
        """Test export and sync checkpointing."""
        cycle_date = get_cycle_date_str()
        pack = self.sm.export_sync_package(cycle_date)
        self.assertEqual(pack["version"], "1.0")
        self.assertEqual(pack["cycle_date"], cycle_date)
        self.assertIn("slots", pack)

        # Create checkpoint
        chk_id = self.sm.create_sync_checkpoint(
            source_node=DEFAULT_MOBILE_NODE,
            target_node=DEFAULT_LAPTOP_NODE,
            event_type="TEST_SYNC",
            details={"test": True}
        )
        self.assertGreater(chk_id, 0)

        status = self.sm.get_ecosystem_status()
        self.assertGreaterEqual(status["active_node_count"], 2)


if __name__ == "__main__":
    unittest.main()
