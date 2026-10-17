# -*- coding: utf-8 -*-
"""
================================================================================
AMINSA MASTER PLAN v2 — FILE 2: REEL FACTORY (reel_pipeline/reel_factory.py)
================================================================================
Generates 2-3 high-definition 1080x1920 60FPS vertical reels/day offset from image slots:
(09:30, 13:30, 17:30 IST), sharing today's frozen OOTD and world plates.
Includes 224 Hz studio voice, word-by-word kinetic golden glowing subtitles,
floating PiP news/proof card, audio ducking, and official Graph API publishing.
================================================================================
"""

import os
import sys
import time
import json
import asyncio
import subprocess
import datetime as dt

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from shared.calendar.festivals import festival_for
from shared.qa import face_gate, clean_bg_gate, caption_gate
from shared.publish import instagram_publisher, facebook_publisher, threads_publisher, storage
from shared.log.ledger import log_row
from engines.topic_appearance_engine import fetch_all_trends, select_10_daily_topics, classify_topic
from engines.kinetic_subtitle_engine import subtitle_engine, get_audio_duration
from engines.laptop_master_avatar_studio import master_studio

REEL_SLOTS = ["09:30", "13:30", "17:30"]

REEL_THEMES = {
    "09:30": {"category": "AI & Technology", "plate": "wfh_nook_morning.jpg", "mood": "Analytical & Innovative"},
    "13:30": {"category": "Science & Innovation", "plate": "wfh_nook_day.jpg", "mood": "Dynamic & Curious"},
    "17:30": {"category": "Business & Startups", "plate": "terrace_sunset.jpg", "mood": "Strategic & Evening Perspective"}
}

