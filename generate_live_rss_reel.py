"""
Md Sadique Amin Live RSS Trending Reel Generator
=========================================
1. Fetches top trending topic from Google News India RSS
2. Uses newly generated Md Sadique Amin Balcony Selfie + Kurta Benchmark
3. Synthesizes 224 Hz Edge-TTS Studio Audio (Zero Namaste)
4. Generates dynamic Facebook-style Floating Proof Card Overlay
5. Composites 1080x1920 9:16 Full HD Reel
6. Syncs across PC and Mobile via ADB
"""

import os
import sys
import time
import asyncio
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import imageio_ffmpeg

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "exports", "reels")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BENCHMARK_SELFIE = os.path.join(PROJECT_ROOT, "md_sadique_amin-images", "md_sadique_amin_live_selfie_balcony.jpg")
BENCHMARK_KURTA = os.path.join(PROJECT_ROOT, "md_sadique_amin-images", "01_md_sadique_amin_clean_portrait_kurta.jpg")

# 1. Fetch Trending Topic from RSS
def fetch_top_rss_trend():
    url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-IN&gl=IN&ceid=IN:en"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
            item = root.find(".//item")
            if item is not None:
                title = item.find("title").text
                # Clean up publication suffix (e.g. - NDTV, - LBBOnline)
                clean_title = title.split(" - ")[0].strip()
                return clean_title
    except Exception as e:
        print(f"[!] RSS fetch warning: {e}")
    return "Flipkart Big Billion Days Biggest iPhone Deals Campaign"

# 2. Generate Floating News Proof Card (Facebook Reel Style)
def create_floating_news_card(headline, subtext, out_path):
    w, h = 820, 440
    card = Image.new("RGBA", (w, h), (18, 24, 38, 235))
    draw = ImageDraw.Draw(card)
    
    # Outer accent border
    draw.rounded_rectangle([0, 0, w-1, h-1], radius=28, outline=(239, 68, 68, 255), width=5)
    
    # Top banner tag
    draw.rounded_rectangle([0, 0, w-1, 75], radius=28, fill=(220, 38, 38, 255))
    draw.rectangle([0, 45, w-1, 75], fill=(220, 38, 38, 255))
    
    # Text rendering (Default font)
    draw.text((35, 20), "⚡ BREAKING TECH UPDATE | MD_SADIQUE_AMIN EXCLUSIVE", fill=(255, 255, 255))
    
    # Headline in Gold / Yellow
    draw.text((40, 110), headline[:48], fill=(250, 204, 21))
    if len(headline) > 48:
        draw.text((40, 155), headline[48:95], fill=(250, 204, 21))
        
    # Subtext in clean White / Slate
    draw.text((40, 225), subtext[:55], fill=(241, 245, 249))
    if len(subtext) > 55:
        draw.text((40, 270), subtext[55:110], fill=(203, 213, 225))
        
    # Bottom Verified Badge
    draw.rounded_rectangle([40, 350, 320, 400], radius=12, fill=(16, 185, 129, 230))
    draw.text((55, 362), "✔ VERIFIED DEALS & ANALYSIS", fill=(255, 255, 255))
    
    card.save(out_path)
    return out_path

# 3. Audio DSP Mastering
STUDIO_MASTERING_FILTER = (
    "highpass=f=80,"
    "equalizer=f=220:width_type=q:w=1.2:g=2.5,"
    "equalizer=f=800:width_type=q:w=1.8:g=-2.0,"
    "equalizer=f=3400:width_type=q:w=1.2:g=2.8,"
    "equalizer=f=11500:width_type=q:w=1.5:g=1.8,"
    "compand=attacks=0.02:decays=0.2:points=-80/-80|-45/-35|-24/-14|-10/-7|0/-3:gain=3.0,"
    "loudnorm=I=-14:LRA=7:TP=-1.5"
)

