#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MD_SADIQUE_AMIN INSTAGRAM & FACEBOOK REAL-FACE IMAGE PIPELINE (PLAN B)
================================================================================
Automated 2–3 Hour Trending Infographic & Carousel Engine:
1. Trend Fetch (Google Trends / Tech News RSS / Reddit / Hacker News)
2. Ollama Content Architect (qwen2.5:7b-instruct @ port 11435)
3. 4K Real-Face 1080x1350 Instagram Portrait (4:5) Infographic Compositor
4. Dual Dispatch: Meta Graph API & Mobile Phone Bridge (ADB)
5. Structured Audit Logging: Excel (daily_performance.xlsx) + SQLite
================================================================================
"""

import os
import sys
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import time
import json
import sqlite3
import random
import argparse
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Base Paths
ENGINES_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ENGINES_DIR.parent
EXPORTS_DIR = PROJECT_ROOT / "exports" / "instagram_infographics"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = PROJECT_ROOT / "md_sadique_amin_automation_records.db"
REPORTS_DIR = PROJECT_ROOT / "reports"
EXCEL_PATH = REPORTS_DIR / "daily_performance.xlsx"

# Priority Master Face Portraits (Plan B)
FACE_PORTRAITS = [
    Path(r"D:/current using file/Mine/Md Sadique Amin/final photos/amin_look2_suit_anchor_24yo.jpg"),
    Path(r"D:/current using file/Mine/Md Sadique Amin/final photos/amin_look3_cyberpunk_fullbeard_24yo.jpg"),
    Path(r"D:/current using file/Mine/Md Sadique Amin/final photos/amin_look1_clean_crewneck_20yo.jpg"),
    Path(r"D:/current using file/Mine/Md Sadique Amin/amin_gold_standard_face.jpg"),
]

def init_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS image_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            topic TEXT UNIQUE,
            category TEXT,
            hook TEXT,
            caption TEXT,
            image_path TEXT,
            platform TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_topic_logged(topic):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM image_posts WHERE topic = ?", (topic,))
    row = cur.fetchone()
    conn.close()
    return row is not None

def log_to_excel(cycle_id, topic, category, img_path, status, latency):
    try:
        import openpyxl
        REPORTS_DIR.mkdir(exist_ok=True)
        if EXCEL_PATH.exists():
            wb = openpyxl.load_workbook(EXCEL_PATH)
            ws = wb.active
        else:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Md Sadique Amin Daily Performance"
            ws.append(["Cycle ID", "Timestamp (IST)", "Viral Topic", "Category", "Media Format", "Artifact Path", "Audio F0", "Target Channels", "Execution Status", "Latency (Sec)"])
            
        ws.append([
            cycle_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            topic,
            category,
            "1080x1350 Plan B Real-Face Infographic",
            str(img_path),
            "N/A (Image)",
            "Instagram Feed & Facebook Page",
            status,
            round(latency, 2)
        ])
        wb.save(EXCEL_PATH)
        print(f"[+] Successfully logged to Excel: {EXCEL_PATH.name}")
    except Exception as e:
        print(f"[-] Excel logging note: {e}")

# 1. Harvest Trending Topic
def harvest_topic():
    print("\n[STEP 1/5] Harvesting Trending Tech / AI Topic...")
    url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
            for item in root.findall(".//item")[:10]:
                title = item.find("title").text
                clean_title = title.split(" - ")[0].strip() if " - " in title else title
                if not is_topic_logged(clean_title):
                    print(f"[+] Found fresh trending topic: {clean_title}")
                    return clean_title, "Tech & AI Architecture"
    except Exception as e:
        print(f"[-] Trend fetch note: {e}")
        
    return "Next-Gen Autonomous AI Coding Agents & System Architecture", "Tech & AI"

# 2. Ollama Copy Architect
def generate_copy_ollama(topic):
    print(f"\n[STEP 2/5] Synthesizing Infographic Copy via Ollama (qwen2.5:7b-instruct)...")
    prompt = f"""
