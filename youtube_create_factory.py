"""
Md Sadique Amin YouTube Create Master Factory
======================================
FULL AUTONOMOUS 24-HOUR PIPELINE:

Schedule: 10 videos × 2.4-hour gaps across 24 hours
Times:    06:00 → 08:24 → 10:48 → 13:12 → 15:36
          18:00 → 20:24 → 22:48 → 01:12 → 03:36

Each Cycle:
  [1] Auto-select trending topic (from Google News India RSS)
  [2] Classify category → Set Md Sadique Amin dynamic appearance
  [3] Generate YouTube Create IMAGE prompt (Md Sadique Amin visual look)
  [4] ADB → Type prompt into YouTube Create → Wait → Image generated
  [5] ADB → Generate TALKING AVATAR VIDEO from generated image
  [6] Pull video from phone to PC
  [7] Auto-post to ALL Md Sadique Amin accounts:
        Instagram Reels → Facebook Page → Threads → YouTube Shorts
  [8] Log to reports/daily_performance.xlsx
  [9] Sleep 2.4 hours → Next cycle
"""

import os
import sys
import time
import asyncio
import json
from datetime import datetime, timedelta

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# ──────────────────────────────────────────
# SCHEDULE CONFIG
# ──────────────────────────────────────────
TOTAL_DAILY_VIDEOS = 10
GAP_HOURS = 24 / TOTAL_DAILY_VIDEOS          # 2.4 hours
GAP_SECONDS = int(GAP_HOURS * 3600)          # 8640 seconds

# 10 slot times starting from 6:00 AM IST
SLOT_START_HOUR = 6
DAILY_SLOTS = []
for i in range(TOTAL_DAILY_VIDEOS):
    delta_minutes = int(i * GAP_HOURS * 60)
    h = (SLOT_START_HOUR * 60 + delta_minutes) // 60 % 24
    m = (SLOT_START_HOUR * 60 + delta_minutes) % 60
    DAILY_SLOTS.append(f"{h:02d}:{m:02d}")

# ──────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────
LOG_FILE = os.path.join(PROJECT_ROOT, "reports", "youtube_create_factory.log")
os.makedirs(os.path.join(PROJECT_ROOT, "reports"), exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

# ──────────────────────────────────────────
# EXCEL TELEMETRY LOGGER
# ──────────────────────────────────────────
def log_to_excel(slot_id, topic, category, appearance_label, image_prompt, 
                  video_path, publish_status, elapsed):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
        xlsx_path = os.path.join(PROJECT_ROOT, "reports", "daily_performance.xlsx")
        if os.path.exists(xlsx_path):
            wb = openpyxl.load_workbook(xlsx_path)
        else:
            wb = openpyxl.Workbook()
        
        sheet_name = f"YTCreate_{datetime.now().strftime('%Y%m%d')}"
        if sheet_name not in wb.sheetnames:
            ws = wb.create_sheet(sheet_name)
            headers = ["Slot", "Time", "Category", "Appearance", "Topic", 
                       "Image Prompt (first 100)", "Video File", "Status", "Latency(s)"]
            for col, h in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=h)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="7B2D8B")
                cell.alignment = Alignment(horizontal="center")
        else:
            ws = wb[sheet_name]
        
        row = ws.max_row + 1
        ws.append([
            slot_id,
            datetime.now().strftime("%H:%M:%S"),
            category,
            appearance_label,
            topic[:80],
            image_prompt[:100],
            os.path.basename(video_path) if video_path else "FAILED",
            publish_status,
            round(elapsed, 1)
        ])
        wb.save(xlsx_path)
        log(f"[+] Excel log updated: {xlsx_path}")
    except ImportError:
        log("[-] openpyxl not installed. Skipping Excel log.")
    except Exception as e:
        log(f"[-] Excel log error: {e}")

