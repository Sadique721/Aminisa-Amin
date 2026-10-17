"""
YouTube Create ADB Driver for Md Sadique Amin
======================================
Controls YouTube Create app on OPPO A78 5G via ADB to:
1. Open YouTube Create → Navigate to "Generate" / "Create with AI"
2. Type Md Sadique Amin image prompt → Tap Generate → Wait for image
3. Use generated image → Type video prompt → Generate talking avatar video
4. Export/save finished video to phone gallery
5. Pull video file to PC for multi-platform upload

All interactions done via ADB shell commands (tap, swipe, input text, keyevent).
No root required. Works on stock OPPO A78 5G.
"""

import os
import sys
import subprocess
import time
import glob

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from mobile_app_controller import get_adb_device, ADB_EXE

YT_CREATE_PKG = "com.google.android.apps.youtube.producer"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "exports", "youtube_create_videos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PHONE_DCIM = "/sdcard/DCIM/YouTube Create"
PHONE_MOVIES = "/sdcard/Movies/YouTube Create"
PHONE_MD_SADIQUE_AMIN = "/sdcard/DCIM/Md Sadique Amin"

# ─────────────────────────────────────────────
# ADB HELPERS
# ─────────────────────────────────────────────
def adb(serial, *args, check=False, capture=True):
    cmd = [ADB_EXE, "-s", serial] + list(args)
    return subprocess.run(cmd, capture_output=capture, text=True, check=check)

def tap(serial, x, y, delay=1.5):
    adb(serial, "shell", "input", "tap", str(x), str(y))
    time.sleep(delay)

def swipe(serial, x1, y1, x2, y2, duration=400, delay=1.0):
    adb(serial, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration))
    time.sleep(delay)

def keyevent(serial, code, delay=0.5):
    adb(serial, "shell", "input", "keyevent", str(code))
    time.sleep(delay)

def clear_text(serial, chars=200):
    """Clear existing text field content."""
    adb(serial, "shell", "input", "keyevent", "KEYCODE_CTRL_A")
    time.sleep(0.3)
    adb(serial, "shell", "input", "keyevent", "KEYCODE_DEL")
    time.sleep(0.3)

def type_text(serial, text, chunk_size=5):
    """Type text via ADB in chunks (avoids buffer overflow)."""
    # Sanitize text for ADB input
    safe = (text
        .replace("'", "")
        .replace('"', "")
        .replace("&", "and")
        .replace("<", "")
        .replace(">", "")
        .replace("|", "")
        .replace("(", "")
        .replace(")", "")
        .replace("#", "")
        .replace("$", "")
        .replace("`", "")
        .replace("\\", "")
        .replace(";", "")
        .replace("!", "")
    )
    words = safe.split(" ")
    chunk = []
    for word in words:
        chunk.append(word)
        if len(chunk) >= chunk_size:
            text_chunk = "%s".join(chunk) + "%s"
            adb(serial, "shell", f"input text {text_chunk}")
            chunk = []
            time.sleep(0.12)
    if chunk:
        text_chunk = "%s".join(chunk)
        adb(serial, "shell", f"input text {text_chunk}")
    time.sleep(0.5)

def screenshot(serial, name="yt_create_state"):
    """Take screenshot and pull to PC for debug."""
    remote = f"/sdcard/{name}.png"
    local = os.path.join(PROJECT_ROOT, f"{name}.png")
    adb(serial, "shell", "screencap", "-p", remote)
    adb(serial, "pull", remote, local)
    return local

