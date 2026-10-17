# -*- coding: utf-8 -*-
"""
Automated Verification Suite for Cloud Direct Publisher
Verifies standalone zero-connection publishing architecture.
"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engines.cloud_direct_publisher import CloudDirectPublisher

class TestCloudDirectPublisher(unittest.TestCase):
    def setUp(self):
        self.pub = CloudDirectPublisher()

    def test_01_ledger_initialization(self):
        self.assertTrue(os.path.exists(self.pub.ledger_file))
        with open(self.pub.ledger_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("system", data)
        self.assertIn("slots", data)

    def test_02_slot_logging_and_query(self):
        mock_results = {"test": True, "mode": "VERIFICATION"}
        self.pub.log_slot(99, "Test Unit Title", "Testing Category", mock_results)
        self.assertTrue(self.pub.is_slot_published(99))

    def test_03_standalone_execution_flow(self):
        # Create a dummy MP4 file for dry-run verification
        dummy_mp4 = os.path.join(os.path.dirname(__file__), "scratch", "dummy_test.mp4")
        os.makedirs(os.path.dirname(dummy_mp4), exist_ok=True)
        with open(dummy_mp4, "wb") as f:
            f.write(b"FAKE_MP4_HEADER_DATA_FOR_TESTING")

        results = self.pub.publish_all_standalone(
            video_path=dummy_mp4,
            slot_id=98,
            title="Sunday Morning: Rajma Chawal Secret Algorithm",
            category="Mummy's Sunday Special",
            caption="Hello everyone! Test caption for zero-connection publishing."
        )

        self.assertIn("facebook", results)
        self.assertIn("instagram", results)
        self.assertIn("wireless_relay", results)
        self.assertTrue(self.pub.is_slot_published(98))

        if os.path.exists(dummy_mp4):
            os.remove(dummy_mp4)

if __name__ == "__main__":
    unittest.main()
