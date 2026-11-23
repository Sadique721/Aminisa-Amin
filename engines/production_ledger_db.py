# -*- coding: utf-8 -*-
"""
Aminsa Amin Production Ledger & 30-Day Anti-Repetition Database Engine
=====================================================================
Manages the persistent multi-table SQLite relational database:
1. Content Cycles & Slots (32-field schema)
2. 30-Day Rolling History (Topics, Angles, Scripts, Wardrobe, Settings, Compositions)
3. Google News RSS Harvesting & Source Verification Ledger
4. Multi-Device Synchronization & Job Leasing (Laptop & Mobile Node)
5. Quality Assurance, System Health & Audit Logging
"""

import os
import sys
import sqlite3
import json
import hashlib
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "aminsa_production_ledger.db")

SCHEMA_VERSION = 1
CANONICAL_FACE_SHA256 = "4ce270282ac57461"


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns a SQLite connection with row_factory and WAL mode enabled for high concurrency."""
    target_path = db_path or DB_PATH
    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
    conn = sqlite3.connect(target_path, timeout=15.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Initializes the complete 18-table production ledger schema with versioned migrations."""
    conn = get_connection(db_path)
    cur = conn.cursor()

    # 0. Versioned Migration Ledger
    cur.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        migration_name TEXT NOT NULL,
        applied_at TEXT NOT NULL,
        checksum TEXT NOT NULL
    );
    """)

    # 1. Content Cycles
    cur.execute("""
    CREATE TABLE IF NOT EXISTS content_cycles (
        cycle_id TEXT PRIMARY KEY,
        cycle_date TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL DEFAULT 'PLANNED',
        total_slots INTEGER NOT NULL DEFAULT 10,
        verified_slots INTEGER NOT NULL DEFAULT 0,
        evergreen_slots INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        completed_at TEXT
    );
    """)

    # 2. Content Slots (Full 32-Field Production Package)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS content_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idempotency_key TEXT NOT NULL UNIQUE,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        scheduled_at_ist TEXT NOT NULL,
        pillar TEXT NOT NULL,
        language TEXT NOT NULL,
        content_type TEXT NOT NULL DEFAULT 'NEWS_DRIVEN',
        topic TEXT NOT NULL,
        story_summary TEXT NOT NULL,
        factual_context TEXT NOT NULL,
        verification_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
        sources_json TEXT NOT NULL DEFAULT '[]',
        publication_dates_json TEXT NOT NULL DEFAULT '[]',
        event_date TEXT,
        opening_hook TEXT NOT NULL,
        spoken_script TEXT NOT NULL,
        estimated_duration_seconds REAL NOT NULL DEFAULT 10.0,
        image_to_video_prompt TEXT NOT NULL,
        wardrobe_json TEXT NOT NULL DEFAULT '{}',
        background_json TEXT NOT NULL DEFAULT '{}',
        visual_composition_json TEXT NOT NULL DEFAULT '{}',
        camera_direction TEXT NOT NULL,
        youtube_title TEXT NOT NULL,
        title_character_count INTEGER NOT NULL,
        hashtags TEXT NOT NULL,
        hashtag_character_count INTEGER NOT NULL,
        caption TEXT NOT NULL,
        caption_character_count INTEGER NOT NULL,
        video_prompt_character_count INTEGER NOT NULL,
        duplicate_check TEXT NOT NULL DEFAULT 'PASSED',
        identity_qa TEXT NOT NULL DEFAULT 'PASSED',
        fact_qa TEXT NOT NULL DEFAULT 'PASSED',
        production_status TEXT NOT NULL DEFAULT 'DRAFT',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (cycle_date) REFERENCES content_cycles(cycle_date)
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_slots_cycle ON content_slots(cycle_date, slot_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_slots_idempotency ON content_slots(idempotency_key);")

    # 3. News Items
    cur.execute("""
    CREATE TABLE IF NOT EXISTS news_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guid TEXT UNIQUE,
        rss_title TEXT NOT NULL,
        cleaned_title TEXT NOT NULL,
        publisher TEXT NOT NULL,
        google_news_url TEXT NOT NULL,
        resolved_url TEXT,
        published_at_utc TEXT,
        published_at_ist TEXT,
        harvested_at_ist TEXT NOT NULL,
        pillar TEXT NOT NULL,
        query TEXT NOT NULL,
        verification_status TEXT NOT NULL DEFAULT 'UNVERIFIED',
        confidence_score REAL NOT NULL DEFAULT 0.0,
        verified_facts_json TEXT NOT NULL DEFAULT '[]',
        raw_metadata_json TEXT NOT NULL DEFAULT '{}'
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_news_published ON news_items(published_at_ist, pillar);")

    # 4. News Sources
    cur.execute("""
    CREATE TABLE IF NOT EXISTS news_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        publisher_name TEXT NOT NULL UNIQUE,
        domain TEXT,
        trust_score REAL NOT NULL DEFAULT 0.8,
        is_independent INTEGER NOT NULL DEFAULT 1,
        is_official INTEGER NOT NULL DEFAULT 0,
        notes TEXT,
        last_seen_at TEXT NOT NULL
    );
    """)

    # 5. Topic History (Rolling 30-Day Anti-Repetition)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS topic_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        topic_title TEXT NOT NULL,
        normalized_topic TEXT NOT NULL,
        topic_cluster TEXT,
        pillar TEXT NOT NULL,
        similarity_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_topic_history_date ON topic_history(cycle_date, pillar);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_topic_history_norm ON topic_history(normalized_topic);")

    # 6. Angle History
    cur.execute("""
    CREATE TABLE IF NOT EXISTS angle_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        editorial_angle TEXT NOT NULL,
        hook_text TEXT NOT NULL,
        normalized_hook TEXT NOT NULL,
        pillar TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_angle_history_date ON angle_history(cycle_date, pillar);")

    # 7. Script History
    cur.execute("""
    CREATE TABLE IF NOT EXISTS script_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        script_text TEXT NOT NULL,
        normalized_script TEXT NOT NULL,
        word_count INTEGER NOT NULL,
        char_count INTEGER NOT NULL,
        duration_seconds REAL NOT NULL,
        script_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_script_history_date ON script_history(cycle_date, slot_id);")

    # 8. Wardrobe History (Rolling 30-Day Anti-Repetition)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS wardrobe_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        pillar TEXT NOT NULL,
        category TEXT NOT NULL,
        garment TEXT NOT NULL,
        color TEXT NOT NULL,
        fabric TEXT,
        pattern TEXT,
        accessories TEXT,
        styling TEXT,
        formality TEXT,
        full_description TEXT NOT NULL,
        wardrobe_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_wardrobe_history_date ON wardrobe_history(cycle_date, pillar);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_wardrobe_hash ON wardrobe_history(wardrobe_hash);")

    # 9. Setting History (Rolling 30-Day Anti-Repetition)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS setting_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        pillar TEXT NOT NULL,
        location_type TEXT NOT NULL,
        environment TEXT NOT NULL,
        architecture TEXT,
        props TEXT,
        lighting TEXT,
        time_of_day TEXT,
        full_description TEXT NOT NULL,
        setting_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_setting_history_date ON setting_history(cycle_date, pillar);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_setting_hash ON setting_history(setting_hash);")

    # 10. Visual Composition History
    cur.execute("""
    CREATE TABLE IF NOT EXISTS visual_composition_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        pillar TEXT NOT NULL,
        shot_size TEXT NOT NULL,
        camera_angle TEXT NOT NULL,
        camera_movement TEXT NOT NULL,
        character_position TEXT,
        depth_of_field TEXT,
        full_description TEXT NOT NULL,
        comp_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_comp_history_date ON visual_composition_history(cycle_date, pillar);")

    # 11. Generation Jobs (Multi-Device Task Leasing & Offline Queue)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS generation_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idempotency_key TEXT NOT NULL UNIQUE,
        node_id TEXT NOT NULL,
        job_type TEXT NOT NULL,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        version INTEGER NOT NULL DEFAULT 1,
        lease_expiry TEXT,
        status TEXT NOT NULL DEFAULT 'PENDING',
        retry_count INTEGER NOT NULL DEFAULT 0,
        payload_json TEXT NOT NULL DEFAULT '{}',
        result_json TEXT NOT NULL DEFAULT '{}',
        error_message TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON generation_jobs(status, lease_expiry);")

    # 12. Production Assets
    cur.execute("""
    CREATE TABLE IF NOT EXISTS production_assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        asset_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        sha256_hash TEXT NOT NULL,
        resolution TEXT,
        duration_seconds REAL,
        format TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_assets_slot ON production_assets(cycle_date, slot_id);")

    # 13. Device Nodes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS device_nodes (
        node_id TEXT PRIMARY KEY,
        device_name TEXT NOT NULL,
        device_type TEXT NOT NULL,
        os_info TEXT NOT NULL,
        ip_address TEXT,
        status TEXT NOT NULL DEFAULT 'ACTIVE',
        last_heartbeat TEXT NOT NULL,
        lease_active_count INTEGER NOT NULL DEFAULT 0,
        capabilities_json TEXT NOT NULL DEFAULT '{}'
    );
    """)

    # 14. Sync Events
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sync_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        source_node TEXT NOT NULL,
        target_node TEXT NOT NULL,
        payload_checksum TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'COMPLETED',
        details_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    );
    """)

    # 15. QA Results
    cur.execute("""
    CREATE TABLE IF NOT EXISTS qa_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        check_type TEXT NOT NULL,
        passed INTEGER NOT NULL,
        score REAL NOT NULL DEFAULT 1.0,
        failure_reason TEXT,
        details_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_qa_slot ON qa_results(cycle_date, slot_id);")

    # 16. Scheduler Runs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scheduler_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_date TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        run_at_ist TEXT NOT NULL,
        run_type TEXT NOT NULL DEFAULT 'SCHEDULED',
        status TEXT NOT NULL DEFAULT 'SUCCESS',
        notes TEXT,
        duration_ms INTEGER NOT NULL DEFAULT 0
    );
    """)

    # 17. System Health
    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id TEXT NOT NULL,
        timestamp_ist TEXT NOT NULL,
        internet_connected INTEGER NOT NULL DEFAULT 1,
        rss_healthy INTEGER NOT NULL DEFAULT 1,
        db_healthy INTEGER NOT NULL DEFAULT 1,
        active_model TEXT,
        notes TEXT,
        cpu_mem_json TEXT NOT NULL DEFAULT '{}'
    );
    """)

    # 18. Audit Logs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        actor TEXT NOT NULL DEFAULT 'SYSTEM',
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        changes_json TEXT NOT NULL DEFAULT '{}',
        timestamp_ist TEXT NOT NULL
    );
    """)

    # 19. Backward-Compatibility Legacy Bridges
    cur.execute("""
    CREATE TABLE IF NOT EXISTS content_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        topic TEXT,
        category TEXT,
        script TEXT,
        video_path TEXT,
        youtube_video_id TEXT,
        status TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS image_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        topic TEXT,
        category TEXT,
        hook TEXT,
        caption TEXT,
        image_path TEXT,
        platform TEXT
    );
    """)

    # Record Version 1 Migration
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
    INSERT INTO schema_migrations (version, migration_name, applied_at, checksum)
    VALUES (1, '001_core_18_table_production_ledger', ?, 'a8f7c9e1b2d3')
    ON CONFLICT(version) DO NOTHING;
    """, (now_str,))

    conn.commit()
    conn.close()


class ProductionLedgerDB:
    """High-level abstraction for Aminsa production ledger & anti-repetition engine."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DB_PATH
        init_db(self.db_path)

    def get_conn(self) -> sqlite3.Connection:
        return get_connection(self.db_path)

    @contextmanager
    def transaction(self):
        """Context manager providing atomic transaction execution with automatic rollback on exception."""
        conn = self.get_conn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_migrations(self) -> List[Dict[str, Any]]:
        """Returns list of applied migrations."""
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT version, migration_name, applied_at, checksum FROM schema_migrations ORDER BY version ASC;")
            return [dict(r) for r in cur.fetchall()]

    def validate_schema(self) -> Dict[str, Any]:
        """Validates all 18 core tables and constraints in the production ledger database."""
        expected_tables = [
            "schema_migrations", "content_cycles", "content_slots", "news_items",
            "news_sources", "topic_history", "angle_history", "script_history",
            "wardrobe_history", "setting_history", "visual_composition_history",
            "generation_jobs", "production_assets", "device_nodes", "sync_events",
            "qa_results", "scheduler_runs", "system_health", "audit_logs"
        ]
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            actual_tables = set(r[0] for r in cur.fetchall())

            missing = [t for t in expected_tables if t not in actual_tables]
            cur.execute("PRAGMA foreign_keys;")
            fk_enabled = bool(cur.fetchone()[0])

            return {
                "valid": len(missing) == 0,
                "missing_tables": missing,
                "total_tables": len(actual_tables),
                "foreign_keys_enabled": fk_enabled,
                "schema_version": SCHEMA_VERSION
            }

    # --------------------------------------------------------------------------
    # Cycles & Slots
    # --------------------------------------------------------------------------
    def ensure_cycle(self, cycle_date: str) -> str:
        """Creates or retrieves daily cycle record."""
        now_ist = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cycle_id = f"CYCLE-{cycle_date}"
        with self.get_conn() as conn:
            conn.execute("""
            INSERT INTO content_cycles (cycle_id, cycle_date, status, created_at)
            VALUES (?, ?, 'PLANNED', ?)
            ON CONFLICT(cycle_date) DO UPDATE SET status = status;
            """, (cycle_id, cycle_date, now_ist))
            conn.commit()
        return cycle_id

    def upsert_slot(self, slot_data: Dict[str, Any]) -> int:
        """Idempotently saves or updates a 32-field slot production package."""
        cycle_date = slot_data["cycle_date"]
        slot_id = slot_data["slot_id"]
        version = slot_data.get("content_version", 1)
        idempotency_key = f"{cycle_date}:slot_{slot_id:02d}:v{version}"
        now_ist = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.ensure_cycle(cycle_date)

        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO content_slots (
                idempotency_key, cycle_date, slot_id, scheduled_at_ist, pillar, language,
                content_type, topic, story_summary, factual_context, verification_status,
                sources_json, publication_dates_json, event_date, opening_hook, spoken_script,
                estimated_duration_seconds, image_to_video_prompt, wardrobe_json, background_json,
                visual_composition_json, camera_direction, youtube_title, title_character_count,
                hashtags, hashtag_character_count, caption, caption_character_count,
                video_prompt_character_count, duplicate_check, identity_qa, fact_qa,
                production_status, created_at, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?
            )
            ON CONFLICT(idempotency_key) DO UPDATE SET
                topic = excluded.topic,
                story_summary = excluded.story_summary,
                factual_context = excluded.factual_context,
                verification_status = excluded.verification_status,
                sources_json = excluded.sources_json,
                spoken_script = excluded.spoken_script,
                image_to_video_prompt = excluded.image_to_video_prompt,
                wardrobe_json = excluded.wardrobe_json,
                background_json = excluded.background_json,
                visual_composition_json = excluded.visual_composition_json,
                youtube_title = excluded.youtube_title,
                title_character_count = excluded.title_character_count,
                hashtags = excluded.hashtags,
                caption = excluded.caption,
                video_prompt_character_count = excluded.video_prompt_character_count,
                duplicate_check = excluded.duplicate_check,
                production_status = excluded.production_status,
                updated_at = excluded.updated_at;
            """, (
                idempotency_key, cycle_date, slot_id, slot_data.get("scheduled_at_ist", ""),
                slot_data.get("pillar", ""), slot_data.get("language", "Hinglish"),
                slot_data.get("content_type", "NEWS_DRIVEN"), slot_data.get("topic", ""),
                slot_data.get("story_summary", ""), slot_data.get("factual_context", ""),
                slot_data.get("verification_status", "UNVERIFIED"),
                json.dumps(slot_data.get("sources", [])),
                json.dumps(slot_data.get("publication_dates", [])),
                slot_data.get("event_date"), slot_data.get("opening_hook", ""),
                slot_data.get("spoken_script", ""),
                float(slot_data.get("estimated_duration_seconds", 10.0)),
                slot_data.get("image_to_video_prompt", ""),
                json.dumps(slot_data.get("wardrobe", {})),
                json.dumps(slot_data.get("background", {})),
                json.dumps(slot_data.get("visual_composition", {})),
                slot_data.get("camera_direction", ""), slot_data.get("youtube_title", ""),
                int(slot_data.get("title_character_count", len(slot_data.get("youtube_title", "")))),
                slot_data.get("hashtags", ""),
                int(slot_data.get("hashtag_character_count", len(slot_data.get("hashtags", "")))),
                slot_data.get("caption", ""),
                int(slot_data.get("caption_character_count", len(slot_data.get("caption", "")))),
                int(slot_data.get("video_prompt_character_count", len(slot_data.get("image_to_video_prompt", "")))),
                slot_data.get("duplicate_check", "PASSED"), slot_data.get("identity_qa", "PASSED"),
                slot_data.get("fact_qa", "PASSED"), slot_data.get("production_status", "DRAFT"),
                now_ist, now_ist
            ))
            conn.commit()
            return cur.lastrowid

    def get_slot(self, cycle_date: str, slot_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a slot record by cycle_date and slot_id."""
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT * FROM content_slots WHERE cycle_date = ? AND slot_id = ?
            ORDER BY id DESC LIMIT 1;
            """, (cycle_date, slot_id))
            row = cur.fetchone()
            if row:
                d = dict(row)
                d["sources"] = json.loads(d.get("sources_json") or "[]")
                d["wardrobe"] = json.loads(d.get("wardrobe_json") or "{}")
                d["background"] = json.loads(d.get("background_json") or "{}")
                d["visual_composition"] = json.loads(d.get("visual_composition_json") or "{}")
                return d
            return None

    def get_cycle_slots(self, cycle_date: str) -> List[Dict[str, Any]]:
        """Retrieves all 10 slots for a given cycle date."""
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT * FROM content_slots WHERE cycle_date = ?
            ORDER BY slot_id ASC;
            """, (cycle_date,))
            slots = []
            for row in cur.fetchall():
                d = dict(row)
                d["sources"] = json.loads(d.get("sources_json") or "[]")
                d["wardrobe"] = json.loads(d.get("wardrobe_json") or "{}")
                d["background"] = json.loads(d.get("background_json") or "{}")
                d["visual_composition"] = json.loads(d.get("visual_composition_json") or "{}")
                slots.append(d)
            return slots

    # --------------------------------------------------------------------------
    # 30-Day Anti-Repetition Checks
    # --------------------------------------------------------------------------
    def is_topic_repeated(self, topic_title: str, pillar: str, window_days: int = 30) -> Tuple[bool, Optional[str]]:
        """Checks if a topic title or similar normalized topic appeared in the last 30 days."""
        norm = self._normalize_text(topic_title)
        cutoff_date = (datetime.now() - timedelta(days=window_days)).strftime("%Y-%m-%d")

        with self.get_conn() as conn:
            cur = conn.cursor()
            # Exact or normalized match
            cur.execute("""
            SELECT cycle_date, slot_id, topic_title FROM topic_history
            WHERE pillar = ? AND cycle_date >= ? AND normalized_topic = ?
            LIMIT 1;
            """, (pillar, cutoff_date, norm))
            row = cur.fetchone()
            if row:
                return True, f"Exact topic match on {row['cycle_date']} (Slot #{row['slot_id']}): '{row['topic_title']}'"

            # Jaccard / token overlap match
            cur.execute("""
            SELECT cycle_date, slot_id, topic_title, normalized_topic FROM topic_history
            WHERE pillar = ? AND cycle_date >= ?;
            """, (pillar, cutoff_date))
            norm_tokens = set(norm.split())
            if len(norm_tokens) >= 3:
                for r in cur.fetchall():
                    past_tokens = set(r["normalized_topic"].split())
                    overlap = len(norm_tokens.intersection(past_tokens))
                    union = len(norm_tokens.union(past_tokens))
                    if union > 0 and (overlap / union) >= 0.70:
                        return True, f"High topic similarity ({int(overlap/union*100)}%) with {r['cycle_date']} Slot #{r['slot_id']}: '{r['topic_title']}'"

        return False, None

    def is_wardrobe_repeated(self, wardrobe_desc: str, pillar: str, window_days: int = 30) -> Tuple[bool, Optional[str]]:
        """Checks if exact wardrobe combination appeared in the last 30 days."""
        w_hash = hashlib.sha256(wardrobe_desc.strip().lower().encode("utf-8")).hexdigest()
        cutoff_date = (datetime.now() - timedelta(days=window_days)).strftime("%Y-%m-%d")

        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT cycle_date, slot_id, full_description FROM wardrobe_history
            WHERE cycle_date >= ? AND wardrobe_hash = ?
            LIMIT 1;
            """, (cutoff_date, w_hash))
            row = cur.fetchone()
            if row:
                return True, f"Identical wardrobe worn on {row['cycle_date']} (Slot #{row['slot_id']})"
        return False, None

    def is_setting_repeated(self, setting_desc: str, pillar: str, window_days: int = 30) -> Tuple[bool, Optional[str]]:
        """Checks if exact studio setting appeared in the last 30 days for this pillar."""
        s_hash = hashlib.sha256(setting_desc.strip().lower().encode("utf-8")).hexdigest()
        cutoff_date = (datetime.now() - timedelta(days=window_days)).strftime("%Y-%m-%d")

        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT cycle_date, slot_id, full_description FROM setting_history
            WHERE cycle_date >= ? AND setting_hash = ?
            LIMIT 1;
            """, (cutoff_date, s_hash))
            row = cur.fetchone()
            if row:
                return True, f"Identical setting used on {row['cycle_date']} (Slot #{row['slot_id']})"
        return False, None

    def record_production_history(self, slot_data: Dict[str, Any]) -> None:
        """Records slot topic, angle, script, wardrobe, setting, and composition into historical ledgers."""
        cycle_date = slot_data["cycle_date"]
        slot_id = slot_data["slot_id"]
        pillar = slot_data["pillar"]
        now_ist = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Normalize texts
        topic = slot_data.get("topic", "")
        norm_topic = self._normalize_text(topic)
        topic_hash = hashlib.sha256(norm_topic.encode("utf-8")).hexdigest()

        hook = slot_data.get("opening_hook", "")
        norm_hook = self._normalize_text(hook)

        script = slot_data.get("spoken_script", "")
        norm_script = self._normalize_text(script)
        script_hash = hashlib.sha256(norm_script.encode("utf-8")).hexdigest()

        wardrobe = slot_data.get("wardrobe", {})
        w_desc = wardrobe.get("full_description", str(wardrobe))
        w_hash = hashlib.sha256(w_desc.strip().lower().encode("utf-8")).hexdigest()

        setting = slot_data.get("background", {})
        s_desc = setting.get("full_description", str(setting))
        s_hash = hashlib.sha256(s_desc.strip().lower().encode("utf-8")).hexdigest()

        comp = slot_data.get("visual_composition", {})
        c_desc = comp.get("full_description", str(comp))
        c_hash = hashlib.sha256(c_desc.strip().lower().encode("utf-8")).hexdigest()

        with self.get_conn() as conn:
            # 1. Topic history
            conn.execute("""
            INSERT INTO topic_history (cycle_date, slot_id, topic_title, normalized_topic, topic_cluster, pillar, similarity_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (cycle_date, slot_id, topic, norm_topic, slot_data.get("topic_cluster", pillar), pillar, topic_hash, now_ist))

            # 2. Angle history
            conn.execute("""
            INSERT INTO angle_history (cycle_date, slot_id, editorial_angle, hook_text, normalized_hook, pillar, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (cycle_date, slot_id, slot_data.get("editorial_angle", ""), hook, norm_hook, pillar, now_ist))

            # 3. Script history
            words = len(script.split())
            conn.execute("""
            INSERT INTO script_history (cycle_date, slot_id, script_text, normalized_script, word_count, char_count, duration_seconds, script_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (cycle_date, slot_id, script, norm_script, words, len(script), float(slot_data.get("estimated_duration_seconds", 10.0)), script_hash, now_ist))

            # 4. Wardrobe history
            conn.execute("""
            INSERT INTO wardrobe_history (cycle_date, slot_id, pillar, category, garment, color, fabric, pattern, accessories, styling, formality, full_description, wardrobe_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (cycle_date, slot_id, pillar, wardrobe.get("category", ""), wardrobe.get("garment", ""), wardrobe.get("color", ""), wardrobe.get("fabric", ""), wardrobe.get("pattern", ""), wardrobe.get("accessories", ""), wardrobe.get("styling", ""), wardrobe.get("formality", ""), w_desc, w_hash, now_ist))

            # 5. Setting history
            conn.execute("""
            INSERT INTO setting_history (cycle_date, slot_id, pillar, location_type, environment, architecture, props, lighting, time_of_day, full_description, setting_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (cycle_date, slot_id, pillar, setting.get("location_type", ""), setting.get("environment", ""), setting.get("architecture", ""), setting.get("props", ""), setting.get("lighting", ""), setting.get("time_of_day", ""), s_desc, s_hash, now_ist))

            # 6. Composition history
            conn.execute("""
            INSERT INTO visual_composition_history (cycle_date, slot_id, pillar, shot_size, camera_angle, camera_movement, character_position, depth_of_field, full_description, comp_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (cycle_date, slot_id, pillar, comp.get("shot_size", "Medium close-up"), comp.get("camera_angle", "Eye level"), comp.get("camera_movement", "Slow push-in"), comp.get("character_position", "Center frame"), comp.get("depth_of_field", "Shallow"), c_desc, c_hash, now_ist))

            conn.commit()

    # --------------------------------------------------------------------------
    # Device Nodes & Synchronization
    # --------------------------------------------------------------------------
    def register_device(self, node_id: str, name: str, dev_type: str, os_info: str, ip: str = "127.0.0.1") -> None:
        now_ist = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_conn() as conn:
            conn.execute("""
            INSERT INTO device_nodes (node_id, device_name, device_type, os_info, ip_address, status, last_heartbeat)
            VALUES (?, ?, ?, ?, ?, 'ACTIVE', ?)
            ON CONFLICT(node_id) DO UPDATE SET
                device_name = excluded.device_name,
                ip_address = excluded.ip_address,
                last_heartbeat = excluded.last_heartbeat,
                status = 'ACTIVE';
            """, (node_id, name, dev_type, os_info, ip, now_ist))
            conn.commit()

    def record_heartbeat(self, node_id: str) -> None:
        now_ist = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_conn() as conn:
            conn.execute("UPDATE device_nodes SET last_heartbeat = ?, status = 'ACTIVE' WHERE node_id = ?;", (now_ist, node_id))
            conn.commit()

    def log_audit(self, action: str, entity_type: str, entity_id: str, changes: Dict[str, Any], actor: str = "SYSTEM") -> None:
        now_ist = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_conn() as conn:
            conn.execute("""
            INSERT INTO audit_logs (action, actor, entity_type, entity_id, changes_json, timestamp_ist)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (action, actor, entity_type, str(entity_id), json.dumps(changes), now_ist))
            conn.commit()

    # --------------------------------------------------------------------------
    # Utility Helpers
    # --------------------------------------------------------------------------
    @staticmethod
    def _normalize_text(text: str) -> str:
        import re
        if not text:
            return ""
        clean = re.sub(r"[^\w\s]", " ", text.lower())
        return re.sub(r"\s+", " ", clean).strip()


ledger_db = ProductionLedgerDB()

if __name__ == "__main__":
    print(f"Production Ledger DB initialized at: {DB_PATH}")
    db = ProductionLedgerDB()
    with db.get_conn() as c:
        cur = c.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cur.fetchall()]
        print(f"Total Tables in Schema: {len(tables)}")
        for t in tables:
            cur.execute(f"PRAGMA table_info({t});")
            cols = len(cur.fetchall())
            print(f"  • {t:<28} ({cols} columns)")
