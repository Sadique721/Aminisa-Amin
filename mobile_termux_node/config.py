# -*- coding: utf-8 -*-
"""
Aminsa Mobile Ecosystem Configuration
======================================
100% Standalone on OPPO A78 5G (Android 15) inside Termux.
Strict Priority: India First, Dynamic Real-Time RSS, Video Prompts ONLY.
YouTube Create Bound: Strictly 250 - 300 characters for all Video Prompts.
"""

import os

# Base paths
BASE_DIR = "/data/data/com.termux/files/home/aminsa_mobile_ecosystem"
HOME_DIR = "/data/data/com.termux/files/home"


def _resolve_storage():
    # If running inside Termux on Android
    if os.path.exists("/data/data/com.termux"):
        sdcard = "/sdcard/DCIM/Aminsa"
        try:
            os.makedirs(sdcard, exist_ok=True)
            test_path = os.path.join(sdcard, ".write_test")
            with open(test_path, "w") as f:
                f.write("ok")
            os.remove(test_path)
            return sdcard
        except Exception:
            fallback = os.path.join(HOME_DIR, "aminsa_data")
            os.makedirs(fallback, exist_ok=True)
            return fallback
    else:
        # Running on Windows/Laptop host for testing
        local_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
        os.makedirs(local_dir, exist_ok=True)
        return local_dir


SDCARD_DIR = _resolve_storage()
LOG_FILE = os.path.join(SDCARD_DIR, "aminsa_daemon.log")
AUDIO_DIR = os.path.join(SDCARD_DIR, "audio")
MEDIA_DIR = os.path.join(SDCARD_DIR, "generated_media")

ADB_HOST = "127.0.0.1"
ADB_PORT = 5555
ADB_TARGET = f"{ADB_HOST}:{ADB_PORT}"

PACKAGES = {
    "youtube_create": "com.google.android.apps.youtube.producer",
    "youtube": "com.google.android.youtube",
    "instagram": "com.instagram.android",
    "threads": "com.instagram.barcelona",
    "facebook": "com.facebook.katana",
}

# YouTube Create UI Touch Coordinates (OPPO A78 5G 720x1612)
YT_CREATE_COORDS = {
    "generate_video_btn": (387, 669),
    "generate_image_btn": (537, 669),
    "edit_with_ai_btn": (238, 669),
    "prompt_input": (360, 500),
    "generate_submit_btn": (643, 906),
    "close_back_btn": (47, 105),
}

# Persona & Voice Settings
PERSONA_NAME = "Aminsa"
VOICE_NAME = "hi-IN-SwaraNeural"
VOICE_RATE = "-2%"
VOICE_PITCH = "+1Hz"
GREETING = "Hello everyone"

CYCLE_HOURS = 2.4
TOTAL_DAILY_SLOTS = 10
WEB_PORT = 8765

# YouTube Create Bound Settings
YT_CREATE_MAX_CHARS = 295
YT_CREATE_MIN_CHARS = 250

