"""
Md Sadique Amin Mobile Ecosystem — Exhaustive A-to-Z Test Suite
======================================================
Tests all layers of the standalone mobile system inside Termux:
1. Environment & Python Libraries
2. Local ADB Loopback Bridge
3. Live RSS Feeds & Category Classifier (10 Categories)
4. Persona Rules & YouTube Create Prompt Constraints (<850 chars)
5. Voice Synthesis Engine (Edge-TTS hi-IN-SwaraNeural @ 224Hz)
6. YouTube Create App Launch & Screen Control
7. Social Media Apps Ecosystem
8. Full End-to-End Autonomous Cycle Execution
"""

import sys
import os
import time
import subprocess

# Ensure Termux paths
os.environ["PATH"] = "/data/data/com.termux/files/usr/bin:" + os.environ.get("PATH", "")
os.environ["TMPDIR"] = "/data/data/com.termux/files/usr/tmp"
os.environ["HOME"] = "/data/data/com.termux/files/home"

sys.path.insert(0, "/data/data/com.termux/files/home/md_sadique_amin_mobile_ecosystem")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    TOTAL_DAILY_SLOTS, CATEGORIES, GREETING, PERSONA_NAME,
    PACKAGES, YT_CREATE_COORDS, AUDIO_DIR
)
from topic_engine import get_slot_topic_and_prompts, fetch_rss_headline
from tts_engine import generate_voice
from adb_bridge import bridge
from youtube_create_driver import yt_driver
from social_poster import social_poster
from md_sadique_amin_daemon import execute_slot_cycle

passed = 0
failed = 0

def record_test(name, success, detail=""):
    global passed, failed
    if success:
        passed += 1
        print(f"  [PASS] {name} {detail}")
    else:
        failed += 1
        print(f"  [FAIL] {name} {detail}")

print("\n" + "=" * 65)
print("🧪 MD_SADIQUE_AMIN AUTONOMOUS MOBILE ECOSYSTEM — A-TO-Z TEST SUITE")
print("=" * 65 + "\n")

# TEST 1: ENVIRONMENT & PACKAGES
print("[1/8] Testing Python Environment & Native Tools...")
try:
    import edge_tts
    record_test("edge_tts module", True)
except Exception as e:
    record_test("edge_tts module", False, str(e))

ffmpeg_res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
record_test("ffmpeg binary", ffmpeg_res.returncode == 0, f"(v: {ffmpeg_res.stdout[:20]}...)")

# TEST 2: LOCAL ADB LOOPBACK BRIDGE
print("\n[2/8] Testing Local ADB Loopback Bridge (127.0.0.1:5555)...")
conn, info = bridge.ensure_connected()
record_test("ADB Loopback Connection", conn, f"({info})")

# TEST 3: LIVE RSS & CATEGORY DIVERSITY (ALL 10 SLOTS)
print("\n[3/8] Testing 10 Daily Categories & Live RSS Feeds...")
categories_ok = True
for i, slot in enumerate(CATEGORIES):
    data = get_slot_topic_and_prompts(i)
    if not data["headline"] or len(data["headline"]) < 10:
        categories_ok = False
        print(f"    [-] Slot {i+1} ({slot['name']}): Invalid headline")
    else:
        print(f"    [+] Slot {i+1:02d} [{slot['name']}]: {data['headline'][:50]}...")
record_test("10 Category Schedule & RSS", categories_ok)

# TEST 4: PERSONA RULES & 2-STEP PROMPT CONSTRAINTS
print("\n[4/8] Validating Persona Rules & 2-Step YouTube Create Prompts...")
sample_slot = get_slot_topic_and_prompts(0)
img_prompt_len = len(sample_slot["yt_image_prompt"])
vid_prompt_len = len(sample_slot["yt_video_prompt"])
record_test("Step 1: Image Prompt Length (<850 chars)", img_prompt_len <= 850, f"({img_prompt_len} chars)")
record_test("Step 2: Video Prompt Length (<800 chars)", vid_prompt_len <= 800, f"({vid_prompt_len} chars)")

# Biometric Identity Anchors in Image Prompt
bio_anchors = ["#EAD5C3", "#6B4423", "zero moles", "Md Sadique Amin"]
bio_locked = all(anchor in sample_slot["yt_image_prompt"] for anchor in bio_anchors)
record_test("Biometric Lock: (#EAD5C3, #6B4423, zero moles)", bio_locked)

# Strict Rule: NEVER Namaste, ALWAYS "Hello everyone" or "Hello"
namaste_absent = "namaste" not in sample_slot["speech_script"].lower()
greeting_present = "hello" in sample_slot["speech_script"].lower()
record_test("Brand Safety: ZERO Namaste", namaste_absent)
record_test("Brand Safety: Hello Greeting", greeting_present)

# TEST 5: VOICE SYNTHESIS ENGINE
print("\n[5/8] Testing Voice Synthesis (Edge-TTS hi-IN-SwaraNeural @ 224Hz)...")
try:
    test_audio = generate_voice("Hello everyone! Standalone Termux voice synthesis test.", "test_voice.mp3")
    audio_exists = os.path.exists(test_audio) and os.path.getsize(test_audio) > 1000
    record_test("Edge-TTS hi-IN-SwaraNeural", audio_exists, f"({os.path.getsize(test_audio)} bytes)")
except Exception as e:
    record_test("Edge-TTS hi-IN-SwaraNeural", False, str(e))

# TEST 6: YOUTUBE CREATE APP & CONTROLLER
print("\n[6/8] Testing YouTube Create App Launch & Screen Control...")
yt_launched = yt_driver.launch()
record_test("YouTube Create Launch", yt_launched)
time.sleep(2)
# Check if foreground is YouTube Create
out, err, code = bridge.cmd(["shell", "dumpsys", "window", "displays"])
in_focus = "com.google.android.apps.youtube.producer" in out
record_test("YouTube Create In Focus", in_focus)
bridge.press_key(3) # Return HOME

# TEST 7: SOCIAL MEDIA APPS ECOSYSTEM
print("\n[7/8] Testing Installed Social Media Apps Presence...")
for app_name, pkg in PACKAGES.items():
    res = subprocess.run(["adb", "-s", bridge.target, "shell", "pm", "path", pkg], capture_output=True, text=True)
    installed = pkg in res.stdout
    record_test(f"App Installed: {app_name}", installed, f"({pkg})")

# TEST 8: FULL AUTONOMOUS CYCLE EXECUTION (DRY-RUN / TEST RUN)
print("\n[8/8] Testing Full Autonomous Cycle (Slot 0)...")
try:
    cycle_res = execute_slot_cycle(slot_idx=0, skip_yt_generation=False)
    record_test("Full Cycle Execution", cycle_res)
except Exception as e:
    record_test("Full Cycle Execution", False, str(e))

print("\n" + "=" * 65)
print(f"🏁 TEST SUITE COMPLETED: {passed} PASSED | {failed} FAILED")
print("=" * 65 + "\n")
