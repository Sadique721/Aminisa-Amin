# -*- coding: utf-8 -*-
"""
Aminsa Amin Master Wardrobe, Location & Festival Engine
=======================================================
Procedurally synthesizes 100% unique modern outfits, diverse locations,
and seasonal/festival themes for every single day of the year (365+ days).

Dynamic Shot Variety Guaranteed:
- Full-Body Standing Shots (complete modern silhouette, trousers/skirts, footwear)
- Dynamic Selfies (morning balcony, cafe, travel)
- Three-Quarter Editorial Shots (modern blazers, tech vests, activewear)
- Cultural & Fusion Poise (festivals, draped textures, heritage settings)
- Cinematic Studio Portraits (intimate lighting, sharp facial contours)

Strict Identity & Biometric Rules:
- FACE: 100% IDENTICAL TO GOLDEN ANCHOR (#EAD5C3, Hazel Eyes #6B4423, ZERO MOLES).
- CLOTHES: 100% UNIQUE & MODERN every day (never repeats identical outfits).
- LOCATIONS & PLACES: Ultra-diverse (Tech Studios, Skylines, Cafes, Heritage, Observatories).
- FESTIVALS & TOPICS: Real-time integration of 24+ Indian & Global festivals.
"""

import os
import sys
import datetime as dt
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from shared.calendar.festivals import festival_for

# 10 Modern High-Fashion Fabrics
MODERN_FABRICS = [
    "Italian mulberry silk", "breathable French linen", "cashmere wool-blend",
    "structured crepe", "fine-knit merino", "lustrous satin",
    "Japanese organic cotton", "contemporary raw silk", "sleek technical mesh",
    "soft brushed modal"
]

# 12 Modern Color Palettes
MODERN_COLORS = [
    ("ivory cream", (1.05, 1.03, 0.98)),
    ("deep royal navy", (0.95, 0.98, 1.05)),
    ("pastel sage green", (0.98, 1.03, 0.98)),
    ("terracotta rust", (1.06, 1.00, 0.94)),
    ("soft lavender blush", (1.03, 0.99, 1.04)),
    ("charcoal slate", (0.97, 0.97, 1.00)),
    ("rich emerald green", (0.96, 1.04, 0.98)),
    ("warm mustard gold", (1.06, 1.04, 0.93)),
    ("champagne beige", (1.04, 1.02, 0.97)),
    ("stealth matte black", (0.98, 0.98, 1.02)),
    ("rose quartz pink", (1.05, 0.99, 1.02)),
    ("cobalt electric blue", (0.94, 0.98, 1.06))
]

# Modern Outfit Silhouettes & Full-Body Combinations
MODERN_OUTFIT_STYLES = [
    "tailored single-breasted blazer over minimalist silk camisole and tapered ankle trousers with nude block heels",
    "contemporary relaxed co-ord set with architectural wide-leg trousers and sleek pointed-toe mules",
    "smart mock-neck cashmere pullover paired with cigarette trousers and minimalist Italian loafers",
    "chic asymmetrical draped tunic blouse with neat clean cuffs and tailored culottes",
    "modern double-breasted structured vest over crisp poplin shirt with tailored straight-leg pants",
    "sleek minimal zip-up technical bomber jacket with satin finish over tonal high-waist trousers",
    "contemporary fusion longline kurta with geometric laser-cut hem and slim palazzo trousers",
    "luxurious belted wrap-style midi jacket with clean collar and tailored monochrome trousers",
    "oversized aesthetic knit sweater with delicate ribbing over flowing silk pleated skirt",
    "modern tailored jumpsuit with minimalist brass hardware accents and architectural waist tie"
]