async def generate_voice(script, raw_audio_path, mastered_audio_path):
    print("[*] Synthesizing 224 Hz Edge-TTS Voice...")
    com = edge_tts.Communicate(text=script, voice="hi-IN-SwaraNeural", rate="+0%", pitch="+0Hz")
    await com.save(raw_audio_path)
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe, "-y",
        "-i", raw_audio_path,
        "-af", STUDIO_MASTERING_FILTER,
        "-b:a", "192k",
        mastered_audio_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"[+] Mastered Voice synthesized: {mastered_audio_path}")

async def main():
    print("=" * 75)
    print("🌟 [Md Sadique Amin Live RSS Trending Reel Generator] Starting...")
    print("=" * 75)
    
    # Step 1: Fetch Trend
    trend = fetch_top_rss_trend()
    print(f"[1/5] 📡 Live RSS Topic: {trend}")
    
    # Step 2: Formulate Viral Script
    script = (
        f"Hello everyone! Main hoon Md Sadique Amin. "
        f"Aaj ki badi tech khabar: {trend}! "
        f"Festive season ke offers shuru ho chuke hain aur discounts sach mein unbelievable hain. "
        f"Aap is naye offer aur launch ke bare me kya sochte hain? "
        f"Mujhe comments mein zaroor batayein aur daily tech updates ke liye follow karein!"
    )
    
    # Step 3: Synthesize Voice
    raw_audio = os.path.join(OUTPUT_DIR, "temp_rss_voice_raw.mp3")
    master_audio = os.path.join(OUTPUT_DIR, "temp_rss_voice_mastered.mp3")
    await generate_voice(script, raw_audio, master_audio)
    
    # Get audio duration
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    probe_cmd = [
        ffmpeg_exe, "-i", master_audio
    ]
    res = subprocess.run(probe_cmd, stderr=subprocess.PIPE, text=True)
    duration = 14.0 # default
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            break
    print(f"[2/5] 🎙️ Audio Track Duration: {duration:.2f}s")
    
    # Step 4: Create Dynamic Floating News Card
    card_path = os.path.join(OUTPUT_DIR, "temp_news_card.png")
    create_floating_news_card(
        headline=trend,
        subtext="Lowest Festival Price & Major New Deals Live Now",
        out_path=card_path
    )
    print(f"[3/5] 🖼️ Dynamic Floating News Proof Card created: {card_path}")
    
    # Step 5: Render Video with Scene Zoom + Floating Card Overlay
    half_dur = round(duration / 2.0, 2)
    output_reel = os.path.join(OUTPUT_DIR, "md_sadique_amin_rss_trending_live_reel.mp4")
    
    # Filter Complex:
    # 0: Selfie image (first half) with slow cinematic zoom-in
    # 1: Kurta Benchmark (second half) with subtle pan
    # 2: Dynamic Floating Proof Card overlayed from t=2.0 to t=8.5 at bottom-center (x=130, y=1320)
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0008,1.15)':d={int(half_dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[v0];"
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0008,1.12)':d={int((duration - half_dur + 0.5)*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[v1];"
        f"[v0][v1]concat=n=2:v=1:a=0[bg];"
        f"[bg][2:v]overlay=x=130:y=1300:enable='between(t,2.0,{min(8.5, duration-2.0)})'[outv]"
    )
    
    print(f"[4/5] 🎬 Compositing 1080x1920 Full HD Reel...")
    render_cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-t", str(half_dur), "-i", BENCHMARK_SELFIE,
        "-loop", "1", "-t", str(duration - half_dur + 0.5), "-i", BENCHMARK_KURTA,
        "-i", card_path,
        "-i", master_audio,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "3:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_reel
    ]
    
    t0 = time.time()
    subprocess.run(render_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    t_render = time.time() - t0
    fsize = os.path.getsize(output_reel) / (1024 * 1024)
    print(f"[+] ✅ Reel Successfully Rendered! Path: {output_reel} ({fsize:.2f} MB in {t_render:.2f}s)")
    
    # Step 6: Multi-Platform Social Media Auto-Upload
    print(f"[5/5] 🌐 Initiating Auto-Upload to ALL Md Sadique Amin Social Media Platforms...")
    caption = (
        f"🔥 {trend} | Latest Tech Update\n\n"
        f"Festive deals and tech updates are live! Here is everything you need to know.\n\n"
        f"Follow @md_sadique_amin.official for daily AI, tech & lifestyle stories.\n\n"
        f"#Md Sadique Amin #TechTrends #iPhoneDeals #BBD #Innovation #AestheticAI"
    )
    
    adb_exe = r"C:\platform-tools\adb.exe"
    try:
        adb_res = subprocess.run([adb_exe, "devices"], capture_output=True, text=True)
        if "device" in adb_res.stdout:
            serial = [l.split()[0] for l in adb_res.stdout.strip().split("\n")[1:] if "\tdevice" in l or " device" in l][0]
            print(f"[+] Active ADB Device detected: {serial}")
            
            phone_dest = f"/sdcard/DCIM/Md Sadique Amin/{os.path.basename(output_reel)}"
            phone_camera = f"/sdcard/DCIM/Camera/{os.path.basename(output_reel)}"
            
            # Push to both Md Sadique Amin folder and Camera roll
            print(f"[*] Pushing reel to phone storage...")
            subprocess.run([adb_exe, "-s", serial, "push", output_reel, phone_dest], check=False)
            subprocess.run([adb_exe, "-s", serial, "push", output_reel, phone_camera], check=False)
            subprocess.run([adb_exe, "-s", serial, "shell", f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{phone_dest}"], check=False)
            subprocess.run([adb_exe, "-s", serial, "shell", f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{phone_camera}"], check=False)
            print(f"[+] Synced to phone gallery and camera roll!")
            
            # 1. Instagram Reels + Facebook Page + Threads Auto-Publish
            print("[*] Uploading to Instagram Reels, Facebook Page & Threads...")
            try:
                from post_reel_via_phone_adb import publish_latest_reel_multi_platform
                publish_latest_reel_multi_platform(caption)
                print("[+] ✅ Instagram + Facebook + Threads Publish Triggered!")
            except Exception as e:
                print(f"[!] Meta upload exception: {e}")
                
            # 2. YouTube Shorts Auto-Publish
            print("[*] Uploading to YouTube Shorts...")
            try:
                from youtube_create_factory import upload_to_youtube_shorts_via_adb
                upload_to_youtube_shorts_via_adb(serial, output_reel, f"{trend[:85]}", caption)
                print("[+] ✅ YouTube Shorts Publish Triggered!")
            except Exception as e:
                print(f"[!] YouTube Shorts upload exception: {e}")
        else:
            print("[!] Mobile device not currently online via ADB. Video is ready on PC at:")
            print(f"    {output_reel}")
            print("[*] As soon as you plug in the mobile phone, run:")
            print("    python generate_live_rss_reel.py --upload-only")
    except Exception as e:
        print(f"[!] ADB sync check notice: {e}")
        
    print("=" * 75)
    print("✨ COMPLETE PIPELINE EXECUTION FINISHED!")
    print(f"📁 Master Video Output: {output_reel}")
    print("=" * 75)

if __name__ == "__main__":
    if "--upload-only" in sys.argv:
        # Just upload latest reel
        output_reel = os.path.join(OUTPUT_DIR, "md_sadique_amin_rss_trending_live_reel.mp4")
        if os.path.exists(output_reel):
            # perform upload logic
            trend = fetch_top_rss_trend()
            caption = f"🔥 {trend}\n\nFollow @md_sadique_amin.official for daily tech updates!"
            from post_reel_via_phone_adb import publish_latest_reel_multi_platform
            publish_latest_reel_multi_platform(caption)
        else:
            print("[-] No rendered video found to upload.")
    else:
        asyncio.run(main())

