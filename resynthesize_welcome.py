import asyncio
import os
import edge_tts

welcome_script = (
    "Hello everyone! Main hoon Md Sadique Amin — aapki digital creator, visual storyteller, "
    "aur tech-culture explorer. Aaj se shuru ho raha hai hamara ek behad khoobsurat safar, "
    "jahan hum explore karenge modern lifestyle, aesthetic fashion, future technology, "
    "aur hamari rich cultural heritage. Is exciting journey ka hissa banne ke liye follow "
    "aur subscribe zaroor karein. Welcome to the Md Sadique Amin universe!"
)

async def make_welcome_audio():
    out_file = "voice_output/md_sadique_amin_grand_welcome_voice.mp3"
    print("[*] Re-synthesizing Grand Welcome voice with 'Hello everyone' (hi-IN-SwaraNeural @ 224Hz)...")
    communicate = edge_tts.Communicate(
        text=welcome_script,
        voice="hi-IN-SwaraNeural",
        rate="+0%",
        pitch="+0Hz"
    )
    await communicate.save(out_file)
    print(f"[+] Updated Grand Welcome audio generated: {out_file} ({os.path.getsize(out_file):,} bytes)")

if __name__ == "__main__":
    asyncio.run(make_welcome_audio())