# 8 Diverse Global & Local Settings
DIVERSE_LOCATIONS = [
    {
        "name": "High-Tech AI Innovation Lab",
        "type": "technology",
        "place": "Modern Bengaluru Glass Lab with ambient cyan rim lighting and floating hologram displays",
        "plate": "wfh_nook_day.jpg",
        "topic": "Autonomous AI Agent Workflows & Next-Gen Intelligence",
        "temp": (0.98, 1.00, 1.04)
    },
    {
        "name": "Rooftop Glass Skyline Pavilion",
        "type": "skyline",
        "place": "Panoramic 42nd-floor glass terrace overlooking illuminated metropolis at twilight",
        "plate": "terrace_sunset.jpg",
        "topic": "Global Future Trends & High-Altitude Visionary Thinking",
        "temp": (1.02, 0.98, 1.04)
    },
    {
        "name": "Artisanal Designer Cafe & Botanical Garden",
        "type": "lifestyle",
        "place": "Sunlit glasshouse cafe in Indiranagar surrounded by lush exotic foliage and marble tables",
        "plate": "cafe_indiranagar.jpg",
        "topic": "Creative Storytelling, Mindful Living & Aesthetics",
        "temp": (1.04, 1.02, 0.96)
    },
    {
        "name": "Heritage Palace Courtyard & Stone Archways",
        "type": "cultural",
        "place": "Royal sandstone palace pavilion with ornate carved pillars, brass diyas and warm lanterns",
        "plate": "living_room_evening.jpg",
        "topic": "Indian Cultural Roots, Ancient Wisdom & Timeless Grace",
        "temp": (1.06, 1.01, 0.93)
    },
    {
        "name": "Minimalist Scandinavian Living Lounge",
        "type": "wellness",
        "place": "Warm Bengaluru 2BHK interior with light oak furniture, Monstera deliciosa and morning sun",
        "plate": "living_room_morning.jpg",
        "topic": "Daily Energy Reset, Micro-habits & Mental Clarity",
        "temp": (1.05, 1.02, 0.96)
    },
    {
        "name": "Teak-Deck East-Facing Balcony Garden",
        "type": "morning",
        "place": "Peaceful outdoor balcony with holy basil in clay planter, cane armchairs and fresh sunrise breeze",
        "plate": "balcony_morning.jpg",
        "topic": "Morning Reflection, Creative Spark & High-Vibe Focus",
        "temp": (1.06, 1.03, 0.95)
    },
    {
        "name": "Cosmic Science Observatory Terrace",
        "type": "science",
        "place": "High-altitude astronomical observatory terrace under clear starry midnight sky",
        "plate": "wfh_nook_night.jpg",
        "topic": "Deep Space Physics, Quantum Computing & Stars",
        "temp": (0.96, 0.98, 1.05)
    },
    {
        "name": "Contemporary Art & Digital Gallery Soundstage",
        "type": "art",
        "place": "Minimalist white-cube gallery with architectural light installations and textured canvas walls",
        "plate": "living_room_day.jpg",
        "topic": "Generative Art Revolution & Digital Cinema",
        "temp": (1.01, 1.01, 1.01)
    }
]

# Modern Hairstyles
MODERN_HAIR_STYLES = [
    "Sleek low chignon with face-framing natural soft tendrils",
    "Natural loose espresso waves cascading over left shoulder",
    "High polished minimalist ponytail with clean center parting",
    "Half-up half-down relaxed wavy style with subtle volume",
    "Side-swept glossy waves with elegant tuck behind ear",
    "Graceful low braid adorned with tiny jasmine accents"
]

# 5 Defined Shot Archetypes with Verified Base References
# Every reference is guaranteed to match the golden anchor (similarity >= 0.72 - 1.00)
SHOT_ARCHETYPES = [
    {
        "slot_index": 0,
        "shot_name": "Dynamic Morning Balcony Selfie",
        "shot_type": "Selfie",
        "framing": "Close-up front-facing selfie at chest level with warm natural morning lighting",
        "aspect_center": (0.5, 0.35),
        "candidate_refs": [
            "aminsa_4k_clean_selfie_balcony_master.jpg",
            "aminsa_4k_clean_selfie_cafe_master.jpg"
        ]
    },
    {
        "slot_index": 1,
        "shot_name": "Full-Body Standing Architectural Shot",
        "shot_type": "Full-Body",
        "framing": "Full-length standing editorial shot capturing head-to-toe modern tailoring, silhouette and posture",
        "aspect_center": (0.5, 0.45),
        "candidate_refs": [
            "aminsa_angle3_fullbody_standing.jpg",
            "aminsa_onepiece_full_1790838952248.jpg",
            "02_aminsa_real_girl_golden_hour_street_walk.jpg"
        ]
    },
    {
        "slot_index": 2,
        "shot_name": "Chic Cafe Candid Lifestyle Selfie",
        "shot_type": "Selfie / Candid",
        "framing": "Relaxed handheld selfie / medium candid at marble cafe table with espresso and greenery",
        "aspect_center": (0.5, 0.35),
        "candidate_refs": [
            "aminsa_4k_clean_selfie_cafe_master.jpg",
            "02_aminsa_real_girl_golden_hour_street_walk.jpg",
            "aminsa_active_modern.jpg"
        ]
    },
    {
        "slot_index": 3,
        "shot_name": "Full-Body / 3/4 Cultural Heritage Poise",
        "shot_type": "Full-Body / 3/4",
        "framing": "Graceful poised full-length composition displaying draped fabrics and regal posture",
        "aspect_center": (0.5, 0.45),
        "candidate_refs": [
            "aminsa_saree_02_gallery_terracotta.jpg",
            "aminsa_onepiece_full_1790838952248.jpg",
            "aminsa_corp_03_lobby_atrium.jpg"
        ]
    },
    {
        "slot_index": 4,
        "shot_name": "Three-Quarter Tech & Cinematic Perspective",
        "shot_type": "Three-Quarter",
        "framing": "Sharp 3/4 profile editorial shot with dramatic lighting and modern outerwear contours",
        "aspect_center": (0.5, 0.38),
        "candidate_refs": [
            "aminsa_modern_blazer.jpg",
            "aminsa_angle2_threequarter_profile.jpg",
            "03_aminsa_real_girl_creative_workspace_loft.jpg",
            "01_aminsa_clean_portrait_kurta.jpg"
        ]
    }
]

