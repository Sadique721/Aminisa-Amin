"""
Aminsa Amin Mobile Ecosystem — Exhaustive A-to-Z Test Suite
===========================================================
Tests all layers of the standalone mobile system inside Termux:
1. Environment & Python Libraries
2. Local ADB Loopback Bridge (127.0.0.1:5555)
3. Live Categories & Dynamic Time-Aware Rotation (10 Daily Slots)
4. Strict YouTube Create Constraints: 250 to 300 Characters
5. Strict Speech Constraints: Cleanly under 10 seconds (<=25 words, zero Namaste)
6. Voice Synthesis Engine (Edge-TTS hi-IN-SwaraNeural, rate -2%, pitch +1Hz)
7. YouTube Create Driver & App Focus
8. Social Media Ecosystem & Individual App Automation
9. Full Autonomous Cycle Dry-Run Execution
"""

import sys
import os
import time
import subprocess

# Ensure Termux paths
os.environ["PATH"] = "/data/data/com.termux/files/usr/bin:" + os.environ.get("PATH", "")
os.environ["TMPDIR"] = "/data/data/com.termux/files/usr/tmp"
os.environ["HOME"] = "/data/data/com.termux/files/home"

sys.path.insert(0, "/data/data/com.termux/files/home/aminsa_mobile_ecosystem")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    TOTAL_DAILY_SLOTS, CATEGORIES, GREETING, PERSONA_NAME,
    PACKAGES, YT_CREATE_COORDS, AUDIO_DIR,
    YT_CREATE_PROMPT_MIN_CHARS, YT_CREATE_PROMPT_MAX_CHARS,
    MAX_SPEECH_WORD_COUNT
)
from topic_engine import get_slot_topic_and_prompts, fetch_rss_headline
from tts_engine import generate_voice
from adb_bridge import bridge
from youtube_create_driver import yt_driver
from social_poster import social_poster
from aminsa_daemon import execute_slot_cycle

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
print("🧪 AMINSA AMIN AUTONOMOUS MOBILE ECOSYSTEM — A-TO-Z TEST SUITE")
print("=" * 65 + "\n")

# TEST 1: ENVIRONMENT & PACKAGES
print("[1/9] Testing Python Environment & Native Tools...")
try:
    import edge_tts
    record_test("edge_tts module", True)
except Exception as e:
    record_test("edge_tts module", False, str(e))

ffmpeg_res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
record_test("ffmpeg binary", ffmpeg_res.returncode == 0, f"(found)")

# TEST 2: LOCAL ADB LOOPBACK BRIDGE
print("\n[2/9] Testing Local ADB Loopback Bridge (127.0.0.1:5555)...")
conn, info = bridge.ensure_connected()
record_test("ADB Loopback Connection", conn, f"({info})")

# TEST 3: CATEGORY DIVERSITY & TIME-AWARE ROTATION
print("\n[3/9] Testing 10 Daily Categories & Dynamic Looks...")
categories_ok = True
for i, slot in enumerate(CATEGORIES):
    data = get_slot_topic_and_prompts(i)
    if not data["look"]["attire"] or not data["look"]["setting"]:
        categories_ok = False
        print(f"    [-] Slot {i+1} ({slot['name']}): Invalid look data")
    else:
        print(f"    [+] Slot {i+1:02d} [{slot['name']}]: {data['look']['attire'][:45]}... | {data['look']['setting'][:40]}...")
record_test("10 Category Schedule & Looks", categories_ok)

# TEST 4: STRICT YOUTUBE CREATE PROMPT CONSTRAINTS (250 TO 300 CHARACTERS)
print("\n[4/9] Validating YouTube Create Prompt Lengths (STRICT 250 - 300 CHARS)...")
prompts_ok = True
for i in range(10):
    pkg = get_slot_topic_and_prompts(i)
    plen = len(pkg["yt_create_prompt"])
    valid = YT_CREATE_PROMPT_MIN_CHARS <= plen <= YT_CREATE_PROMPT_MAX_CHARS
    if not valid:
        prompts_ok = False
        print(f"    [-] Slot {i+1} prompt failed: {plen} chars (expected 250..300)")
    else:
        print(f"    [+] Slot {i+1:02d}: {plen} chars -> \"{pkg['yt_create_prompt'][:65]}...\"")