# 10 Daily Production Slots (India Priority + Specialized Domains)
CATEGORIES = [
    {
        "id": "slot_1",
        "time": "08:00 AM",
        "category": "special_day_or_india_top",
        "name": "India National Day & Morning Focus",
        "language": "hinglish",
        "rss_query": "india breaking news national events",
        "look": {
            "attire": "Graceful ivory khadi short kurti with delicate tricolor thread border",
            "setting": "Warm morning sunlight courtyard with historic Indian stone pillars softly blurred",
            "attire_short": "ivory khadi kurti",
            "setting_short": "Morning courtyard with stone pillars"
        }
    },
    {
        "id": "slot_2",
        "time": "10:24 AM",
        "category": "tech_ai",
        "name": "Global & Indian Tech & AI Revolution",
        "language": "english",
        "rss_query": "artificial intelligence models technology breakthrough india",
        "look": {
            "attire": "Crisp modern navy-blue tailored blazer over minimalist white silk top",
            "setting": "Futuristic tech lab studio with subtle blue ambient rim lighting and glass monitor",
            "attire_short": "navy-blue tailored blazer",
            "setting_short": "Futuristic tech lab studio"
        }
    },
    {
        "id": "slot_3",
        "time": "12:48 PM",
        "category": "cricket_sports",
        "name": "Cricket & Sports Updates",
        "language": "hinglish",
        "rss_query": "india cricket match bcci team india sports",
        "look": {
            "attire": "Sporty royal blue zip-up athletic jacket with clean white accents",
            "setting": "Vibrant sports broadcast studio desk with stadium illumination in backdrop",
            "attire_short": "royal blue athletic jacket",
            "setting_short": "Vibrant sports broadcast desk"
        }
    },
    {
        "id": "slot_4",
        "time": "03:12 PM",
        "category": "economy_business",
        "name": "Indian Economy, Startups & Market Trends",
        "language": "hinglish",
        "rss_query": "indian startups economy markets sensex unicorn",
        "look": {
            "attire": "Elegantly tailored charcoal formal blazer over an emerald green top",
            "setting": "Modern minimalist corporate glass boardroom overlooking Bengaluru skyline",
            "attire_short": "charcoal tailored blazer",
            "setting_short": "Modern glass boardroom"
        }
    },
    {
        "id": "slot_5",
        "time": "05:36 PM",
        "category": "culture_heritage",
        "name": "Indian Culture, Art & Regional Heritage",
        "language": "hinglish",
        "rss_query": "indian art culture festivals heritage monuments",
        "look": {
            "attire": "Vibrant mustard-yellow embroidered chanderi kurta with silver jhumkas",
            "setting": "Aesthetic Indian heritage courtyard illuminated with warm terracotta lamps",
            "attire_short": "mustard-yellow embroidered kurta",
            "setting_short": "Heritage courtyard with lamps"
        }
    },
    {
        "id": "slot_6",
        "time": "08:00 PM",
        "category": "bollywood_trends",
        "name": "Bollywood, OTT & Entertainment Trends",
        "language": "hinglish",
        "rss_query": "bollywood movies ott releases box office trending entertainment",
        "look": {
            "attire": "Chic contemporary maroon satin co-ord set with minimalist gold pendant",
            "setting": "Lively warm studio lounge with golden fairy lights and cinematic bokeh",
            "attire_short": "maroon satin co-ord set",
            "setting_short": "Warm studio lounge with fairy lights"
        }
    },
    {
        "id": "slot_7",
        "time": "10:24 PM",
        "category": "science_isro",
        "name": "ISRO, Space & Indian Innovations",
        "language": "hinglish",
        "rss_query": "isro satellite space mission drdo science india",
        "look": {
            "attire": "Clean metallic-accented slate grey smart blazer",
            "setting": "High-tech space observatory control center with glowing telemetry screens",
            "attire_short": "slate grey smart blazer",
            "setting_short": "Space observatory control center"
        }
    },
    {
        "id": "slot_8",
        "time": "12:48 AM",
        "category": "future_tech",
        "name": "Future Tech & Developer Ecosystem",
        "language": "english",
        "rss_query": "software development open source next generation technology",
        "look": {
            "attire": "Dark minimalist designer hoodie with subtle neon geometric trim",
            "setting": "Late-night developer workstation with dual ultra-wide curved code displays",
            "attire_short": "minimalist designer hoodie",
            "setting_short": "Night developer workstation"
        }
    },
    {
        "id": "slot_9",
        "time": "03:12 AM",
        "category": "global_affairs",
        "name": "Global Affairs (India's Lens)",
        "language": "hinglish",
        "rss_query": "world news international affairs geopolitical india global",
        "look": {
            "attire": "Classic navy formal collared shirt with rolled cuffs",
            "setting": "Sophisticated global news studio with backlit world map glass panel",
            "attire_short": "navy formal collared shirt",
            "setting_short": "Global newsroom studio"
        }
    },
    {
        "id": "slot_10",
        "time": "05:36 AM",
        "category": "wellness_health",
        "name": "Morning Health, Yoga & Wellness",
        "language": "hinglish",
        "rss_query": "yoga health wellness fitness routine lifestyle india",
        "look": {
            "attire": "Pastel peach breathable cotton yoga kurta with comfortable stretch fit",
            "setting": "Lush green outdoor botanical terrace at sunrise with golden dawn mist",
            "attire_short": "pastel peach yoga kurta",
            "setting_short": "Sunrise botanical terrace"
        }
    }
]