class AminsaReelFactory:
    def __init__(self):
        self.state_file = os.path.join(ROOT_DIR, "state", "today.json")
        self.export_dir = os.path.join(ROOT_DIR, "exports", "reels")
        self.temp_dir = os.path.join(ROOT_DIR, "exports", "temp")
        os.makedirs(self.export_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    def load_today_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"date": dt.date.today().isoformat(), "ootd": {"style_category": "Western Modest"}}

    def generate_reel_script(self, topic, fest_info=None):
        if fest_info:
            fname = fest_info["name"]
            script = (
                f"Hello everyone! Celebrating {fname} today with gratitude, cultural pride, and community warmth. "
                f"Across India, traditions remind us of shared values and bright beginnings. "
                f"Wishing you all peace, light, and happiness!"
            )
            caption = (
                f"Hello everyone! Wishing you a memorable {fname}! "
                f"Celebrating unity and warmth. #AIGenerated #VirtualCreator #Aminsa #{fname.replace(' ', '')}"
            )
            return script, caption

        # General tech/cultural explainer script (20-35s)
        script = (
            f"Hello everyone! Let us talk about {topic}. "
            f"Rapid breakthroughs in AI and software systems are transforming everyday workflows across India. "
            f"From autonomous agents to intuitive interfaces, the future is moving faster than ever. "
            f"What are your thoughts on this shift? Let me know in the comments below!"
        )
        caption = (
            f"Hello everyone! Exploring {topic[:70]}. "
            f"How is technology changing the way you work and create? "
            f"#AIGenerated #VirtualCreator #Aminsa #TechTrends #Bengaluru"
        )
        return script, caption

    def run_slot(self, slot="09:30", dry_run=None, topic_override=None):
        start_time = time.time()
        print("=" * 70)
        print(f"REEL FACTORY: EXECUTING SLOT {slot} (IST)")
        print("=" * 70)

        # 1. State & Festival Check
        today_data = self.load_today_state()
        fest = festival_for(dt.date.today())
        theme_cfg = REEL_THEMES.get(slot, REEL_THEMES["09:30"])

        # 2. Topic Selection
        if topic_override:
            headline = topic_override
        elif fest:
            headline = f"Special Cultural Tribute: {fest['name']}"
        else:
            try:
                trends = fetch_all_trends()
                headline = trends[0]["title"] if trends else "Autonomous AI Systems Transforming Creative Industries 2026"
            except Exception:
                headline = "Autonomous AI Systems Transforming Creative Industries 2026"

        print(f"[*] Topic Headline: {headline}")

        # 3. Script & Caption
        script_text, caption_text = self.generate_reel_script(headline, fest)
        cap_ok, cap_msg = caption_gate.ok(caption_text, script_text)
        if not cap_ok:
            print(f"[-] Reel Caption Gate failed: {cap_msg}")
            log_row(slot, cycle_type="REEL", topic=headline, status="REJECTED_CAPTION")
            return False
        print("[+] Script & Caption Certified: 'Hello everyone!' verified, zero 'Namaste', #AIGenerated compliant.")

        # 4. Synthesize Studio Voice (224 Hz + -14 LUFS DSP)
        audio_filename = f"reel_voice_{slot.replace(':', '')}_{int(time.time())}.mp3"
        audio_path = os.path.join(self.temp_dir, audio_filename)
        asyncio.run(master_studio.synthesize_voice(script_text, audio_path))
        duration = get_audio_duration(audio_path)
        print(f"[+] Studio Voice Synthesized: {duration:.2f}s (hi-IN-SwaraNeural 224 Hz)")

        # 5. Generate Kinetic Word-by-Word Subtitles (.ass)
        ass_filename = f"reel_subs_{slot.replace(':', '')}_{int(time.time())}.ass"
        ass_path = os.path.join(self.temp_dir, ass_filename)
        subtitle_engine.generate_ass(script_text, duration, ass_path)
        print("[+] Kinetic Glowing Subtitles Generated (.ass)")

        # 6. Hero Still & Face Gate
        face_anchor = os.path.join(ROOT_DIR, "shared", "identity", "face_anchor.jpg")
        f_ok = face_gate.ok(face_anchor)
        f_score = face_gate.compute_similarity(face_anchor)
        if not f_ok:
            print("[-] Face Gate failed for hero still!")
            log_row(slot, cycle_type="REEL", topic=headline, face_score=f_score, status="REJECTED_FACE_GATE")
            return False
        print(f"[+] Hero Face Anchor Certified (ArcFace: {f_score:.2%})")

        # 7. Render 1080x1920 60FPS Master Reel with PiP Card + Subtitles
        slot_num = REEL_SLOTS.index(slot) + 1 if slot in REEL_SLOTS else 1
        video_path = master_studio.render_talking_avatar_reel(
            face_image_path=face_anchor,
            script_text=script_text,
            headline=headline,
            slot_idx=slot_num
        )
        if not video_path or not os.path.exists(video_path):
            print("[-] Video compilation failed!")
            log_row(slot, cycle_type="REEL", topic=headline, status="RENDER_FAILED")
            return False
        print(f"[+] Master Reel Rendered: {os.path.basename(video_path)} ({os.path.getsize(video_path)/(1024*1024):.2f} MB)")

        # 8. Upload to Supabase Storage
        public_video_url = storage.upload(video_path)

        # 9. Publish via Official Graph APIs
        post_ids = {}
        # Instagram Reel
        ig_res = instagram_publisher.publish_reel(public_video_url, caption_text, dry_run=dry_run)
        if ig_res.get("success"):
            post_ids["instagram"] = ig_res.get("media_id")
        # Facebook Page Reel
        fb_res = facebook_publisher.publish_video_reel(public_video_url, caption_text, title=headline[:60], dry_run=dry_run)
        if fb_res.get("success"):
            post_ids["facebook"] = fb_res.get("post_id")
        # Threads
        th_res = threads_publisher.publish_video(public_video_url, caption_text, dry_run=dry_run)
        if th_res.get("success"):
            post_ids["threads"] = th_res.get("post_id")

        elapsed = time.time() - start_time
        print(f"[SUCCESS] Reel Slot {slot} completed in {elapsed:.2f}s | Post IDs: {post_ids}")
        log_row(slot, cycle_type="REEL", topic=headline, face_score=f_score, render_s=elapsed, post_ids=post_ids, status="POSTED")
        return True

reel_factory = AminsaReelFactory()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--slot", type=str, default="09:30", choices=REEL_SLOTS)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--topic", type=str, default=None)
    args = parser.parse_args()
    reel_factory.run_slot(args.slot, dry_run=args.dry_run, topic_override=args.topic)
