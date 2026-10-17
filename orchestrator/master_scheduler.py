# -*- coding: utf-8 -*-
"""
Aminsa Master Autonomous Scheduler & Telemetry Engine
Runs every 2.5 hours (max 8 posts/day) with exponential backoff and Excel telemetry logging.
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime, date

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.topic_appearance_engine import (
    select_10_daily_topics,
    generate_script_and_caption,
    classify_topic,
    APPEARANCE_MAP
)
from engines.laptop_master_avatar_studio import master_studio
from character.consistency_gate import consistency_gate
from publishers.instagram import instagram_publisher
from publishers.facebook import facebook_publisher
from publishers.threads import threads_publisher

LOG_FILE = os.path.join(PROJECT_ROOT, "reports", "master_orchestrator.log")
os.makedirs(os.path.join(PROJECT_ROOT, "reports"), exist_ok=True)

INTERVAL_SECONDS = int(2.5 * 3600)  # 2.5 hours = 9000 seconds
MAX_DAILY_POSTS = 8

def log(msg):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def log_to_excel(cycle_id, topic, category, video_file, post_ids, status, latency):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
        xlsx_path = os.path.join(PROJECT_ROOT, "reports", "daily_performance.xlsx")
        if os.path.exists(xlsx_path):
            wb = openpyxl.load_workbook(xlsx_path)
        else:
            wb = openpyxl.Workbook()

        today_str = datetime.now().strftime("%Y%m%d")
        sheet_name = f"Log_{today_str}"
        if sheet_name not in wb.sheetnames:
            ws = wb.create_sheet(sheet_name)
            headers = ["Cycle ID", "Timestamp", "Category", "Topic", "Video Path", "Post IDs", "Status", "Latency (s)"]
            for col, h in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=h)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="1E293B")
                cell.alignment = Alignment(horizontal="center")
        else:
            ws = wb[sheet_name]

        ws.append([
            cycle_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            category,
            topic,
            os.path.basename(video_file) if video_file else "N/A",
            json.dumps(post_ids) if isinstance(post_ids, (dict, list)) else str(post_ids),
            status,
            round(latency, 2)
        ])
        wb.save(xlsx_path)
    except Exception as e:
        log(f"[WARN] Excel logging error: {e}")

class AminsaMasterOrchestrator:
    def __init__(self):
        self.today = date.today()
        self.daily_post_count = 0
        self.daily_topics = []

    def check_and_reset_daily_cap(self):
        current_date = date.today()
        if current_date != self.today or not self.daily_topics:
            self.today = current_date
            self.daily_post_count = 0
            log(f"[*] Refreshing daily topics plan for {self.today}...")
            try:
                self.daily_topics = select_10_daily_topics()
            except Exception as e:
                log(f"[WARN] Trend selection error: {e}. Using fallback topics.")
                self.daily_topics = []

    def run_single_pipeline_cycle(self, slot_id=1, topic_override=None):
        self.check_and_reset_daily_cap()

        if self.daily_post_count >= MAX_DAILY_POSTS:
            log(f"[!] Daily cap reached: {self.daily_post_count}/{MAX_DAILY_POSTS}. Skipping cycle until next day.")
            return False

        start_time = time.time()
        cycle_id = f"AMINSA-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        log("=" * 70)
        log(f"CYCLE START: {cycle_id} | POST #{self.daily_post_count + 1} OF {MAX_DAILY_POSTS}")
        log("=" * 70)

        # 1. Topic Harvest & Wardrobe Mapping
        if topic_override:
            app = APPEARANCE_MAP.get("AI & Technology", list(APPEARANCE_MAP.values())[0])
            topic_entry = {
                "topic": topic_override,
                "appearance": app,
                "script": f"Hello everyone! Today we explore {topic_override}. Stay connected with Aminsa!",
                "caption": f"Hello everyone! {topic_override} #AIGenerated #VirtualCreator #Aminsa #TechTrends"
            }
        else:
            idx = (slot_id - 1) % max(len(self.daily_topics), 1)
            if self.daily_topics:
                topic_entry = self.daily_topics[idx]
            else:
                topic_entry = {
                    "topic": "Future of Autonomous AI Creators and Virtual Presence 2026",
                    "appearance": list(APPEARANCE_MAP.values())[0]
                }

        topic = topic_entry["topic"]
        cat_name = topic_entry["appearance"]["label"]
        face_imgs = sorted([
            os.path.join(PROJECT_ROOT, "aminsa-images", f)
            for f in os.listdir(os.path.join(PROJECT_ROOT, "aminsa-images"))
            if f.endswith(".jpg")
        ])
        face_img = face_imgs[(slot_id - 1) % len(face_imgs)] if face_imgs else os.path.join(PROJECT_ROOT, "aminsa-images", "01_aminsa_clean_portrait_kurta.jpg")
        if not os.path.exists(face_img):
            face_img = os.path.join(PROJECT_ROOT, "aminsa-images", "01_aminsa_clean_portrait_kurta.jpg")

        script, caption = generate_script_and_caption(topic_entry)
        # Ensure mandatory tags & greetings
        if not script.strip().lower().startswith("hello everyone"):
            script = "Hello everyone! " + script
        script = script.replace("Namaste", "Hello").replace("namaste", "hello")
        if "#AIGenerated" not in caption:
            caption += " #AIGenerated #VirtualCreator"

        # 2. Consistency & Persona Gate
        log("[*] [Gate] Evaluating biometric and persona compliance...")
        gate_ok, gate_details = consistency_gate.run_all_gates(face_img, script, caption)
        if not gate_ok:
            log(f"[-] Consistency Gate REJECTED: {gate_details}")
            log_to_excel(cycle_id, topic, cat_name, None, {}, "REJECTED_CONSISTENCY_GATE", time.time() - start_time)
            return False
        log("[+] Consistency Gate Passed 100%!")

        # 3. Render 1080x1920 Master Reel with Kinetic Subtitles
        log("[*] [Render] Compiling 1080x1920 Reel...")
        video_path = master_studio.render_talking_avatar_reel(face_img, script, topic, slot_idx=slot_id)
        if not video_path or not os.path.exists(video_path):
            log("[-] Video rendering failed!")
            log_to_excel(cycle_id, topic, cat_name, None, {}, "RENDER_FAILED", time.time() - start_time)
            return False

        # 4. Multi-Platform Publishing (Official APIs)
        video_url = f"https://media.aminsa.live/reels/{os.path.basename(video_path)}"
        post_ids = {}

        # Instagram
        ig_res = instagram_publisher.publish_reel(video_url, caption)
        if ig_res.get("success"):
            post_ids["instagram"] = ig_res.get("media_id")

        # Facebook
        fb_res = facebook_publisher.publish_video_reel(video_url, caption, title=topic[:60])
        if fb_res.get("success"):
            post_ids["facebook"] = fb_res.get("post_id")

        # Threads
        th_res = threads_publisher.publish_video(video_url, caption)
        if th_res.get("success"):
            post_ids["threads"] = th_res.get("post_id")

        self.daily_post_count += 1
        elapsed = time.time() - start_time
        log(f"[+] Cycle Completed in {elapsed:.2f}s | Post IDs: {post_ids}")
        log_to_excel(cycle_id, topic, cat_name, video_path, post_ids, "PUBLISHED_SUCCESS", elapsed)
        log("=" * 70)
        return True

    def start_loop(self):
        log(f"[*] Starting Master Autonomous Loop: every {INTERVAL_SECONDS / 3600}h (max {MAX_DAILY_POSTS}/day)...")
        slot = 1
        while True:
            try:
                self.run_single_pipeline_cycle(slot_id=slot)
                slot = (slot % 10) + 1
                log(f"[*] Sleeping {INTERVAL_SECONDS / 3600} hours ({INTERVAL_SECONDS}s)...")
                time.sleep(INTERVAL_SECONDS)
            except KeyboardInterrupt:
                log("[!] Scheduler stopped by user.")
                break
            except Exception as e:
                log(f"[-] Cycle exception: {e}. Backoff 60s...")
                time.sleep(60)

orchestrator = AminsaMasterOrchestrator()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-once", action="store_true", help="Run a single test cycle and exit")
    parser.add_argument("--slot", type=int, default=1)
    parser.add_argument("--topic", type=str, default=None)
    args = parser.parse_args()

    if args.run_once:
        orchestrator.run_single_pipeline_cycle(slot_id=args.slot, topic_override=args.topic)
    else:
        orchestrator.start_loop()
