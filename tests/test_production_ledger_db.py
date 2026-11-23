# -*- coding: utf-8 -*-
"""
Unit Tests for Phase 1: Aminsa Production Ledger & 30-Day Anti-Repetition DB
============================================================================
Validates all Phase 1 strict implementation conditions:
1. Fresh database initialization & schema migrations
2. Repeated (idempotent) initialization
3. Duplicate idempotency key rejection
4. Foreign-key validation
5. Transaction rollback handling
6. Historical data retention (permanent storage, no destructive pruning)
7. 30-day rolling comparison window queries
8. Restart and recovery consistency
"""

import os
import sys
import sqlite3
import unittest
import tempfile
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.production_ledger_db import ProductionLedgerDB, init_db, SCHEMA_VERSION


class TestProductionLedgerDB(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_file.close()
        self.db = ProductionLedgerDB(db_path=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

    def test_01_fresh_database_initialization(self):
        """Verifies fresh initialization creates all tables and applies migration v1."""
        validation = self.db.validate_schema()
        self.assertTrue(validation["valid"], f"Missing tables: {validation.get('missing_tables')}")
        self.assertGreaterEqual(validation["total_tables"], 18)
        self.assertTrue(validation["foreign_keys_enabled"])

        # Verify schema migration v1 recorded
        migrations = self.db.get_migrations()
        self.assertEqual(len(migrations), 1)
        self.assertEqual(migrations[0]["version"], 1)
        self.assertEqual(migrations[0]["migration_name"], "001_core_18_table_production_ledger")

    def test_02_repeated_initialization(self):
        """Verifies repeated init_db calls are safe, idempotent, and cause no corruption."""
        init_db(self.temp_file.name)
        init_db(self.temp_file.name)

        validation = self.db.validate_schema()
        self.assertTrue(validation["valid"])
        migrations = self.db.get_migrations()
        self.assertEqual(len(migrations), 1, "Migrations must not duplicate on repeated init")

    def test_03_duplicate_idempotency_key_rejection(self):
        """Verifies duplicate idempotency keys raise sqlite3.IntegrityError on direct insert."""
        cycle_date = "2026-11-23"
        self.db.ensure_cycle(cycle_date)
        key = "2026-11-23:slot_01:v1"

        slot_data = {
            "cycle_date": cycle_date,
            "slot_id": 1,
            "content_version": 1,
            "scheduled_at_ist": "08:00 AM",
            "pillar": "Tech",
            "language": "English",
            "topic": "AI Breakthrough",
            "story_summary": "Summary",
            "factual_context": "Facts",
            "opening_hook": "Hook",
            "spoken_script": "Script",
            "image_to_video_prompt": "Prompt",
            "camera_direction": "Slow push-in",
            "youtube_title": "AI Breakthrough #Aminsa #Shorts #Tech",
            "caption": "Caption"
        }
        self.db.upsert_slot(slot_data)

        # Attempt raw duplicate insert with exact same idempotency_key without ON CONFLICT
        with self.db.get_conn() as conn:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("""
                INSERT INTO content_slots (
                    idempotency_key, cycle_date, slot_id, scheduled_at_ist, pillar, language,
                    topic, story_summary, factual_context, opening_hook, spoken_script,
                    image_to_video_prompt, camera_direction, youtube_title, caption
                ) VALUES (?, ?, 1, '08:00 AM', 'Tech', 'English', 'Duplicate Entry', 'Summary 2', 'Facts 2', 'Hook 2', 'Script 2', 'Prompt 2', 'Push', 'Title 2', 'Caption 2');
                """, (key, cycle_date))

    def test_04_foreign_key_validation(self):
        """Verifies SQLite foreign key constraints are enabled."""
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys;")
            fk_status = cur.fetchone()[0]
            self.assertEqual(fk_status, 1, "Foreign keys must be actively enabled")

    def test_05_transaction_rollback(self):
        """Verifies transaction rollback ensures no partial writes survive exceptions."""
        try:
            with self.db.transaction() as conn:
                conn.execute("""
                INSERT INTO audit_logs (action, actor, entity_type, entity_id, changes_json, timestamp_ist)
                VALUES ('TEST_ROLLBACK', 'TEST_RUNNER', 'slot', 'test_key', '{}', '2026-11-23 12:00:00');
                """)
                # Force failure mid-transaction
                raise RuntimeError("Simulated transaction fault")
        except RuntimeError:
            pass

        # Verify row was NOT written due to rollback
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM audit_logs WHERE action = 'TEST_ROLLBACK';")
            count = cur.fetchone()[0]
            self.assertEqual(count, 0, "Failed transaction must roll back completely")

    def test_06_historical_data_retention(self):
        """Verifies data older than 30 days is permanently retained, not deleted."""
        old_cycle = "2026-08-15"  # ~100 days in the past
        now_cycle = "2026-11-23"

        self.db.ensure_cycle(old_cycle)
        self.db.ensure_cycle(now_cycle)

        # Record history in the past
        slot_data_old = {
            "cycle_date": old_cycle,
            "slot_id": 1,
            "pillar": "India National / Morning Brief",
            "topic": "Historic Independence Day Celebrations Across India",
            "opening_hook": "Desh 80th Independence Day dhoom-dhaam se mana raha hai!",
            "spoken_script": "Hello everyone! Main hoon Aminsa. Desh ke 80th Independence Day par shubhkaamnayein.",
            "estimated_duration_seconds": 10.0,
            "wardrobe": {"full_description": "Tricolor khadi saree with gold border"},
            "background": {"full_description": "Red Fort New Delhi background softly blurred"},
            "visual_composition": {"full_description": "Centered medium portrait"}
        }
        self.db.record_production_history(slot_data_old)

        # Verify old record still exists permanently in historical tables
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM topic_history WHERE cycle_date = ?;", (old_cycle,))
            count = cur.fetchone()[0]
            self.assertEqual(count, 1, "Historical records older than 30 days must be preserved permanently")

    def test_07_30_day_rolling_window_queries(self):
        """Verifies 30-day window checks detect recency without deleting old data."""
        pillar = "Global & Indian Technology / AI"
        today = datetime.now()

        # Topic A: 10 days ago (within 30-day window)
        date_10d_ago = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        slot_data_recent = {
            "cycle_date": date_10d_ago,
            "slot_id": 2,
            "pillar": pillar,
            "topic": "OpenAI Unveils Autonomous Multimodal Web Agent",
            "opening_hook": "AI agents just gained autonomous web navigation capabilities!",
            "spoken_script": "Hello everyone! Today's AI milestone: new web agents capable of complete task workflows.",
            "estimated_duration_seconds": 10.0,
            "wardrobe": {"full_description": "Charcoal modern blazer"},
            "background": {"full_description": "Futuristic glass research lab"},
            "visual_composition": {"full_description": "Medium close-up"}
        }
        self.db.record_production_history(slot_data_recent)

        # Topic B: 45 days ago (outside 30-day window)
        date_45d_ago = (today - timedelta(days=45)).strftime("%Y-%m-%d")
        slot_data_older = {
            "cycle_date": date_45d_ago,
            "slot_id": 3,
            "pillar": pillar,
            "topic": "Early Prototype Breakthrough in Quantum Entanglement",
            "opening_hook": "Quantum researchers achieve 99% qubit fidelity!",
            "spoken_script": "Hello everyone! A huge quantum computing milestone achieved.",
            "estimated_duration_seconds": 10.0,
            "wardrobe": {"full_description": "Midnight navy suit"},
            "background": {"full_description": "Cryogenic physics laboratory"},
            "visual_composition": {"full_description": "Profile angle push-in"}
        }
        self.db.record_production_history(slot_data_older)

        # 1. Recent topic within 30 days must be detected as repeated
        is_rep_recent, reason = self.db.is_topic_repeated(
            "OpenAI Unveils Autonomous Multimodal Web Agent",
            pillar=pillar,
            window_days=30
        )
        self.assertTrue(is_rep_recent, "Topic from 10 days ago must be flagged as repeated")

        # 2. Topic from 45 days ago must NOT be blocked by 30-day rolling window
        is_rep_older, reason_old = self.db.is_topic_repeated(
            "Early Prototype Breakthrough in Quantum Entanglement",
            pillar=pillar,
            window_days=30
        )
        self.assertFalse(is_rep_older, "Topic from 45 days ago must be allowed by 30-day rolling window")

        # 3. Both topics still exist in database
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM topic_history;")
            total_history = cur.fetchone()[0]
            self.assertEqual(total_history, 2, "Both records must persist in database without deletion")

    def test_08_restart_and_recovery_consistency(self):
        """Verifies state is completely preserved across connection closures and re-initialization."""
        cycle_date = "2026-11-23"
        self.db.ensure_cycle(cycle_date)
        slot_data = {
            "cycle_date": cycle_date,
            "slot_id": 1,
            "content_version": 1,
            "scheduled_at_ist": "08:00 AM",
            "pillar": "India National / Morning Brief",
            "language": "Hinglish",
            "content_type": "NEWS_DRIVEN",
            "topic": "Skyroot Aerospace Mission Update",
            "story_summary": "Summary",
            "factual_context": "Facts",
            "verification_status": "CONFIRMED",
            "sources": ["https://news.google.com/test"],
            "opening_hook": "Hook",
            "spoken_script": "Hello everyone! Main hoon Aminsa.",
            "estimated_duration_seconds": 10.0,
            "image_to_video_prompt": "Prompt",
            "youtube_title": "Skyroot Aerospace Mission Update #Aminsa #Shorts #Space",
            "production_status": "DRAFT"
        }
        self.db.upsert_slot(slot_data)

        # Simulate full service restart / disconnect by creating brand new instance on same file
        restarted_db = ProductionLedgerDB(db_path=self.temp_file.name)
        recovered_slot = restarted_db.get_slot(cycle_date, 1)

        self.assertIsNotNone(recovered_slot)
        self.assertEqual(recovered_slot["topic"], "Skyroot Aerospace Mission Update")
        self.assertEqual(recovered_slot["production_status"], "DRAFT")
        self.assertEqual(recovered_slot["verification_status"], "CONFIRMED")


if __name__ == "__main__":
    unittest.main()