record_test("YouTube Create Prompt Bounds (250-300 chars)", prompts_ok)

# Biometric Identity Anchors in Prompt
sample_slot = get_slot_topic_and_prompts(0)
bio_anchors = ["#EAD5C3", "almond hazel eyes", "Aminsa Amin"]
bio_locked = all(anchor in sample_slot["yt_create_prompt"] for anchor in bio_anchors)
record_test("Biometric Lock: (#EAD5C3, almond hazel eyes, Aminsa Amin)", bio_locked)

# TEST 5: STRICT SPEECH DURATION & BRAND SAFETY (UNDER 10 SECONDS, ZERO NAMASTE)
print("\n[5/9] Validating Speech Duration & Strict Brand Safety (<=10 sec / <=25 words)...")
speech_ok = True
for i in range(10):
    pkg = get_slot_topic_and_prompts(i)
    wcnt = pkg["speech_word_count"]
    script = pkg["speech_script"]
    if wcnt > MAX_SPEECH_WORD_COUNT or not script.startswith("Hello everyone"):
        speech_ok = False
        print(f"    [-] Slot {i+1} speech invalid: {wcnt} words -> {script}")
record_test("Speech Word Count (<=25 words, under 10s)", speech_ok)

namaste_absent = "namaste" not in sample_slot["speech_script"].lower()
greeting_present = sample_slot["speech_script"].startswith("Hello everyone")
record_test("Brand Safety: ZERO Namaste", namaste_absent)
record_test("Brand Safety: Hello Greeting Hook", greeting_present)

# TEST 6: VOICE SYNTHESIS ENGINE
print("\n[6/9] Testing Voice Synthesis (hi-IN-SwaraNeural, rate -2%, pitch +1Hz)...")
try:
    test_audio = generate_voice("Hello everyone, main hoon Aminsa! Standalone Termux voice test successful.", "test_voice.mp3")
    audio_exists = os.path.exists(test_audio) and os.path.getsize(test_audio) > 1000
    record_test("Edge-TTS hi-IN-SwaraNeural", audio_exists, f"({os.path.getsize(test_audio)} bytes)")
except Exception as e:
    record_test("Edge-TTS hi-IN-SwaraNeural", False, str(e))

# TEST 7: YOUTUBE CREATE APP CONTROLLER
print("\n[7/9] Testing YouTube Create App Controller...")
yt_launched = yt_driver.launch()
record_test("YouTube Create Launch", yt_launched)
time.sleep(2)
out, err, code = bridge.cmd(["shell", "dumpsys", "window", "displays"])
in_focus = "com.google.android.apps.youtube.producer" in out
record_test("YouTube Create In Focus", in_focus)
bridge.press_key(3)  # Return HOME

# TEST 8: SOCIAL MEDIA APPS PRESENCE
print("\n[8/9] Testing Installed Social Media Apps Presence...")
for app_name, pkg in PACKAGES.items():
    try:
        res = subprocess.run([bridge.adb, "-s", bridge.target, "shell", "pm", "path", pkg], capture_output=True, text=True)
        installed = pkg in res.stdout
    except Exception:
        installed = False
    record_test(f"App Installed: {app_name}", installed, f"({pkg})")

# TEST 9: FULL AUTONOMOUS CYCLE EXECUTION (DRY-RUN / TEST RUN)
print("\n[9/9] Testing Full Autonomous Cycle (Slot 0 Dry-Run)...")
try:
    cycle_res = execute_slot_cycle(slot_idx=0, skip_yt_generation=True)
    record_test("Full Cycle Dry-Run Execution", cycle_res)
except Exception as e:
    record_test("Full Cycle Dry-Run Execution", False, str(e))

print("\n" + "=" * 65)
print(f"🏁 TEST SUITE COMPLETED: {passed} PASSED | {failed} FAILED")
print("=" * 65 + "\n")