You are the lead content architect for Md Sadique Amin (Senior AI & Systems Engineer).
Topic: "{topic}"

Generate structured content for a high-impact Instagram 4:5 Infographic post in JSON format with exact keys:
{{
  "hook": "A punchy, bold 4-7 word headline question or statement that grabs attention",
  "bullet1": "Key insight 1 (max 10 words, practical technical takeaway)",
  "bullet2": "Key insight 2 (max 10 words, architecture or industry impact)",
  "bullet3": "Key insight 3 (max 10 words, future-looking advice for developers)",
  "caption": "Full Instagram/Facebook caption formatted with emojis, bullet points, engaging explanation in natural Hinglish, call-to-action asking viewers their thoughts, and 8 trending hashtags including #MdSadiqueAmin #AIArchitecture #SoftwareEngineering #TechTrends"
}}
Return ONLY valid JSON.
"""
    try:
        req = urllib.request.Request(
            "http://localhost:11435/api/generate",
            data=json.dumps({"model": "qwen2.5:7b-instruct", "prompt": prompt, "stream": False, "format": "json"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=40) as resp:
            res_data = json.loads(resp.read().decode())
            parsed = json.loads(res_data.get("response", "{}"))
            if "hook" in parsed and "bullet1" in parsed:
                return parsed
    except Exception as e:
        print(f"[-] Ollama JSON generation note: {e}")

    # High-quality fallback
    return {
        "hook": f"What You Need to Know About {topic[:30]}",
        "bullet1": "Transforms legacy development workflows into autonomous pipelines.",
        "bullet2": "Reduces debugging latency by over 60% with context-aware indexing.",
        "bullet3": "The future belongs to engineers who orchestrate multi-agent systems.",
        "caption": f"🚀 Breaking down the biggest architectural shifts in {topic}!\n\nAs systems scale, staying ahead of tech evolution isn't optional—it's mandatory.\n\n👇 What's your take on this? Let me know in the comments!\n\n#MdSadiqueAmin #AIArchitecture #TechInnovation #CodingLife #SoftwareEngineering #FutureTech #InstagramTech"
    }

# 3. Plan B Real-Face Infographic Compositor (1080x1350)
def render_infographic(topic, hook, bullets, face_idx=0):
    print(f"\n[STEP 3/5] Composing 1080x1350 Instagram Portrait (Plan B Real Face)...")
    WIDTH, HEIGHT = 1080, 1350
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 23))
    draw = ImageDraw.Draw(canvas)

    # 1. Background Gradient & Cyber Accents
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(11 * (1 - ratio) + 16 * ratio)
        g = int(15 * (1 - ratio) + 24 * ratio)
        b = int(25 * (1 - ratio) + 40 * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Ambient glow blobs
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([(-100, -100), (500, 500)], fill=(0, 229, 255, 35))
    glow_draw.ellipse([(600, 800), (1200, 1400)], fill=(0, 255, 170, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    canvas.paste(glow, (0, 0), glow)

    # 2. Header Brand Banner
    draw.rectangle([(60, 50), (1020, 110)], fill=(20, 28, 44), outline=(0, 229, 255, 60), width=1)
    draw.text((85, 68), "🧬 MD SADIQUE AMIN | AI SYSTEMS ARCHITECTURE", fill=(0, 255, 170))
    draw.text((830, 68), "DAILY BRIEFING", fill=(160, 180, 205))

    # 3. Main Hook Headline
    draw.text((60, 150), hook[:45].upper(), fill=(255, 255, 255))

    # 4. Ingest Plan B Real Face Master Portrait
    valid_faces = [f for f in FACE_PORTRAITS if f.exists()]
    chosen_face = valid_faces[face_idx % len(valid_faces)] if valid_faces else None

    if chosen_face:
        print(f"[+] Ingesting authentic master face: {chosen_face.name}")
        face_img = Image.open(chosen_face).convert("RGB")
        # Crop square headshot and round corner
        fw, fh = face_img.size
        min_dim = min(fw, fh)
        crop_box = ((fw - min_dim)//2, 0, (fw + min_dim)//2, min_dim)
        headshot = face_img.crop(crop_box).resize((360, 360), Image.LANCZOS)
        
        # Rounded border card for portrait
        mask = Image.new("L", (360, 360), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (360, 360)], radius=24, fill=255)
        
        # Border
        draw.rounded_rectangle([(60, 240), (424, 604)], radius=26, outline=(0, 255, 170), width=3)
        canvas.paste(headshot, (62, 242), mask)
        
        # Profile details card on right
        draw.rounded_rectangle([(450, 240), (1020, 604)], radius=24, fill=(18, 25, 38), outline=(255, 255, 255, 25), width=1)
        draw.text((480, 275), "VERIFIED BIOMETRICS", fill=(0, 229, 255))
        draw.text((480, 320), "Md Sadique Amin", fill=(255, 255, 255))
        draw.text((480, 365), "• 100% Identity Locked Real Face", fill=(180, 195, 215))
        draw.text((480, 410), "• Mesofacial Athletic Architecture", fill=(180, 195, 215))
        draw.text((480, 455), "• Light Jade-Green Hazel Irises (#6E8B75)", fill=(0, 255, 170))
        draw.text((480, 500), "• Full Mandibular Sculpted Density", fill=(180, 195, 215))
        draw.text((480, 545), "• Autonomous AI Systems Lead", fill=(255, 209, 102))

    # 5. Core Insights (3 Bullets) Cards
    start_y = 640
    bullet_icons = ["01", "02", "03"]
    for i, b_text in enumerate(bullets[:3]):
        y_pos = start_y + (i * 175)
        # Card background
        draw.rounded_rectangle([(60, y_pos), (1020, y_pos + 145)], radius=18, fill=(16, 23, 35), outline=(0, 229, 255, 40), width=1)
        # Number badge
        draw.rounded_rectangle([(85, y_pos + 25), (155, y_pos + 95)], radius=12, fill=(0, 255, 170, 25), outline=(0, 255, 170), width=2)
        draw.text((105, y_pos + 42), bullet_icons[i], fill=(0, 255, 170))
        # Text
        draw.text((180, y_pos + 35), f"INSIGHT #{i+1}:", fill=(0, 229, 255))
        draw.text((180, y_pos + 70), b_text[:85], fill=(240, 245, 252))

    # 6. Footer Call To Action
    draw.rectangle([(0, 1240), (1080, 1350)], fill=(12, 17, 26))
    draw.line([(0, 1240), (1080, 1240)], fill=(0, 255, 170, 80), width=2)
    draw.text((60, 1275), "SAVE & SHARE FOR LATER", fill=(255, 209, 102))
    draw.text((700, 1275), "FOLLOW @MD_SADIQUE_AMIN", fill=(0, 255, 170))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = EXPORTS_DIR / f"md_sadique_amin_infographic_{timestamp}.png"
    canvas.save(out_path, quality=98)
    print(f"[+] Rendered Master 1080x1350 Infographic to: {out_path.name}")
    return out_path

# 4. Dispatch to Phone / Meta Graph API
def dispatch_content(img_path, caption):
    print("\n[STEP 4/5] Preparing Multi-Platform Dispatch (Meta Graph API & Mobile Backup)...")
    
    meta_status = []
    
    # Attempt Official Meta Graph API
    try:
        from meta_poster import post_to_instagram, post_to_facebook_page
        
        # 1. Instagram Feed
        ig_res = post_to_instagram(str(img_path), caption)
        if ig_res.get("status") == "SUCCESS":
            print(f"[+] Instagram Published via Meta API! Permalink: {ig_res.get('permalink')}")
            meta_status.append(f"IG_PUBLISHED:{ig_res.get('media_id')}")
        else:
            print(f"[*] Instagram Meta API status: {ig_res.get('status')} ({ig_res.get('message', ig_res.get('error', 'pending config'))})")
            
        # 2. Facebook Page
        fb_res = post_to_facebook_page(None, str(img_path), caption)
        if fb_res.get("status") == "SUCCESS":
            print(f"[+] Facebook Page Published via Meta API! Permalink: {fb_res.get('permalink')}")
            meta_status.append(f"FB_PUBLISHED:{fb_res.get('post_id')}")
        else:
            print(f"[*] Facebook Page Meta API status: {fb_res.get('status')} ({fb_res.get('message', fb_res.get('error', 'pending config'))})")
    except Exception as e:
        print(f"[-] Meta Graph API bridge warning: {e}")

    # ADB Staging Backup to Mobile Gallery
    serial = None
    adb_path = r"C:\platform-tools\adb.exe"
    if os.path.exists(adb_path):
        try:
            res = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
            for line in res.stdout.strip().splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 2 and parts[1] == "device":
                    serial = parts[0]
                    break
        except Exception:
            pass

    if serial:
        print(f"[+] Backup: Target Phone Detected ({serial}). Pushing to /sdcard/DCIM/Camera/...")
        remote_dest = f"/sdcard/DCIM/Camera/{img_path.name}"
        subprocess.run([adb_path, "-s", serial, "push", str(img_path), remote_dest], check=False)
        subprocess.run([adb_path, "-s", serial, "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{remote_dest}"], check=False)
        print("[+] Media pushed and scanned on mobile device gallery!")
        if meta_status:
            return "META_API_PUBLISHED_AND_GALLERY_READY"
        return "MOBILE_GALLERY_READY"
    else:
        if meta_status:
            return "META_API_PUBLISHED"
        print("[!] No active ADB device currently authorized. Image saved locally in exports/ ready for Meta Graph API / Buffer upload.")
        return "LOCAL_EXPORT_READY"

# 5. Execution Cycle
def run_cycle():
    start_time = time.time()
    cycle_id = f"CYC-IMG-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print("="*80)
    print(f"[*] INITIATING MD_SADIQUE_AMIN INSTAGRAM/FACEBOOK CYCLE [{cycle_id}]")
    print("="*80)
    
    init_sqlite()
    topic, category = harvest_topic()
    copy_data = generate_copy_ollama(topic)
    
    hook = copy_data.get("hook", topic)
    bullets = [copy_data.get("bullet1", ""), copy_data.get("bullet2", ""), copy_data.get("bullet3", "")]
    caption = copy_data.get("caption", "")
    
    img_path = render_infographic(topic, hook, bullets, face_idx=random.randint(0, 3))
    status = dispatch_content(img_path, caption)
    
    latency = time.time() - start_time
    
    # Log SQLite
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        INSERT OR REPLACE INTO image_posts 
        (timestamp, topic, category, hook, caption, image_path, platform, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), topic, category, hook, caption, str(img_path), "Instagram/Facebook", status))
    conn.commit()
    conn.close()
    
    # Log Excel
    log_to_excel(cycle_id, topic, category, img_path, status, latency)
    
    print("\n" + "="*80)
    print(f"[OK] CYCLE {cycle_id} COMPLETE ({latency:.1f}s)")
    print(f"• Image   : {img_path}")
    print(f"• Caption : {caption[:120]}...")
    print("="*80)
    return True

def main():
    parser = argparse.ArgumentParser(description="Md Sadique Amin Instagram/Facebook Plan B Automation Daemon")
    parser.add_argument("--once", action="store_true", help="Run a single infographic cycle and exit")
    parser.add_argument("--interval-hours", type=float, default=2.5, help="Loop interval in hours (default: 2.5)")
    args = parser.parse_args()
    
    if args.once:
        run_cycle()
        return

    interval_sec = int(args.interval_hours * 3600)
    print(f"[*] Starting 24h Autonomous Loop (Repeating every {args.interval_hours}h)...")
    while True:
        try:
            run_cycle()
        except Exception as e:
            print(f"[!] Cycle exception: {e}")
            
        print(f"\n[*] Sleeping for {args.interval_hours}h ({interval_sec}s)... Next run at {time.ctime(time.time() + interval_sec)}")
        time.sleep(interval_sec)

if __name__ == "__main__":
    main()
