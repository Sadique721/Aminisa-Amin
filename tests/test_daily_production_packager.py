# -*- coding: utf-8 -*-
"""
Unit Tests for Phase 4: Production Package & 32-Field Schema Validator
"""

import os
import sys
import unittest
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.production_ledger_db import ProductionLedgerDB
from engines.daily_production_packager import DailyProductionPackager


class TestDailyProductionPackager(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_file.close()
        self.db = ProductionLedgerDB(db_path=self.temp_file.name)
        self.packager = DailyProductionPackager(db=self.db)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

    def test_32_field_schema_integrity(self):
        cycle_date = "2026-11-23"
        slot1 = self.packager.generate_slot_package(slot_id=1, cycle_date=cycle_date)

        expected_fields = [
            "cycle_date", "slot_id", "scheduled_at_ist", "pillar", "language",
            "content_type", "topic", "story_summary", "factual_context",
            "verification_status", "sources", "publication_dates", "event_date",
            "opening_hook", "spoken_script", "estimated_duration_seconds",
            "image_to_video_prompt", "wardrobe", "background", "visual_composition",
            "camera_direction", "youtube_title", "title_character_count", "hashtags",
            "hashtag_character_count", "caption", "caption_character_count",
            "video_prompt_character_count", "duplicate_check", "identity_qa",
            "fact_qa", "production_status"
        ]

        for field in expected_fields:
            self.assertIn(field, slot1, f"Missing required field: {field}")

        self.assertEqual(len(expected_fields), 32)

    def test_youtube_title_hard_limit(self):
        cycle_date = "2026-11-23"
        for s_id in range(1, 11):
            s = self.packager.generate_slot_package(slot_id=s_id, cycle_date=cycle_date)
            title = s["youtube_title"]
            count = s["title_character_count"]

            self.assertEqual(len(title), count)
            self.assertLessEqual(count, 100, f"Slot #{s_id} title exceeds 100 characters: {count}")
            self.assertIn("#Aminsa", title, f"Slot #{s_id} missing #Aminsa hashtag")

    def test_video_prompt_hard_limit(self):
        cycle_date = "2026-11-23"
        for s_id in [2, 7]:  # Test Tech & Space slots
            s = self.packager.generate_slot_package(slot_id=s_id, cycle_date=cycle_date)
            prompt = s["image_to_video_prompt"]
            count = s["video_prompt_character_count"]

            self.assertEqual(len(prompt), count)
            self.assertLessEqual(count, 900, f"Slot #{s_id} prompt exceeds 900 characters: {count}")
            self.assertIn("character/aminsa_face_master_4k.png", prompt)

    def test_language_rules(self):
        cycle_date = "2026-11-23"
        s2 = self.packager.generate_slot_package(slot_id=2, cycle_date=cycle_date)
        s8 = self.packager.generate_slot_package(slot_id=8, cycle_date=cycle_date)
        s1 = self.packager.generate_slot_package(slot_id=1, cycle_date=cycle_date)

        self.assertEqual(s2["language"], "English")
        self.assertEqual(s8["language"], "English")
        self.assertEqual(s1["language"], "Hinglish")


if __name__ == "__main__":
    unittest.main()