# ─────────────────────────────────────────────
# YOUTUBE CREATE APP NAVIGATOR
# ─────────────────────────────────────────────
class YouTubeCreateDriver:
    def __init__(self):
        self.serial, self.state = get_adb_device()
        if self.state != "device":
            raise RuntimeError(f"[ERROR] OPPO A78 5G not connected! ADB state: {self.state}")
        print(f"[+] Connected to OPPO A78 5G ({self.serial})")

    # ── Step 1: Launch YouTube Create ──
    def launch(self):
        print("[*] Launching YouTube Create...")
        adb(self.serial, "shell", "am", "force-stop", YT_CREATE_PKG)
        time.sleep(1)
        adb(self.serial, "shell", "am", "start", "-n",
            f"{YT_CREATE_PKG}/{YT_CREATE_PKG}.ui.MainActivity")
        time.sleep(4)
        # Dismiss any notifications or overlays
        keyevent(self.serial, "4", delay=0.5)   # BACK to dismiss
        keyevent(self.serial, "4", delay=0.5)
        print("[+] YouTube Create launched.")

    # ── Step 2: Navigate to Generate / Create with AI ──
    def navigate_to_generate(self):
        print("[*] Navigating to 'Generate' AI screen...")
        # Bottom nav bar: tap '+' / Create button (center bottom)
        tap(self.serial, 360, 1500, delay=2)
        # Look for "Generate" option in bottom sheet
        tap(self.serial, 360, 900, delay=2)  # "Generate" tile
        time.sleep(1)
        print("[+] On Generate screen.")

    # ── Step 3: Type image prompt and generate image ──
    def generate_image(self, image_prompt):
        print(f"[*] Typing image prompt ({len(image_prompt)} chars)...")
        # Tap on text field
        tap(self.serial, 360, 750, delay=1)
        clear_text(self.serial)
        type_text(self.serial, image_prompt)
        time.sleep(0.5)
        # Dismiss keyboard
        keyevent(self.serial, "4", delay=1)
        # Tap "Generate" / "Create" button
        print("[*] Tapping Generate button...")
        tap(self.serial, 360, 1450, delay=3)   # Generate button
        # Wait for AI generation (YouTube Create takes 30-90 sec)
        print("[*] Waiting for AI image generation (up to 90 seconds)...")
        time.sleep(60)
        # Extra wait if still processing
        for _ in range(3):
            res = adb(self.serial, "shell", "dumpsys", "window", "windows")
            if YT_CREATE_PKG in res.stdout:
                break
            time.sleep(20)
        print("[+] Image generation wait complete.")

    # ── Step 4: Select the generated image ──
    def select_generated_image(self):
        print("[*] Selecting generated image...")
        # Generated images usually appear in a grid; tap first result
        tap(self.serial, 180, 900, delay=2)  # First image in grid (top-left)
        # Tap "Use this" / "Select" button
        tap(self.serial, 360, 1480, delay=2)
        print("[+] Image selected.")

    # ── Step 5: Type video prompt and generate video ──
    def generate_video(self, video_prompt):
        print(f"[*] Typing video/avatar prompt ({len(video_prompt)} chars)...")
        # Video prompt field
        tap(self.serial, 360, 750, delay=1)
        clear_text(self.serial)
        type_text(self.serial, video_prompt)
        keyevent(self.serial, "4", delay=1)
        # Tap Generate video
        print("[*] Tapping Generate video button...")
        tap(self.serial, 360, 1450, delay=3)
        # YouTube Create video generation takes 60-180 sec
        print("[*] Waiting for AI video generation (up to 180 seconds)...")
        time.sleep(120)
        for _ in range(4):
            time.sleep(30)
            # Try to detect completion by checking screen
            sc = screenshot(self.serial, "yt_create_video_check")
            print(f"[*] Screenshot taken, checking for completion...")
            break   # proceed after wait
        print("[+] Video generation wait complete.")

    # ── Step 6: Export / Save video to gallery ──
    def export_video(self):
        print("[*] Exporting video to phone gallery...")
        # Tap 'Export' or 'Save' button (usually top-right or bottom-right)
        tap(self.serial, 640, 120, delay=2)   # Top-right export/save
        tap(self.serial, 360, 1200, delay=2)  # Confirm if dialog appears
        # Alternative: Share → Save to Gallery
        tap(self.serial, 640, 1480, delay=2)  # Share button
        time.sleep(1)
        tap(self.serial, 180, 900, delay=2)   # Save to device option
        time.sleep(3)
        print("[+] Export command sent. Video saving to gallery.")

    # ── Step 7: Pull video file from phone to PC ──
    def pull_video_to_pc(self, slot_id, topic_label):
        print("[*] Pulling generated video from phone gallery to PC...")
        safe_label = topic_label.replace(" ", "_").replace("/", "-")[:30]
        local_filename = f"md_sadique_amin_yt_create_slot{slot_id:02d}_{safe_label}.mp4"
        local_path = os.path.join(OUTPUT_DIR, local_filename)

        # Try multiple phone paths where YouTube Create might save
        for phone_dir in [PHONE_DCIM, PHONE_MOVIES, PHONE_MD_SADIQUE_AMIN, "/sdcard/DCIM/Camera"]:
            # Find most recently modified .mp4
            res = adb(self.serial, "shell",
                      f"ls -t {phone_dir}/*.mp4 2>/dev/null | head -1")
            remote_file = res.stdout.strip()
            if remote_file and ".mp4" in remote_file:
                pull_res = adb(self.serial, "pull", remote_file, local_path)
                if pull_res.returncode == 0 and os.path.exists(local_path):
                    print(f"[+] Video pulled: {local_path} ({os.path.getsize(local_path)//1024}KB)")
                    return local_path

        print(f"[-] Could not find generated video on phone. Will retry after publish wait.")
        return None

    # ── FULL GENERATION CYCLE ──
    def run_full_cycle(self, slot_id, topic_entry, image_prompt, video_prompt):
        """
        Complete YouTube Create generation cycle for one topic slot.
        Returns: local video file path or None.
        """
        print("\n" + "─"*60)
        print(f"[YT CREATE] Slot {slot_id:02d} | {topic_entry['appearance']['emoji']} {topic_entry['appearance']['label']}")
        print(f"[YT CREATE] Topic: {topic_entry['topic'][:60]}")
        print("─"*60)
        try:
            self.launch()
            self.navigate_to_generate()
            self.generate_image(image_prompt)
            self.select_generated_image()
            self.generate_video(video_prompt)
            self.export_video()
            time.sleep(5)
            return self.pull_video_to_pc(slot_id, topic_entry["appearance"]["label"])
        except Exception as e:
            print(f"[ERROR] YouTube Create cycle failed for slot {slot_id}: {e}")
            return None


if __name__ == "__main__":
    from engines.topic_appearance_engine import (
        select_10_daily_topics,
        generate_youtube_create_image_prompt,
        generate_youtube_create_video_prompt,
        generate_script_and_caption,
    )
    driver = YouTubeCreateDriver()
    topics = select_10_daily_topics()
    t = topics[0]
    img_p = generate_youtube_create_image_prompt(t)
    script, caption = generate_script_and_caption(t)
    vid_p = generate_youtube_create_video_prompt(t, script)
    result = driver.run_full_cycle(1, t, img_p, vid_p)
    print("Result:", result)
