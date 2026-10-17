"""
Md Sadique Amin Rapid Test Cycle Runner
Executes 1 full end-to-end autonomous cycle immediately:
1. Harvests live trend
2. Generates script, caption, hashtags
3. Synthesizes 224Hz neural voice track
4. Renders 1080x1920 9:16 vertical video reel
5. Logs execution row to reports/daily_performance.xlsx
"""

import os
import sys
import time
import asyncio
from datetime import datetime

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from engines.trend_harvester import get_latest_trends
from engines.voice_synthesizer import synthesize_voice
from engines.reel_composer import compose_vertical_reel
from reports.excel_logger import log_execution_cycle

async def execute_rapid_cycle():
    start_time = time.time()
    cycle_id = f"CYC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    print("=" * 70)
    print(f"🚀 EXECUTING MD_SADIQUE_AMIN RAPID TEST CYCLE [{cycle_id}]")
    print("=" * 70)
    
    # Step 1: Harvest Trend
    print("\n[Stage 1/5] Harvesting Real-Time Viral Trend...")
    trends = get_latest_trends()
    if trends:
        selected_trend = trends[0]
    else:
        selected_trend = {
            "topic": "Wearable AI & Smart Glasses: The Future of Fashion Tech",
            "category": "Tech & Future Lifestyle",
            "source": "Fallback Anchor"
        }
    print(f"[+] Selected Target Trend: {selected_trend['topic']}")
    print(f"[+] Category Pillar: {selected_trend['category']}")
    
    # Step 2: Cognitive Script & Caption Synthesis
    print("\n[Stage 2/5] Synthesizing First-Person Script & Social Caption...")
    script_text = (
        f"Hello everyone! Main hoon Md Sadique Amin. Aaj ka sabse exciting update: {selected_trend['topic']}. "
        "Technology aur fashion ab ek sath evolve ho rahe hain, creating a seamless future. "
        "Aapki is par kya raye hai? Mujhse judne ke liye follow karein aur comments me batayein!"
    )
    caption_text = (
        f"✨ The Future is Here | {selected_trend['topic']}\n\n"
        "Exploring how intelligent design and cutting-edge technology are redefining daily lifestyle.\n\n"
        "What are your thoughts on this evolution? Drop your perspective below! 👇\n\n"
        "#Md Sadique Amin #AICreator #VirtualInfluencer #FutureLifestyle #TechTrends #FashionTech #Innovation #DailyUpdate"
    )
    print(f"[+] Generated Script ({len(script_text)} chars):\n    \"{script_text}\"")
    
    # Step 3: Neural Voice Synthesis (224 Hz)
    print("\n[Stage 3/5] Synthesizing Neural Voice Track (224 Hz Lock)...")
    audio_filename = f"{cycle_id}_voice.mp3"
    audio_path = await synthesize_voice(script_text, audio_filename)
    
    # Step 4: Vertical Reel Rendering (1080x1920 9:16)
    print("\n[Stage 4/5] Compositing 1080x1920 9:16 Vertical Video Reel...")
    master_image = r"md_sadique_amin-images\01_md_sadique_amin_clean_portrait_kurta.jpg"
    reel_filename = f"{cycle_id}_reel.mp4"
    reel_path = compose_vertical_reel(master_image, audio_path, reel_filename)
    
    # Step 5: Excel Telemetry Logging
    print("\n[Stage 5/5] Logging Telemetry to reports/daily_performance.xlsx...")
    elapsed = time.time() - start_time
    log_execution_cycle(
        cycle_id=cycle_id,
        topic=selected_trend['topic'],
        category=selected_trend['category'],
        media_format="Reel 9:16 MP4",
        media_path=reel_path,
        status="RENDER_SUCCESS",
        latency=elapsed
    )
    
    print("\n" + "=" * 70)
    print("🎉 RAPID TEST CYCLE COMPLETED SUCCESSFULLY!")
    print(f"⏱️ Total End-to-End Latency: {elapsed:.2f} seconds")
    print(f"🎬 Rendered Reel: {reel_path}")
    print(f"🎙️ Voice Track: {audio_path}")
    print(f"📊 Audit Ledger: reports/daily_performance.xlsx")
    print("=" * 70)
    return {
        "cycle_id": cycle_id,
        "topic": selected_trend['topic'],
        "reel_path": reel_path,
        "audio_path": audio_path,
        "caption": caption_text,
        "latency": elapsed
    }

if __name__ == "__main__":
    asyncio.run(execute_rapid_cycle())