# ──────────────────────────────────────────
# YOUTUBE SHORTS UPLOAD VIA ADB
# ──────────────────────────────────────────
def upload_to_youtube_shorts_via_adb(serial, video_local_path, title, description):
    """
    Upload video to YouTube Shorts via ADB by:
    1. Pushing video to phone
    2. Opening YouTube app → Camera / Upload flow
    3. Selecting video → Adding title & description → Publishing as Short
    """
    import subprocess
    from mobile_app_controller import ADB_EXE, push_media_to_phone

    def adb(*args):
        return subprocess.run([ADB_EXE, "-s", serial] + list(args),
                              capture_output=True, text=True)
    def tap(x, y, d=1.5):
        adb("shell", "input", "tap", str(x), str(y))
        time.sleep(d)

    log("[*] Uploading to YouTube Shorts via ADB...")
    
    # Push video to phone first
    push_media_to_phone(video_local_path)
    time.sleep(2)
    
    # Open YouTube app
    adb("shell", "am", "start", "-n",
        "com.google.android.youtube/com.google.android.youtube.HomeActivity")
    time.sleep(3)
    
    # Tap '+' create button (bottom center)
    tap(360, 1480, 2)
    # Tap "Upload a video"
    tap(360, 1200, 2)
    # Select most recent video (first in gallery)
    tap(180, 400, 2)
    # Tap Next
    tap(641, 1500, 3)
    # Add title
    adb("shell", "input", "tap", "360", "350")
    time.sleep(1)
    safe_title = title.replace("'", "").replace('"', "")[:90]
    adb("shell", f"input text {safe_title.replace(' ', '%s')}")
    time.sleep(1)
    # Make it a Short (toggle if needed)
    tap(360, 900, 1)
    # Tap Upload / Publish
    tap(641, 1500, 3)
    log("[+] YouTube Shorts upload command executed.")
    return True

# ──────────────────────────────────────────
# SINGLE SLOT EXECUTION
# ──────────────────────────────────────────
def run_single_slot(slot_id, topic_entry, topics_remaining):
    """
    Full pipeline for one slot:
    Topic → YouTube Create Image + Video → Multi-platform publish
    """
    from engines.topic_appearance_engine import (
        generate_youtube_create_image_prompt,
        generate_youtube_create_video_prompt,
        generate_script_and_caption,
    )
    from engines.youtube_create_adb_driver import YouTubeCreateDriver
    from mobile_app_controller import get_adb_device
    from post_reel_via_phone_adb import publish_latest_reel_multi_platform

    start_time = time.time()
    cycle_id = f"YTC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    log("=" * 70)
    log(f"SLOT {slot_id:02d}/10 | CYCLE: {cycle_id}")
    log(f"TOPIC    : {topic_entry['topic'][:65]}")
    log(f"CATEGORY : {topic_entry['appearance']['emoji']} {topic_entry['appearance']['label']}")
    log(f"REMAINING: {len(topics_remaining)} slots after this")
    log("=" * 70)

    # [1] Generate prompts
    image_prompt = generate_youtube_create_image_prompt(topic_entry)
    script, caption = generate_script_and_caption(topic_entry)
    video_prompt = generate_youtube_create_video_prompt(topic_entry, script)
    
    log(f"[Step 1/4] Prompts ready. Image: {len(image_prompt)} chars | Video: {len(video_prompt)} chars")

    # [2] YouTube Create: Generate image + video via ADB
    video_path = None
    try:
        log("[Step 2/4] Launching YouTube Create ADB Driver...")
        driver = YouTubeCreateDriver()
        video_path = driver.run_full_cycle(slot_id, topic_entry, image_prompt, video_prompt)
        if video_path:
            log(f"[+] Video ready: {video_path}")
        else:
            log("[-] Video not pulled. Will attempt to use latest phone gallery file.")
    except Exception as e:
        log(f"[-] YouTube Create ADB error: {e}")

    # [3] Multi-Platform Publish (Instagram + Facebook + Threads)
    publish_status = "PENDING"
    published_ig = False
    if video_path or True:  # Proceed even if pull failed (video may be in gallery)
        log("[Step 3/4] Publishing to Instagram Reels + Facebook Page + Threads...")
        try:
            published_ig = publish_latest_reel_multi_platform(caption)
            if published_ig:
                publish_status = "PUBLISHED_IG_FB_THREADS"
                log("[+] Successfully posted: Instagram Reels + Facebook Page + Threads!")
        except Exception as e:
            log(f"[-] IG/FB/Threads publish error: {e}")
            publish_status = "IG_PUBLISH_ERROR"

    # [4] YouTube Shorts upload
    try:
        serial, state = get_adb_device()
        if state == "device" and video_path:
            yt_title = f"{topic_entry['topic'][:80]} | Md Sadique Amin"
            yt_desc = f"{caption}\n\n#Shorts #Md Sadique Amin #AICreator"
            upload_to_youtube_shorts_via_adb(serial, video_path, yt_title, yt_desc)
            publish_status += "_YT_SHORTS"
            log("[+] YouTube Shorts upload executed!")
    except Exception as e:
        log(f"[-] YouTube Shorts upload error: {e}")

    # [5] Log to Excel
    elapsed = time.time() - start_time
    log_to_excel(
        slot_id=slot_id,
        topic=topic_entry["topic"],
        category=topic_entry["category"],
        appearance_label=topic_entry["appearance"]["label"],
        image_prompt=image_prompt,
        video_path=video_path or "",
        publish_status=publish_status,
        elapsed=elapsed
    )

    log(f"[SLOT {slot_id:02d} COMPLETE] Status: {publish_status} | Time: {elapsed:.0f}s")
    return publish_status

