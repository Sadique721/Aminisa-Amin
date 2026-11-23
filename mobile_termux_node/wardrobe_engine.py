# -*- coding: utf-8 -*-
"""
Aminsa Dynamic Wardrobe & Setting Matrix Engine (Mobile Node Bridge)
===================================================================
Upgraded from legacy 7-day hardcoded cycle to true 30-day dynamic variation engine.
Preserves backward compatibility with existing function signatures while ensuring
zero repetitive weekly patterns.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any

# Ensure project root in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from engines.dynamic_wardrobe_engine import dynamic_wardrobe_engine
    HAS_DYNAMIC_ENGINE = True
except Exception:
    HAS_DYNAMIC_ENGINE = False


def get_dynamic_wardrobe_and_setting(category_key: str, target_dt=None) -> Dict[str, Any]:
    """
    Returns a dynamically generated, 30-day anti-repetition wardrobe and setting.
    Compatible with existing mobile caller signatures.
    """
    dt = target_dt or datetime.now()
    cycle_date = dt.strftime("%Y-%m-%d")

    # Map category_key to pillar description
    category_pillar_map = {
        "special_day_or_india_top": "India National / Morning Brief",
        "tech_ai": "Global & Indian Technology / AI",
        "cricket_sports": "Cricket & Sports",
        "economy_business": "Indian Economy / Startups / Markets",
        "culture_heritage": "Culture / Art / Regional Heritage",
        "bollywood_trends": "Bollywood / OTT / Entertainment",
        "science_isro": "ISRO / Space / Innovation",
        "future_tech": "Future Technology / Developer Ecosystem",
        "global_affairs": "Global Affairs through India's Lens",
        "wellness_health": "Health / Yoga / Wellness"
    }
    pillar = category_pillar_map.get(category_key, "India National / Morning Brief")

    if HAS_DYNAMIC_ENGINE:
        look = dynamic_wardrobe_engine.generate_slot_look(slot_id=1, pillar=pillar, cycle_date=cycle_date)
        w = look["wardrobe"]
        s = look["background"]
        return {
            "attire": w["full_description"],
            "setting": s["full_description"],
            "attire_short": f"{w.get('color', '')} {w.get('garment', '')}".strip(),
            "setting_short": s.get("location_type", "Studio"),
            "wardrobe_hash": w.get("wardrobe_hash"),
            "setting_hash": s.get("setting_hash"),
            "camera_direction": look.get("camera_direction", "Slow push-in on subject")
        }

    # Safe fallback
    return {
        "attire": "Tailored ivory-white raw silk blazer over emerald shell blouse",
        "setting": "Modern minimalist Indian newsroom studio with warm ambient lighting",
        "attire_short": "ivory silk blazer",
        "setting_short": "Indian newsroom studio"
    }


if __name__ == "__main__":
    for cat in ["tech_ai", "culture_heritage", "cricket_sports", "science_isro"]:
        res = get_dynamic_wardrobe_and_setting(cat)
        print(f"[{cat}]")
        print(f"  Attire:  {res['attire']}")
        print(f"  Setting: {res['setting']}")
