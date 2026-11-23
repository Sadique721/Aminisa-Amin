# -*- coding: utf-8 -*-
"""
Aminsa Emergency Software Kill Switch
======================================
Provides a centralized, tamper-resistant mechanism to immediately pause
or resume autonomous production across laptop and mobile nodes.
State file: state/kill_switch.json
"""

import os
import json
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_DIR)
KILL_SWITCH_PATH = os.path.join(_ROOT, "state", "kill_switch.json")


def _read_state() -> dict:
    if not os.path.exists(KILL_SWITCH_PATH):
        return {
            "production_enabled": True,
            "scheduler_enabled": True,
            "mobile_worker_enabled": True,
            "reason": "Default initialized",
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_by": "SYSTEM"
        }
    try:
        with open(KILL_SWITCH_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "production_enabled": False,  # Fail safe: pause if corrupt
            "scheduler_enabled": False,
            "mobile_worker_enabled": False,
            "reason": "Corrupt state file - fail safe triggered",
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_by": "FAIL_SAFE"
        }


def _write_state(data: dict) -> bool:
    os.makedirs(os.path.dirname(KILL_SWITCH_PATH), exist_ok=True)
    tmp_path = KILL_SWITCH_PATH + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if os.path.exists(KILL_SWITCH_PATH):
            os.replace(tmp_path, KILL_SWITCH_PATH)
        else:
            os.rename(tmp_path, KILL_SWITCH_PATH)
        return True
    except Exception as e:
        print(f"[-] Kill switch write error: {e}")
        return False


def is_production_enabled() -> bool:
    """Returns True if autonomous production is permitted."""
    st = _read_state()
    return bool(st.get("production_enabled", True))


def is_scheduler_enabled() -> bool:
    """Returns True if the 10-slot scheduler is active."""
    st = _read_state()
    return bool(st.get("scheduler_enabled", True)) and bool(st.get("production_enabled", True))


def is_mobile_worker_enabled() -> bool:
    """Returns True if the Termux mobile production node is permitted to produce."""
    st = _read_state()
    return bool(st.get("mobile_worker_enabled", True)) and bool(st.get("production_enabled", True))


def set_kill_switch(production_enabled: bool, reason: str = "", actor: str = "USER") -> dict:
    """Updates the kill switch state."""
    st = _read_state()
    st["production_enabled"] = production_enabled
    st["reason"] = reason or ("Autonomous production enabled" if production_enabled else "Emergency pause activated")
    st["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st["updated_by"] = actor
    _write_state(st)
    return st


def get_status() -> dict:
    """Returns the full kill switch status object."""
    return _read_state()


if __name__ == "__main__":
    print("Kill Switch Status:", get_status())
    print("Production Enabled:", is_production_enabled())
