"""
Md Sadique Amin Reel Composer Engine
Composites vertical 9:16 (1080x1920) Full-HD video reels from image + audio with cinematic motion.
Uses bundled imageio_ffmpeg binary.
"""

import os
import subprocess
import imageio_ffmpeg

OUTPUT_DIR = os.path.join("exports", "reels")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def compose_vertical_reel(image_path, audio_path, output_filename="reel.mp4"):
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio not found: {audio_path}")
        
    print(f"[*] Rendering vertical reel (1080x1920 9:16): {output_path}...")
    
    # 1080x1920 Ken Burns smooth zoom filter
    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0008,1.15)':d=250:s=1080x1920:fps=30[v]"
    )
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"[+] Reel rendered successfully: {output_path} ({size_mb:.2f} MB)")
        return output_path
    else:
        raise RuntimeError(f"FFmpeg render error: {res.stderr[-400:]}")

if __name__ == "__main__":
    test_img = r"md_sadique_amin-images\01_md_sadique_amin_clean_portrait_kurta.jpg"
    test_audio = r"voice_output\test_speech.mp3"
    if os.path.exists(test_img) and os.path.exists(test_audio):
        compose_vertical_reel(test_img, test_audio, "test_render.mp4")
