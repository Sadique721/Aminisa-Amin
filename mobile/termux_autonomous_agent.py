#!/usr/bin/env python3
"""
Md Sadique Amin Standalone Mobile Agent for Termux (Android 15 / OPPO A78 5G)
Runs 100% autonomously on your smartphone, even when the laptop is completely powered OFF.
Zero-cost, open-source stack.
"""

import os
import sys
import time
import random
import datetime
import asyncio
import urllib.request
import xml.etree.ElementTree as ET
import subprocess

try:
    import edge_tts
except ImportError:
    print("[!] Please run 'pip install edge-tts' in Termux")

# Configuration
CYCLE_INTERVAL_HOURS = 2.5
JITTER_MINUTES = 20
VOICE_NAME = "hi-IN-SwaraNeural"

def fetch_live_trend():
    print("[*] [Termux] Fetching live trending topics from Google Trends India...")
    url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
            items = root.findall(".//item")
            if items:
                title = items[0].find("title").text
                return title
    except Exception as e:
        print(f"[-] [Termux] Trend fetch error: {e}")
    return "Next-Gen AI & Modern Lifestyle Aesthetics"

async def synthesize_speech(text, output_file="current_speech.mp3"):
    print(f"[*] [Termux] Synthesizing speech via Edge-TTS ({VOICE_NAME} @ 224Hz)...")
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE_NAME,
        rate="+0%",
        pitch="+0Hz"
    )
    await communicate.save(output_file)
    print(f"[+] [Termux] Audio synthesized: {output_file}")
    return output_file

def notify_user(title, message):
    try:
        subprocess.run(["termux-notification", "--title", title, "--content", message], check=False)
    except Exception:
        pass

def run_single_cycle():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}\n🚀 [Termux] Executing Autonomous Md Sadique Amin Cycle: {now_str}\n{'='*60}")
    
    # 1. Harvest Trend
    trend = fetch_live_trend()
    print(f"[+] Current Target Trend: {trend}")
    
    # 2. Build Script
    script = (
        f"Hello everyone! Main hoon Md Sadique Amin. Aaj ka bada update: {trend}. "
        "Technology aur hamari lifestyle kis tezi se badal rahi hai, yeh dekhna waqai inspiring hai. "
        "Aapki is par kya raye hai? Follow karein aur comment me batayein!"
    )
    
    # 3. Synthesize Voice
    asyncio.run(synthesize_speech(script, "mobile_speech.mp3"))
    
    # 4. Notify on Android
    notify_user("Md Sadique Amin Autonomous Agent", f"Rendered asset for trend: {trend[:40]}...")
    print("[✓] [Termux] Cycle successfully completed and logged!")

def main_loop():
    print("=" * 60)
    print("🤖 MD_SADIQUE_AMIN STANDALONE MOBILE DAEMON ACTIVATED (TERMUX)")
    print("=" * 60)
    print(f"[*] Interval: Every {CYCLE_INTERVAL_HOURS} hours (± {JITTER_MINUTES} mins jitter)")
    
    # Ensure wakelock so Termux doesn't sleep
    try:
        subprocess.run(["termux-wake-lock"], check=False)
        print("[+] Termux wake-lock acquired (Process will run with screen OFF)")
    except Exception:
        pass

    while True:
        try:
            run_single_cycle()
        except Exception as e:
            print(f"[!] [Termux] Cycle error: {e}")
            
        # Calculate jittered sleep time
        jitter = random.randint(-JITTER_MINUTES * 60, JITTER_MINUTES * 60)
        sleep_seconds = int(CYCLE_INTERVAL_HOURS * 3600 + jitter)
        sleep_hrs = sleep_seconds / 3600
        print(f"[*] Sleeping for {sleep_hrs:.2f} hours until next autonomous cycle...\n")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        run_single_cycle()
    else:
        main_loop()
