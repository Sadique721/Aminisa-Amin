import asyncio
import os
import edge_tts
from moviepy import ImageClip, AudioFileClip

AUDIO_TEXT = (
    "Hello everyone! Main hoon Md Sadique Amin. Ek digital creator aur AI persona. "
    "Mera ye official voice aur look 100 percent locked hai. "
    "Ab hum milkar technology, global fashion aur future trends ko explore karenge. "
    "Welcome to my official universe!"
)

VOICE = "hi-IN-SwaraNeural"  # Warm, modern, expressive 224 Hz female voice
AUDIO_OUTPUT = "md_sadique_amin_intro_voice.mp3"
IMAGE_PATH = os.path.join("md_sadique_amin-images", "01_md_sadique_amin_clean_portrait_kurta.jpg")
VIDEO_OUTPUT = "md_sadique_amin_official_intro_reel.mp4"

async def generate_speech():
    print(f"Generating Md Sadique Amin audio with {VOICE}...")
    communicate = edge_tts.Communicate(AUDIO_TEXT, VOICE, pitch="+0Hz", rate="+0%")
    await communicate.save(AUDIO_OUTPUT)
    print(f"Audio saved to: {AUDIO_OUTPUT}")

def create_video():
    print("Synthesizing Md Sadique Amin 9:16 Reel Video...")
    audio_clip = AudioFileClip(AUDIO_OUTPUT)
    duration = audio_clip.duration
    
    # Create image clip matching audio length
    video_clip = ImageClip(IMAGE_PATH).with_duration(duration)
    video_clip = video_clip.with_audio(audio_clip)
    
    # Export high quality vertical reel MP4
    video_clip.write_videofile(
        VIDEO_OUTPUT,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )
    print(f"Master Video successfully created: {VIDEO_OUTPUT}")

if __name__ == "__main__":
    asyncio.run(generate_speech())
    create_video()
