# -*- coding: utf-8 -*-
"""
Unit Tests for Phase 1: Aminsa Production Ledger & 30-Day Anti-Repetition DB
"""

import os
import sys
import unittest
import tempfile
from datetime import datetime

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.production_ledger_db import ProductionLedgerDB


class TestProductionLedgerDB(unittest.TestCase):

    def setUp(self):
        # Create a temporary database for test isolation
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_file.close()
        self.db = ProductionLedgerDB(db_path=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

    def test_cycle_and_slot_upsert(self):
        cycle_date = "2026-11-23"
        cycle_id = self.db.ensure_cycle(cycle_date)
        self.assertEqual(cycle_id, "CYCLE-2026-11-23")

        slot_data = {
            "cycle_date": cycle_date,
            "slot_id": 1,
            "content_version": 1,
            "scheduled_at_ist": "08:00 AM",
            "pillar": "India National / Morning Brief",
            "language": "Hinglish",
            "content_type": "NEWS_DRIVEN",
            "topic": "India Space Startup Skyroot Unveils Orbital Mission Roadmap",
            "story_summary": "Skyroot Aerospace announces final stage testing of orbital booster.",
            "factual_context": "Confirmed by ISRO-INSPACe authorization and official release.",
            "verification_status": "CONFIRMED",
            "sources": ["https://news.google.com/test", "https://isro.gov.in/test"],
            "publication_dates": ["2026-11-23T06:00:00Z"],
            "event_date": "2026-11-23",
            "opening_hook": "Skyroot ka orbital booster launch ke liye poori tarah ready hai!",
            "spoken_script": "Hello everyone! Main hoon Aminsa. Desh ke private space sector ke liye aaj ek aitihasik din hai.",
            "estimated_duration_seconds": 9.5,
            "image_to_video_prompt": "Aminsa speaking confidently to camera discussing Skyroot orbital mission.",
            "wardrobe": {
                "category": "Formal",
                "garment": "ivory khadi kurti",
                "color": "ivory",
                "full_description": "Graceful ivory khadi short kurti with subtle tricolor thread border"
            },
            "background": {
                "location_type": "Studio",
                "environment": "Sandstone courtyard",
                "full_description": "Sunlit architectural Indian sandstone courtyard softly blurred"
            },
            "visual_composition": {
                "shot_size": "Medium close-up",
                "camera_angle": "Eye level",
                "full_description": "Medium close-up eye level portrait centered in frame"
            },
            "camera_direction": "Slow push-in on key announcement",
            "youtube_title": "Skyroot Orbital Booster Ready For Launch #Aminsa #Shorts #Space",
            "title_character_count": 63,
            "hashtags": "#Aminsa #Shorts #Space #ISRO",
            "hashtag_character_count": 29,
            "caption": "India's private space revolution takes another massive leap forward with Skyroot.",
            "caption_character_count": 80,
            "video_prompt_character_count": 72,
            "duplicate_check": "PASSED",
            "identity_qa": "PASSED",
            "fact_qa": "PASSED",
            "production_status": "DRAFT"
        }

        # 1. First insert
        self.db.upsert_slot(slot_data)
        retrieved = self.db.get_slot(cycle_date, 1)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["topic"], slot_data["topic"])
        self.assertEqual(retrieved["verification_status"], "CONFIRMED")
        self.assertEqual(len(retrieved["sources"]), 2)

        # 2. Idempotent update (same key)
        slot_data["verification_status"] = "VERIFIED_CONFIRMED"
        self.db.upsert_slot(slot_data)
        updated = self.db.get_slot(cycle_date, 1)
        self.assertEqual(updated["verification_status"], "VERIFIED_CONFIRMED")

        # Ensure no duplicate slot was created
        all_slots = self.db.get_cycle_slots(cycle_date)
        self.assertEqual(len(all_slots), 1)

    def test_30_day_anti_repetition_engine(self):
        cycle_date = "2026-11-23"
        slot_data = {
            "cycle_date": cycle_date,
            "slot_id": 2,
            "pillar": "Global & Indian Technology / AI",
            "topic": "Google DeepMind Announces Gemini 3.0 Breakthrough",
            "opening_hook": "AI models just took a massive leap in multi-agent reasoning!",
            "spoken_script": "Hello everyone! I'm Aminsa. Today's top tech breakthrough comes from deep reasoning research.",
            "estimated_duration_seconds": 10.0,
            "wardrobe": {
                "category": "Tech Chic",
                "garment": "navy blazer",
                "color": "navy",
                "full_description": "Crisp tailored midnight-navy blazer over a pristine white silk shell top"
            },
            "background": {
                "location_type": "Tech Studio",
                "environment": "Glass AI Lab",
                "full_description": "Cutting-edge AI research studio with glass transparent data monitors"
            },
            "visual_composition": {
                "shot_size": "Medium shot",
                "full_description": "Crisp centered framing with glowing code monitors in background"
            }
        }

        # Record history
        self.db.record_production_history(slot_data)

        # Test exact topic repetition
        is_rep, reason = self.db.is_topic_repeated(
            "Google DeepMind Announces Gemini 3.0 Breakthrough",
            pillar="Global & Indian Technology / AI",
            window_days=30
        )
        self.assertTrue(is_rep)
        self.assertIn("Exact topic match", reason)

        # Test similar topic repetition (fuzzy overlap)
        is_rep2, reason2 = self.db.is_topic_repeated(
            "Google DeepMind Announces Gemini 3.0 Breakthrough In Reasoning",
            pillar="Global & Indian Technology / AI",
            window_days=30
        )
        self.assertTrue(is_rep2)
        self.assertIn("similarity", reason2.lower())

        # Test distinct topic (no repetition)
        is_rep3, reason3 = self.db.is_topic_repeated(
            "Quantum Supercomputing Milestone Achieved in Bengaluru",
            pillar="Global & Indian Technology / AI",
            window_days=30
        )
        self.assertFalse(is_rep3)

        # Test wardrobe repetition
        is_w_rep, w_reason = self.db.is_wardrobe_repeated(
            "Crisp tailored midnight-navy blazer over a pristine white silk shell top",
            pillar="Global & Indian Technology / AI",
            window_days=30
        )
        self.assertTrue(is_w_rep)
        self.assertIn("Identical wardrobe worn", w_reason)

        # Test distinct wardrobe
        is_w_rep2, _ = self.db.is_wardrobe_repeated(
            "Vibrant mustard chanderi kurta with silver accents",
            pillar="Global & Indian Technology / AI",
            window_days=30
        )
        self.assertFalse(is_w_rep2)

    def test_device_node_and_audit_logging(self):
        self.db.register_device(
            node_id="laptop-win11-master",
            name="Laptop Master Orchestrator",
            dev_type="LAPTOP",
            os_info="Windows 11 Pro"
        )
        self.db.record_heartbeat("laptop-win11-master")

        # Test audit log
        self.db.log_audit(
            action="SLOT_GENERATED",
            entity_type="content_slot",
            entity_id="2026-11-23:slot_01:v1",
            changes={"status": "DRAFT", "pillar": "India National / Morning Brief"}
        )

        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT status FROM device_nodes WHERE node_id = 'laptop-win11-master';")
            status = cur.fetchone()[0]
            self.assertEqual(status, "ACTIVE")

            cur.execute("SELECT COUNT(*) FROM audit_logs;")
            count = cur.fetchone()[0]
            self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
