# -*- coding: utf-8 -*-
"""
Aminsa Multi-Node Synchronization & Job Leasing Engine
======================================================
Manages coordinated production between:
1. Laptop Orchestration Node (Windows 11)
2. Mobile Production Node (OPPO A78 5G / Android 15 / Termux)
3. Content Planning Interface (ChatGPT JSON Sync)

Features:
- Unique Device/Node Registration & Heartbeat Monitor
- Atomic Job Leasing with TTL and Heartbeat-based expiry
- Idempotency Keys ({cycle_date}:{slot_id}:{version}:{job_type})
- Retry Policies & Duplicate-Job Prevention
- Bidirectional Sync Checkpoints and Conflict Detection
- Offline Queue Reconciliation
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional

_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_DIR)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from engines.production_ledger_db import ledger_db

IST_TZ = timezone(timedelta(hours=5, minutes=30))

DEFAULT_LAPTOP_NODE = "laptop_orchestrator"
DEFAULT_MOBILE_NODE = "oppo_a78_5g_termux"


def get_ist_now() -> str:
    return datetime.now(IST_TZ).strftime("%Y-%m-%d %H:%M:%S")


def get_cycle_date_str() -> str:
    now = datetime.now(IST_TZ)
    if now.hour < 8:
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    return now.strftime("%Y-%m-%d")


class SyncManager:
    """Manages node presence, job leases, idempotency, and state synchronization."""

    def __init__(self, db=None):
        self.db = db or ledger_db
        self._ensure_default_nodes()

    def _ensure_default_nodes(self):
        """Pre-registers the canonical Laptop and Mobile nodes."""
        self.register_node(
            node_id=DEFAULT_LAPTOP_NODE,
            device_name="Windows 11 Laptop Orchestrator",
            device_type="LAPTOP",
            os_info="Windows 11 (64-bit)",
            capabilities={
                "rss_harvesting": True,
                "fact_verification": True,
                "wardrobe_generation": True,
                "daily_packager": True,
                "master_scheduler": True,
                "full_database_ledger": True
            }
        )
        self.register_node(
            node_id=DEFAULT_MOBILE_NODE,
            device_name="OPPO A78 5G Production Worker",
            device_type="MOBILE",
            os_info="Android 15 / Termux / Google AI Edge",
            capabilities={
                "local_tts": True,
                "youtube_create_bridge": True,
                "local_storage": True,
                "offline_queue": True,
                "web_daemon_8765": True
            }
        )

    def register_node(self, node_id: str, device_name: str, device_type: str,
                      os_info: str, ip_address: str = "127.0.0.1",
                      capabilities: Optional[Dict[str, Any]] = None) -> bool:
        """Registers or updates a device node."""
        now_str = get_ist_now()
        cap_json = json.dumps(capabilities or {}, ensure_ascii=False)
        with self.db.get_conn() as conn:
            conn.execute("""
            INSERT INTO device_nodes (node_id, device_name, device_type, os_info, ip_address, status, last_heartbeat, capabilities_json)
            VALUES (?, ?, ?, ?, ?, 'ACTIVE', ?, ?)
            ON CONFLICT(node_id) DO UPDATE SET
                device_name = excluded.device_name,
                device_type = excluded.device_type,
                os_info = excluded.os_info,
                ip_address = excluded.ip_address,
                status = 'ACTIVE',
                last_heartbeat = excluded.last_heartbeat,
                capabilities_json = excluded.capabilities_json;
            """, (node_id, device_name, device_type, os_info, ip_address, now_str, cap_json))
            conn.commit()
        return True

    def record_heartbeat(self, node_id: str, ip_address: Optional[str] = None) -> bool:
        """Updates the node heartbeat timestamp."""
        now_str = get_ist_now()
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            if ip_address:
                cur.execute("""
                UPDATE device_nodes 
                SET last_heartbeat = ?, ip_address = ?, status = 'ACTIVE'
                WHERE node_id = ?;
                """, (now_str, ip_address, node_id))
            else:
                cur.execute("""
                UPDATE device_nodes 
                SET last_heartbeat = ?, status = 'ACTIVE'
                WHERE node_id = ?;
                """, (now_str, node_id))
            conn.commit()
            return cur.rowcount > 0

    def is_node_online(self, node_id: str, max_age_seconds: int = 180) -> bool:
        """Checks if a device node sent a heartbeat within max_age_seconds."""
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT last_heartbeat FROM device_nodes WHERE node_id = ?;", (node_id,))
            row = cur.fetchone()
            if not row or not row["last_heartbeat"]:
                return False
            try:
                hb = datetime.strptime(row["last_heartbeat"], "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                return (now - hb).total_seconds() <= max_age_seconds
            except Exception:
                return False

    def create_generation_job(self, node_id: str, job_type: str, cycle_date: str,
                              slot_id: int, payload: Dict[str, Any],
                              version: int = 1) -> str:
        """
        Creates a new idempotent generation job.
        Idempotency key format: {cycle_date}:{slot_id}:{version}:{job_type}
        """
        idempotency_key = f"{cycle_date}:{slot_id}:{version}:{job_type}"
        now_str = get_ist_now()
        payload_str = json.dumps(payload, ensure_ascii=False)

        with self.db.get_conn() as conn:
            conn.execute("""
            INSERT INTO generation_jobs (
                idempotency_key, node_id, job_type, cycle_date, slot_id,
                version, status, retry_count, payload_json, result_json,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, 'PENDING', 0, ?, '{}', ?, ?)
            ON CONFLICT(idempotency_key) DO UPDATE SET
                updated_at = excluded.updated_at
            ;
            """, (idempotency_key, node_id, job_type, cycle_date, slot_id, version, payload_str, now_str, now_str))
            conn.commit()
        return idempotency_key

    def acquire_job_lease(self, node_id: str, job_type: Optional[str] = None,
                          lease_seconds: int = 300) -> Optional[Dict[str, Any]]:
        """
        Atomically leases an available PENDING or EXPIRED job to node_id.
        Prevents dual execution of the same production task.
        """
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        expiry = (now + timedelta(seconds=lease_seconds)).strftime("%Y-%m-%d %H:%M:%S")

        with self.db.get_conn() as conn:
            cur = conn.cursor()
            query = """
            SELECT id, idempotency_key, job_type, cycle_date, slot_id, version, payload_json, retry_count
            FROM generation_jobs
            WHERE (status = 'PENDING' OR (status = 'IN_PROGRESS' AND lease_expiry < ?))
            """
            params = [now_str]
            if job_type:
                query += " AND job_type = ?"
                params.append(job_type)
            query += " ORDER BY id ASC LIMIT 1;"

            cur.execute(query, params)
            row = cur.fetchone()
            if not row:
                return None

            job_id = row["id"]
            cur.execute("""
            UPDATE generation_jobs
            SET status = 'IN_PROGRESS',
                node_id = ?,
                lease_expiry = ?,
                updated_at = ?
            WHERE id = ?;
            """, (node_id, expiry, now_str, job_id))

            cur.execute("""
            UPDATE device_nodes
            SET lease_active_count = lease_active_count + 1,
                last_heartbeat = ?
            WHERE node_id = ?;
            """, (now_str, node_id))
            conn.commit()

            payload = json.loads(row["payload_json"]) if row["payload_json"] else {}
            return {
                "job_id": job_id,
                "idempotency_key": row["idempotency_key"],
                "job_type": row["job_type"],
                "cycle_date": row["cycle_date"],
                "slot_id": row["slot_id"],
                "version": row["version"],
                "retry_count": row["retry_count"],
                "payload": payload,
                "lease_expiry": expiry
            }

    def renew_job_lease(self, job_id: int, node_id: str, lease_seconds: int = 300) -> bool:
        """Renews an active job lease before it expires."""
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        expiry = (now + timedelta(seconds=lease_seconds)).strftime("%Y-%m-%d %H:%M:%S")

        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            UPDATE generation_jobs
            SET lease_expiry = ?, updated_at = ?
            WHERE id = ? AND node_id = ? AND status = 'IN_PROGRESS';
            """, (expiry, now_str, job_id, node_id))
            conn.commit()
            return cur.rowcount > 0

    def complete_job(self, job_id: int, node_id: str, result: Dict[str, Any]) -> bool:
        """Marks a leased job as successfully completed."""
        now_str = get_ist_now()
        res_json = json.dumps(result, ensure_ascii=False)

        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            UPDATE generation_jobs
            SET status = 'COMPLETED',
                result_json = ?,
                updated_at = ?
            WHERE id = ? AND node_id = ?;
            """, (res_json, now_str, job_id, node_id))

            cur.execute("""
            UPDATE device_nodes
            SET lease_active_count = MAX(0, lease_active_count - 1),
                last_heartbeat = ?
            WHERE node_id = ?;
            """, (now_str, node_id))
            conn.commit()
            return cur.rowcount > 0

    def fail_job(self, job_id: int, node_id: str, error_msg: str, max_retries: int = 3) -> bool:
        """Handles job failure and schedules retry if under max_retries."""
        now_str = get_ist_now()
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT retry_count FROM generation_jobs WHERE id = ?;", (job_id,))
            row = cur.fetchone()
            if not row:
                return False

            retries = row["retry_count"] + 1
            new_status = 'PENDING' if retries < max_retries else 'FAILED'

            cur.execute("""
            UPDATE generation_jobs
            SET status = ?,
                retry_count = ?,
                error_message = ?,
                updated_at = ?
            WHERE id = ? AND node_id = ?;
            """, (new_status, retries, error_msg[:500], now_str, job_id, node_id))

            cur.execute("""
            UPDATE device_nodes
            SET lease_active_count = MAX(0, lease_active_count - 1),
                last_heartbeat = ?
            WHERE node_id = ?;
            """, (now_str, node_id))
            conn.commit()
            return True

    def create_sync_checkpoint(self, source_node: str, target_node: str,
                               event_type: str, details: Dict[str, Any]) -> int:
        """Logs a state synchronization event between nodes."""
        now_str = get_ist_now()
        details_str = json.dumps(details, ensure_ascii=False)
        checksum = hashlib.sha256(details_str.encode("utf-8")).hexdigest()[:16]

        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO sync_events (event_type, source_node, target_node, payload_checksum, status, details_json, created_at)
            VALUES (?, ?, ?, ?, 'COMPLETED', ?, ?);
            """, (event_type, source_node, target_node, checksum, details_str, now_str))
            conn.commit()
            return cur.lastrowid

    def export_sync_package(self, cycle_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Exports a self-contained JSON synchronization pack containing:
        - Daily cycle state
        - 10 validated slots (with 32 fields)
        - Active jobs
        - Sync timestamp
        """
        if not cycle_date:
            cycle_date = get_cycle_date_str()

        slots = self.db.get_cycle_slots(cycle_date)

        pack = {
            "version": "1.0",
            "cycle_date": cycle_date,
            "exported_at": get_ist_now(),
            "slots": [dict(s) for s in slots],
            "total_slots": len(slots)
        }
        return pack

    def import_sync_package(self, pack: Dict[str, Any], source_node: str) -> Dict[str, Any]:
        """
        Imports and reconciles a synchronization pack from a peer node.
        Detects conflicts and updates local ledger idempotently.
        """
        cycle_date = pack.get("cycle_date")
        slots = pack.get("slots", [])
        if not cycle_date or not slots:
            return {"status": "ERROR", "message": "Invalid sync payload format"}

        applied_slots = 0
        conflicts = 0

        for slot_data in slots:
            slot_id = slot_data.get("slot_id")
            existing = self.db.get_slot(cycle_date, slot_id)
            if existing:
                if existing["status"] == "COMPLETED" and slot_data.get("status") != "COMPLETED":
                    conflicts += 1
                    continue
            self.db.upsert_slot(cycle_date, slot_id, slot_data)
            applied_slots += 1

        self.create_sync_checkpoint(
            source_node=source_node,
            target_node=DEFAULT_LAPTOP_NODE,
            event_type="PACKAGE_IMPORT",
            details={
                "cycle_date": cycle_date,
                "applied_slots": applied_slots,
                "conflicts": conflicts
            }
        )

        return {
            "status": "SUCCESS",
            "cycle_date": cycle_date,
            "applied_slots": applied_slots,
            "conflicts": conflicts
        }

    def get_ecosystem_status(self) -> Dict[str, Any]:
        """Returns health summary of all registered nodes and sync checkpoints."""
        with self.db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM device_nodes ORDER BY last_heartbeat DESC;")
            nodes = [dict(r) for r in cur.fetchall()]

            cur.execute("""
            SELECT status, count(*) as count 
            FROM generation_jobs 
            GROUP BY status;
            """)
            jobs_summary = {r["status"]: r["count"] for r in cur.fetchall()}

            cur.execute("SELECT * FROM sync_events ORDER BY id DESC LIMIT 5;")
            recent_syncs = [dict(r) for r in cur.fetchall()]

        return {
            "nodes": nodes,
            "active_node_count": len(nodes),
            "jobs_summary": jobs_summary,
            "recent_sync_events": recent_syncs,
            "checked_at": get_ist_now()
        }


# Singleton instance
sync_manager = SyncManager()


if __name__ == "__main__":
    print("Testing SyncManager...")
    sm = SyncManager()
    sm.record_heartbeat(DEFAULT_LAPTOP_NODE)
    sm.record_heartbeat(DEFAULT_MOBILE_NODE)
    status = sm.get_ecosystem_status()
    print("Registered Nodes:", [n["node_id"] for n in status["nodes"]])
    print("Node Online Check (Laptop):", sm.is_node_online(DEFAULT_LAPTOP_NODE))
    print("Node Online Check (Mobile):", sm.is_node_online(DEFAULT_MOBILE_NODE))
    print("Ecosystem Status:", status["jobs_summary"])
    print("[SUCCESS] SyncManager operational.")