# ──────────────────────────────────────────
# WAIT UNTIL NEXT SLOT TIME
# ──────────────────────────────────────────
def wait_until_slot(slot_index):
    """Wait until the scheduled slot time (or sleep gap_seconds if already past)."""
    now = datetime.now()
    target_str = DAILY_SLOTS[slot_index]
    target_h, target_m = map(int, target_str.split(":"))
    target = now.replace(hour=target_h, minute=target_m, second=0, microsecond=0)
    
    if target <= now:
        target += timedelta(days=1)
    
    wait_sec = (target - now).total_seconds()
    if wait_sec > 0 and wait_sec < GAP_SECONDS * 1.5:
        log(f"[*] Waiting {wait_sec/60:.1f} min until slot time {target_str}...")
        time.sleep(wait_sec)
    else:
        # Just sleep the gap
        log(f"[*] Sleeping {GAP_SECONDS/3600:.2f} hours until next slot...")
        time.sleep(GAP_SECONDS)

# ──────────────────────────────────────────
# MAIN 24-HOUR FACTORY LOOP
# ──────────────────────────────────────────
def run_24h_factory():
    """
    Main infinite loop:
    - Fetches 10 topics at start of each day
    - Runs 10 slots with 2.4-hour gaps
    - Repeats every 24 hours
    """
    from engines.topic_appearance_engine import select_10_daily_topics
    
    log("=" * 70)
    log("MD_SADIQUE_AMIN YOUTUBE CREATE MASTER FACTORY — 24H AUTONOMOUS MODE")
    log(f"Schedule: {TOTAL_DAILY_VIDEOS} videos/day | Gap: {GAP_HOURS:.1f}h each")
    log(f"Slots: {' | '.join(DAILY_SLOTS)}")
    log("=" * 70)

    day_count = 0
    while True:
        day_count += 1
        date_str = datetime.now().strftime("%Y-%m-%d")
        log(f"\n{'='*70}")
        log(f"DAY {day_count} | {date_str} — FETCHING FRESH DAILY TOPICS")
        log(f"{'='*70}")

        # Fetch 10 fresh topics for the day
        try:
            daily_topics = select_10_daily_topics()
            log(f"[+] {len(daily_topics)} topics selected for today:")
            for i, t in enumerate(daily_topics):
                log(f"  Slot {i+1:02d}: {t['appearance']['emoji']} [{t['appearance']['label']}] {t['topic'][:50]}")
        except Exception as e:
            log(f"[-] Topic fetch error: {e}. Using default topics.")
            daily_topics = _get_default_topics()

        # Save today's plan
        plan_file = os.path.join(PROJECT_ROOT, "reports", f"daily_plan_{date_str}.json")
        try:
            with open(plan_file, "w", encoding="utf-8") as f:
                json.dump([{"slot": i+1, "topic": t["topic"], "category": t["category"]}
                           for i, t in enumerate(daily_topics)], f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        # Run all 10 slots
        results = []
        for slot_idx in range(TOTAL_DAILY_VIDEOS):
            slot_id = slot_idx + 1
            topic = daily_topics[slot_idx] if slot_idx < len(daily_topics) else daily_topics[0]
            remaining = daily_topics[slot_idx+1:]
            
            log(f"\n[*] Starting Slot {slot_id}/10 at {datetime.now().strftime('%H:%M:%S')}")
            status = run_single_slot(slot_id, topic, remaining)
            results.append({"slot": slot_id, "status": status, "topic": topic["topic"][:50]})
            
            if slot_idx < TOTAL_DAILY_VIDEOS - 1:
                log(f"[*] Slot {slot_id} done. Waiting {GAP_HOURS:.1f}h before next slot...")
                wait_until_slot(slot_idx + 1)

        # Day summary
        log(f"\n{'='*70}")
        log(f"DAY {day_count} COMPLETE — {len(results)} slots executed")
        success = sum(1 for r in results if "PUBLISHED" in r.get("status", ""))
        log(f"Published: {success}/{len(results)} | Next refresh in ~24h")
        log(f"{'='*70}")

        # Wait remainder of the day before next refresh
        now = datetime.now()
        next_day_start = (now + timedelta(days=1)).replace(
            hour=SLOT_START_HOUR, minute=0, second=0, microsecond=0)
        sleep_left = max(0, (next_day_start - now).total_seconds())
        if sleep_left > 60:
            log(f"[*] Sleeping {sleep_left/3600:.1f}h until tomorrow's 06:00...")
            time.sleep(sleep_left)

def _get_default_topics():
    """Emergency fallback topics if RSS fetch fails."""
    from engines.topic_appearance_engine import APPEARANCE_MAP
    defaults = [
        ("AI tools transforming Indian education in 2025", "tech"),
        ("Diwali fashion trends — what's stylish this season", "festival"),
        ("Morning routines of successful young Indians", "personal"),
        ("India's EV revolution — what you need to know", "tech"),
        ("Navratri garba outfit ideas for 2025", "festival"),
        ("Smart money habits for Gen Z in India", "finance"),
        ("Travel destinations you must visit in India", "travel"),
        ("Best street food cities in India right now", "food"),
        ("Home workout routines for working professionals", "health"),
        ("Career tips for fresh graduates in India", "education"),
    ]
    return [{"topic": t, "category": c, "appearance": APPEARANCE_MAP[c]} for t, c in defaults]

# ──────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Md Sadique Amin YouTube Create Master Factory")
    parser.add_argument("--test-slot", type=int, default=0,
                        help="Test a single slot immediately (1-10). 0 = run full 24h loop")
    parser.add_argument("--preview-topics", action="store_true",
                        help="Preview today's 10 topics without running")
    args = parser.parse_args()

    if args.preview_topics:
        from engines.topic_appearance_engine import select_10_daily_topics, generate_youtube_create_image_prompt, generate_script_and_caption
        topics = select_10_daily_topics()
        print("\n" + "="*70)
        print(f"TODAY'S 10-SLOT YOUTUBE CREATE SCHEDULE ({datetime.now().strftime('%Y-%m-%d')})")
        print("="*70)
        for i, t in enumerate(topics):
            slot_time = DAILY_SLOTS[i]
            img_p = generate_youtube_create_image_prompt(t)
            script, caption = generate_script_and_caption(t)
            print(f"\nSlot {i+1:02d} @ {slot_time} | {t['appearance']['emoji']} {t['appearance']['label']}")
            print(f"  Topic      : {t['topic'][:65]}")
            print(f"  Outfit     : {t['appearance']['outfit'][:60]}")
            print(f"  Hair       : {t['appearance']['hair']}")
            print(f"  Background : {t['appearance']['background'][:60]}")
            print(f"  Img Prompt : {img_p[:80]}...")
            print(f"  Script     : {script[:80]}...")

    elif args.test_slot > 0:
        from engines.topic_appearance_engine import select_10_daily_topics
        topics = select_10_daily_topics()
        slot = min(args.test_slot, len(topics)) - 1
        run_single_slot(args.test_slot, topics[slot], topics[slot+1:])

    else:
        run_24h_factory()
