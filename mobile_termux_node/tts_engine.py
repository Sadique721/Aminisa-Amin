"""
Voice Synthesis Engine for Aminsa Amin Mobile
============================================
Runs natively inside Termux on Android using Edge-TTS.
Generates Aminsa Amin's signature voice: hi-IN-SwaraNeural @ 224Hz (Pitch: +1Hz, Rate: -2%).
"""

import os
import asyncio
from config import VOICE_NAME, VOICE_PITCH, VOICE_RATE, AUDIO_DIR

try:
    import edge_tts
except ImportError:
    edge_tts = None

async def _synthesize_async(text, output_path):
    if not edge_tts:
        raise RuntimeError("edge-tts library is not installed in Termux. Run 'pip install edge-tts'")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE_NAME,
        rate=VOICE_RATE,
        pitch=VOICE_PITCH
    )
    await communicate.save(output_path)
    return output_path

def generate_voice(text, filename="aminsa_speech.mp3"):
    """Synchronous wrapper to generate audio file.
    Audio dir is auto-resolved by config.py (sdcard if writable, else Termux home).
    """
    try:
        os.makedirs(AUDIO_DIR, exist_ok=True)
    except Exception:
        pass  # config.py already created the fallback dir
    target = os.path.join(AUDIO_DIR, filename)
    asyncio.run(_synthesize_async(text, target))
    return target

if __name__ == "__main__":
    test_text = "Hello everyone, main hoon Aminsa! Standalone Termux voice synthesis test successful."
    path = generate_voice(test_text, "test_audio.mp3")
    print(f"[+] Audio generated at: {path} (Size: {os.path.getsize(path)} bytes)")
