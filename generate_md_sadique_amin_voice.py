"""
Md Sadique Amin Voice Synthesis Engine
Generates official voice tracks using Microsoft Edge-TTS
Locked Voice Persona: hi-IN-SwaraNeural / en-IN-NeerjaExpressiveNeural @ 224 Hz center
"""

import asyncio
import os
import edge_tts

OUTPUT_DIR = "voice_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPT_TEXT = (
    "Hello everyone! Main hoon Md Sadique Amin. Welcome to my official digital space. "
    "Yahan hum explore karenge technology, global fashion, aur hamari rich cultural heritage ka khoobsurat sangam. "
    "Mujhse judne ke liye follow karein, aur is journey ka hissa banein. Stay inspired!"
)

VOICE_NAME = "hi-IN-SwaraNeural"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "md_sadique_amin_official_intro.mp3")

async def generate_voice():
    print(f"[*] Generating Md Sadique Amin Voice Track with {VOICE_NAME}...")
    communicate = edge_tts.Communicate(
        text=SCRIPT_TEXT,
        voice=VOICE_NAME,
        rate="+0%",
        pitch="+0Hz"
    )
    await communicate.save(OUTPUT_FILE)
    print(f"[+] Successfully generated official voice track: {OUTPUT_FILE}")
    print(f"[+] File Size: {os.path.getsize(OUTPUT_FILE)} bytes")

if __name__ == "__main__":
    asyncio.run(generate_voice())
