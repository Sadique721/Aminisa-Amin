"""
Md Sadique Amin 24/7 Autonomous Mobile Daemon
=====================================
Runs natively in background inside Termux on Android.
Zero PC dependencies.
"""

import os
import sys
import time
import datetime
import random
import traceback
from config import (
    SDCARD_DIR, LOG_FILE, TOTAL_DAILY_SLOTS, CYCLE_HOURS,
    CATEGORIES
)
from topic_engine import get_slot_topic_and_prompts
from tts_engine import generate_voice
from adb_bridge import bridge
from youtube_create_driver import yt_driver
from social_poster import social_poster

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def get_current_slot_index():
    """Calculates slot index 0..9 based on current hour and minute."""
    now = datetime.datetime.now()
    minutes_since_midnight = now.hour * 60 + now.minute
    total_slot_minutes = 24 * 60 / TOTAL_DAILY_SLOTS # 144 mins = 2.4 hours
    slot_idx = int(minutes_since_midnight // total_slot_minutes) % TOTAL_DAILY_SLOTS
    return slot_idx

def execute_slot_cycle(slot_idx=None, skip_yt_generation=False):
    """Executes a single autonomous production and publishing cycle."""
    if slot_idx is None:
        slot_idx = get_current_slot_index()

    log("=" * 65)
    log(f"🚀 EXECUTING MD_SADIQUE_AMIN AUTONOMOUS CYCLE — SLOT #{slot_idx + 1}/{TOTAL_DAILY_SLOTS}")
    log("=" * 65)

    # 1. Ensure ADB bridge is connected
    connected, info = bridge.ensure_connected()
    if connected:
        log(f"[✓] ADB Local Bridge Connected: {info}")
    else:
        log(f"[!] Warning: ADB Local Bridge not ready: {info}")

    # 2. Fetch Topic & Generate Scripts
    log("[*] Fetching trending topic & crafting Md Sadique Amin look...")
    data = get_slot_topic_and_prompts(slot_idx)
    log(f"[+] Category: {data['slot_name']} ({data['category']})")
    log(f"[+] Headline: {data['headline']}")
    log(f"[+] Md Sadique Amin Look: {data['look']['attire'][:50]}... | Hair: {data['look']['hair']}")

    # 3. Synthesize Voice
    try:
        log("[*] Synthesizing Md Sadique Amin signature voice (hi-IN-SwaraNeural)...")
        audio_name = f"md_sadique_amin_slot_{slot_idx}_{int(time.time())}.mp3"
        audio_path = generate_voice(data["speech_script"], audio_name)
        log(f"[✓] Voice synthesized: {audio_path}")
    except Exception as e:
        log(f"[!] Voice error: {e}")
        audio_path = None

    # 4. YouTube Create 2-Step AI Generation (Image First -> Then Video)
    if not skip_yt_generation and connected:
        try:
            log("[*] [YouTube Create] Executing Step 1 (Locked Face Image) -> Step 2 (Video from Image)...")
            res = yt_driver.run_full_two_step_cycle(data["yt_image_prompt"], data["yt_video_prompt"])
            log(f"[✓] Step 1 Image proof: {res['image_proof']}")
            log(f"[✓] Step 2 Video proof: {res['video_proof']}")
        except Exception as e:
            log(f"[!] YouTube Create 2-step error: {e}")
    else:
        log("[i] YouTube Create generation skipped (dry-run or no ADB).")

    # 5. Social Media Sharing & Individual App Automation
    try:
        log("[*] Copying caption & preparing individual social media triggers...")
        social_poster.copy_to_clipboard(data["caption"])
        log(f"[✓] Social caption ready on clipboard.")

        # Check for generated video file to share
        latest_video = None
        if os.path.exists(SDCARD_DIR):
            for f in sorted(os.listdir(SDCARD_DIR), reverse=True):
                if f.endswith(".mp4") and not f.startswith(".trashed"):
                    latest_video = os.path.join(SDCARD_DIR, f)
                    break
        
        if latest_video:
            log(f"[*] Dispatching to individual apps with media: {latest_video}")
            social_poster.post_to_all_individual_platforms(
                media_path=latest_video,
                caption=data["caption"],
                title=data["headline"][:60]
            )
        else:
            # Fallback text share to Threads
            social_poster.share_to_threads(data["caption"])
    except Exception as e:
        log(f"[!] Social posting error: {e}")

    # 6. Android Native Notification
    bridge.notify(
        title=f"Md Sadique Amin AI: Slot #{slot_idx + 1} Done!",
        message=f"{data['slot_name']}: {data['headline'][:40]}... (Posted to Apps)"
    )
    log(f"[✓] Slot #{slot_idx + 1} completed successfully with individual app triggers!")
    log("=" * 65)
    return True


def run_daemon_loop():
    """Runs 24/7 background loop inside Termux."""
    log("=" * 65)
    log("🌟 MD_SADIQUE_AMIN STANDALONE 24/7 MOBILE DAEMON STARTED")
    log(f"🌟 Schedule: 10 videos per 24 hours (every {CYCLE_HOURS} hours)")
    log("=" * 65)

    bridge.acquire_wake_lock()
    log("[+] Termux wake-lock active — daemon will run with screen OFF.")

    last_slot = -1
    while True:
        try:
            curr_slot = get_current_slot_index()
            if curr_slot != last_slot:
                log(f"[*] New slot detected: #{curr_slot + 1}")
                execute_slot_cycle(curr_slot)
                last_slot = curr_slot
            else:
                # Slot already executed, check again in 2 minutes
                time.sleep(120)
        except KeyboardInterrupt:
            log("[!] Daemon stopped by user.")
            bridge.release_wake_lock()
            break
        except Exception as e:
            log(f"[!] Unexpected error in daemon loop: {e}")
            log(traceback.format_exc())
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        execute_slot_cycle(skip_yt_generation=False)
    elif len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        execute_slot_cycle(skip_yt_generation=True)
    elif len(sys.argv) > 1 and sys.argv[1] == "--slot":
        slot_num = int(sys.argv[2])
        execute_slot_cycle(slot_idx=slot_num, skip_yt_generation=False)
    else:
        run_daemon_loop()
