"""
Md Sadique Amin Mobile Ecosystem Configuration
======================================
100% Standalone on OPPO A78 5G (Android 15) inside Termux.
Zero PC dependencies.
"""

import os

# Base paths
BASE_DIR = "/data/data/com.termux/files/home/md_sadique_amin_mobile_ecosystem"
HOME_DIR = "/data/data/com.termux/files/home"

# Smart storage: prefer /sdcard if writable, fallback to Termux home
def _resolve_storage():
    sdcard = "/sdcard/DCIM/Md Sadique Amin"
    try:
        os.makedirs(sdcard, exist_ok=True)
        test_path = os.path.join(sdcard, ".write_test")
        with open(test_path, "w") as f:
            f.write("ok")
        os.remove(test_path)
        return sdcard  # sdcard is writable
    except Exception:
        fallback = os.path.join(HOME_DIR, "md_sadique_amin_data")
        os.makedirs(fallback, exist_ok=True)
        return fallback  # fallback to Termux home

SDCARD_DIR = _resolve_storage()
LOG_FILE = os.path.join(SDCARD_DIR, "md_sadique_amin_daemon.log")
AUDIO_DIR = os.path.join(SDCARD_DIR, "audio")
MEDIA_DIR = os.path.join(SDCARD_DIR, "generated_media")


# ADB Bridge Settings
ADB_HOST = "127.0.0.1"
ADB_PORT = 5555
ADB_TARGET = f"{ADB_HOST}:{ADB_PORT}"

# Package Names on Phone
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
PERSONA_NAME = "Md Sadique Amin"
VOICE_NAME = "hi-IN-SwaraNeural"
VOICE_RATE = "+0%"
VOICE_PITCH = "+0Hz"

# Strict Rule: NEVER USE NAMASTE
GREETING = "Hello everyone"

# 24-Hour Cycle Settings (10 videos = 2.4 hour intervals)
CYCLE_HOURS = 2.4
TOTAL_DAILY_SLOTS = 10

# 10 Daily Categories with Dynamic Looks
CATEGORIES = [
    {
        "id": "slot_1",
        "time": "06:00",
        "category": "tech",
        "name": "Morning Tech & AI",
        "rss_query": "technology+artificial+intelligence+india",
        "look": {
            "attire": "Crisp modern navy-blue tailored smart blazer over ivory minimalist silk top",
            "hair": "Sleek low bun with graceful front tendrils",
            "lipstick": "Soft rose nude matte",
            "setting": "High-tech studio with soft blue neon ambient rim lighting and glass desk",
        },
    },
    {
        "id": "slot_2",
        "time": "08:24",
        "category": "business",
        "name": "Business & Startups",
        "rss_query": "business+startup+economy+india",
        "look": {
            "attire": "Pastel grey blazer and white crisp formal shirt with modern collar",
            "hair": "High polished ponytail",
            "lipstick": "Warm terracotta semi-matte",
            "setting": "Sunlit glass corner corporate office overlooking city skyline",
        },
    },
    {
        "id": "slot_3",
        "time": "10:48",
        "category": "education",
        "name": "Education & Career",
        "rss_query": "education+skills+career+india",
        "look": {
            "attire": "Smart casual soft lavender knit cardigan over white crew-neck",
            "hair": "Natural loose espresso waves resting over left shoulder",
            "lipstick": "Subtle pink blush cream",
            "setting": "Warm contemporary library lounge with wooden bookshelves and soft lighting",
        },
    },
    {
        "id": "slot_4",
        "time": "13:12",
        "category": "lifestyle",
        "name": "Lifestyle & Daily Hacks",
        "rss_query": "lifestyle+health+gadgets+india",
        "look": {
            "attire": "Chic beige linen tunic with delicate mandarin collar",
            "hair": "Casual messy bun with gentle framing strands",
            "lipstick": "Peachy coral tint",
            "setting": "Modern minimalist kitchen with indoor monstera plant and daylight",
        },
    },
    {
        "id": "slot_5",
        "time": "15:36",
        "category": "creative",
        "name": "Creative & Digital Art",
        "rss_query": "creative+entertainment+design+cinema+india",
        "look": {
            "attire": "Stylish emerald green contemporary top with geometric cuts",
            "hair": "Voluminous side-parted soft waves",
            "lipstick": "Vibrant berry tint",
            "setting": "Artist gallery studio with warm canvas backdrops and soft spotlight",
        },
    },
    {
        "id": "slot_6",
        "time": "18:00",
        "category": "science",
        "name": "Science & Space Exploration",
        "rss_query": "science+space+isro+technology+india",
        "look": {
            "attire": "Futuristic deep charcoal jacket with clean metallic accents",
            "hair": "Pin-straight middle-parted glossy espresso hair",
            "lipstick": "Deep muted plum",
            "setting": "Observatory terrace with starry sky and deep purple twilight backdrop",
        },
    },
    {
        "id": "slot_7",
        "time": "20:24",
        "category": "cultural",
        "name": "Culture, Festivals & Heritage",
        "rss_query": "culture+festival+heritage+india",
        "look": {
            "attire": "Royal maroon silk kurta with fine golden thread zardozi embroidery and matching dupatta",
            "hair": "Traditional low braid adorned with tiny jasmine accents",
            "lipstick": "Classic deep Indian rose",
            "setting": "Heritage palace courtyard with warm brass diyas and carved stone pillars",
        },
    },
    {
        "id": "slot_8",
        "time": "22:48",
        "category": "mindset",
        "name": "Mindset & Personal Growth",
        "rss_query": "mindset+productivity+wellness+india",
        "look": {
            "attire": "Warm oatmeal-toned cashmere oversized turtle-neck sweater",
            "hair": "Soft bedtime tousled hair falling naturally",
            "lipstick": "Natural nude balm",
            "setting": "Cozy living room corner with warm fairy lights and ceramic tea cup",
        },
    },
    {
        "id": "slot_9",
        "time": "01:12",
        "category": "night_tech",
        "name": "Night Owl Tech & Coding",
        "rss_query": "cybersecurity+coding+gadgets+future",
        "look": {
            "attire": "Matte black oversized aesthetic tech hoodie",
            "hair": "Slightly undone wavy hair tucked behind ear",
            "lipstick": "Soft cinnamon nude",
            "setting": "Dark gaming/coding workspace with gentle dual cyan and magenta ambient LEDs",
        },
    },
    {
        "id": "slot_10",
        "time": "03:36",
        "category": "global_trends",
        "name": "Global Innovation & World View",
        "rss_query": "innovation+world+future+breakthrough",
        "look": {
            "attire": "Sophisticated pearl-white silk shirt with subtle French cuffs",
            "hair": "Half-up half-down gentle wavy style",
            "lipstick": "Warm caramel nude",
            "setting": "Modern rooftop glass pavilion overlooking illuminated global metropolis",
        },
    },
]
