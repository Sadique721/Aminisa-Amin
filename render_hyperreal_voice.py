import asyncio
import os
import sys
import subprocess
import edge_tts
import imageio_ffmpeg

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

OUTPUT_DIR = "voice_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Strictly starting with 'Hello everyone!' (Zero Namaste)
TEXT = (
    "Hello everyone! Main hoon Md Sadique Amin ... aapki digital creator, visual storyteller, aur tech-culture explorer. ... "
    "Aaj se shuru ho raha hai hamara ek behad khoobsurat safar ... jahan hum explore karenge modern lifestyle, aesthetic fashion, future technology aur hamari rich cultural heritage. ... "
    "Is exciting journey ka hissa banne ke liye follow aur subscribe zaroor karein. ... "
    "Welcome to the Md Sadique Amin universe!"
)

STUDIO_MASTERING_FILTER = (
    "highpass=f=80,"
    "equalizer=f=220:width_type=q:w=1.2:g=2.5,"
    "equalizer=f=800:width_type=q:w=1.8:g=-2.0,"
    "equalizer=f=3400:width_type=q:w=1.2:g=2.8,"
    "equalizer=f=11500:width_type=q:w=1.5:g=1.8,"
    "compand=attacks=0.02:decays=0.2:points=-80/-80|-45/-35|-24/-14|-10/-7|0/-3:gain=3.5,"
    "loudnorm=I=-14:LRA=7:TP=-1.5"
)

async def build_hyperreal_voice():
    raw_path = os.path.join(OUTPUT_DIR, "raw_welcome_v2.mp3")
    final_path = os.path.join(OUTPUT_DIR, "md_sadique_amin_grand_welcome_voice_v2_hyperreal.mp3")
    master_path = os.path.join(OUTPUT_DIR, "md_sadique_amin_grand_welcome_voice.mp3")
    
    print("[*] Synthesizing Hyper-Real Neural Voice with relaxed human pacing (-3%)...")
    communicate = edge_tts.Communicate(
        text=TEXT,
        voice="hi-IN-SwaraNeural",
        rate="-3%",
        pitch="+0Hz"
    )
    await communicate.save(raw_path)
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe, "-y",
        "-i", raw_path,
        "-af", STUDIO_MASTERING_FILTER,
        "-b:a", "192k",
        final_path
    ]
    
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode == 0 and os.path.exists(final_path):
        print(f"[✓] Studio Mastered Hyper-Real Voice Generated: {final_path} ({os.path.getsize(final_path):,} bytes)")
        # Overwrite master path as well
        with open(final_path, "rb") as src, open(master_path, "wb") as dst:
            dst.write(src.read())
        print(f"[✓] Master voice updated: {master_path}")
        if os.path.exists(raw_path):
            os.remove(raw_path)
    else:
        print("[-] FFmpeg processing error, copying raw file")
        os.rename(raw_path, final_path)

if __name__ == "__main__":
    asyncio.run(build_hyperreal_voice())
