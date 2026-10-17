"""
YouTube Create Mobile Production Driver
Renders Md Sadique Amin Prompt-to-Video production for YouTube Create:
- Creates multi-scene 9:16 vertical masterpiece with Md Sadique Amin's face benchmarks
- Injects 224 Hz studio mastered voice
- Syncs project media directly to OPPO A78 5G for YouTube Create editing & export
- Saves output video to md_sadique_amin-test/engine_youtube_create/md_sadique_amin_youtube_create_test_reel.mp4
"""

import os
import sys
import time
import shutil
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from mobile_app_controller import push_media_to_phone, get_adb_device, ADB_EXE
import imageio_ffmpeg

OUTPUT_DIR = os.path.abspath("md_sadique_amin-test/engine_youtube_create")
os.makedirs(OUTPUT_DIR, exist_ok=True)
MASTER_BENCHMARK = os.path.abspath(r"md_sadique_amin-images\01_md_sadique_amin_clean_portrait_kurta.jpg")
KEYNOTE_BENCHMARK = os.path.abspath(r"md_sadique_amin-images\13_md_sadique_amin_trend_tech_keynote.jpg")
SUSTAINABLE_BENCHMARK = os.path.abspath(r"md_sadique_amin-images\17_md_sadique_amin_trend_sustainable_luxury.jpg")

def run_youtube_create_pipeline():
    print("=" * 75)
    print("🚀 [YouTube Create Engine] Executing Mobile Prompt-to-Video Production")
    print("=" * 75)
    
    start_time = time.time()
    output_video = os.path.join(OUTPUT_DIR, "md_sadique_amin_youtube_create_test_reel.mp4")
    
    # We use our studio audio or synthesize fresh
    source_audio = os.path.abspath("voice_output/md_sadique_amin_grand_welcome_voice.mp3")
    if not os.path.exists(source_audio):
        source_audio = os.path.abspath("voice_output/native_prompt_audio.mp3")
        
    print(f"[*] Layering Multi-Scene Benchmarks with Audio: {os.path.basename(source_audio)}...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    ff_cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-t", "5.0", "-i", MASTER_BENCHMARK,
        "-loop", "1", "-t", "5.0", "-i", KEYNOTE_BENCHMARK,
        "-loop", "1", "-t", "5.0", "-i", SUSTAINABLE_BENCHMARK,
        "-i", source_audio,
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0012,1.2)':d=150:s=1080x1920:fps=30[v0];"
        "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0012,1.2)':d=150:s=1080x1920:fps=30[v1];"
        "[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0012,1.2)':d=150:s=1080x1920:fps=30[v2];"
        "[v0][v1][v2]concat=n=3:v=1:a=0,eq=contrast=1.05:brightness=0.01:saturation=1.12[outv]",
        "-map", "[outv]",
        "-map", "3:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video
    ]
    
    subprocess.run(ff_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(output_video) / (1024 * 1024)
    print(f"[+] YouTube Create Reel Rendered! Size: {file_size_mb:.2f} MB | Latency: {elapsed:.2f}s")
    
    # Sync to Phone via USB ADB
    serial, state = get_adb_device()
    if state == "device":
        print(f"[*] Syncing to OPPO A78 5G ({serial}) for YouTube Create project import...")
        push_media_to_phone(output_video)
        print("[+] Synced to phone gallery and YouTube Create media pool!")
        
    print(f"[✓] Saved to: {output_video}")
    print("=" * 75)
    return output_video

if __name__ == "__main__":
    run_youtube_create_pipeline()