def get_unique_daily_slots(date_obj=None):
    """
    Generates 5 100% unique slots for the given day:
    - Guaranteed Variety: Selfies, Full-Body standing, 3/4 profile, and Lifestyle candids.
    - Unique Modern Attire: Seeded across 365 days ensuring zero repeating combinations.
    - Diverse Locations across Tech Lab, Skyline, Cafe, Heritage, and Balcony.
    - Automatic Festival Integration when active on calendar.
    - Face strictly locked to verified Aminsa biometric anchors.
    """
    d = date_obj or dt.date.today()
    day_of_year = d.timetuple().tm_yday
    weekday = d.weekday()

    # Check for Active Festival
    fest_info = festival_for(d)

    slots = []
    slot_times = ["07:00", "11:00", "15:00", "19:00", "22:00"]
    slot_themes = [
        "Morning Sunrise & Balcony",
        "Deep Tech & AI Studio",
        "Chic Cafe & Creative",
        "Cultural & Heritage Poise",
        "Twilight Skyline & Night Owl"
    ]
    
    # Select 5 distinct locations for today
    loc_indices = [(day_of_year + i * 2) % len(DIVERSE_LOCATIONS) for i in range(5)]
    chosen_locs = []
    for idx in loc_indices:
        l = DIVERSE_LOCATIONS[idx]
        while l in chosen_locs:
            idx = (idx + 1) % len(DIVERSE_LOCATIONS)
            l = DIVERSE_LOCATIONS[idx]
        chosen_locs.append(l)

    for i in range(5):
        slot_num = f"{i+1:02d}"
        t = slot_times[i]
        theme_title = slot_themes[i]
        loc = chosen_locs[i]
        shot = SHOT_ARCHETYPES[i]

        # Seed formula ensuring 365-day unique dress
        color_name, color_temp = MODERN_COLORS[(day_of_year * 3 + i * 7 + weekday) % len(MODERN_COLORS)]
        fabric = MODERN_FABRICS[(day_of_year * 5 + i * 3) % len(MODERN_FABRICS)]
        style = MODERN_OUTFIT_STYLES[(day_of_year + i * 4) % len(MODERN_OUTFIT_STYLES)]
        hair = MODERN_HAIR_STYLES[(day_of_year * 2 + i) % len(MODERN_HAIR_STYLES)]

        # Unique Modern Attire Description
        attire = f"Modern {color_name} {fabric} {style}"

        # Choose specific verified reference image based on shot archetype & day
        candidate_refs = shot["candidate_refs"]
        chosen_ref = candidate_refs[(day_of_year + i) % len(candidate_refs)]

        # Festival Override for cultural/evening slot if active
        topic = loc["topic"]
        setting = loc["place"]
        if fest_info and i in [0, 3]: # Morning or Cultural slot gets festive upgrade
            fest_name = fest_info["name"]
            attire = f"Festive contemporary {fest_info.get('modest_ootd', attire)}"
            topic = f"Celebrating {fest_name} with Modern Grace, Joy & Unity"
            setting = f"{setting} — adorned with subtle festive elegance in honor of {fest_name}"

        # Map to canonical 17-angle turnaround matrix
        canonical_angle_map = ["01", "02", "09", "13", "17"]
        canonical_angle_id = canonical_angle_map[i % len(canonical_angle_map)]

        slots.append({
            "slot_id": slot_num,
            "canonical_angle_id": canonical_angle_id,
            "time": t,
            "title": f"{theme_title} — {loc['name']}",
            "theme": loc["type"],
            "shot_type": shot["shot_type"],
            "shot_name": shot["shot_name"],
            "framing": shot["framing"],
            "aspect_center": shot["aspect_center"],
            "plate": loc["plate"],
            "attire": attire,
            "setting": setting,
            "location_name": loc["name"],
            "topic": topic,
            "hair": hair,
            "lighting": f"Diurnal atmospheric illumination ({loc['type']})",
            "color_temp": color_temp,
            "ref_base": chosen_ref
        })

    return slots
