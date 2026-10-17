"""
Topic & Script Engine for Md Sadique Amin Mobile
========================================
Runs directly inside Termux on Android with zero external dependencies.
Uses built-in urllib and xml.etree.ElementTree.

Adheres 100% strictly to:
- GEMINI.md Biometric & Brand Guidelines:
  * Name: Md Sadique Amin (22yo adult female)
  * Skin: Warm glowing fair wheatish (#EAD5C3), unblemished porcelain, STRICT ZERO MOLES, ZERO MARKS.
  * Eyes: Deep almond hazel-brown with espresso limbal rings (#6B4423).
  * Nose: Delicate straight nose.
  * Hair: Dark espresso (#231709).
  * Greeting: ALWAYS "Hello everyone", NEVER "Namaste".
"""

import urllib.request
import xml.etree.ElementTree as ET
import re
from config import CATEGORIES, GREETING, PERSONA_NAME

USER_AGENT = "Mozilla/5.0 (Linux; Android 15; CPH2495) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

def clean_title(title):
    """Clean RSS title removing site branding."""
    if not title:
        return ""
    cleaned = re.sub(r"\s*-\s*[^-]+$", "", title)
    return cleaned.strip()

def fetch_rss_headline(query):
    """Fetch top headline from Google News RSS."""
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            items = root.findall(".//item")
            for it in items:
                title = it.find("title")
                if title is not None and title.text:
                    cleaned = clean_title(title.text)
                    if len(cleaned) > 15:
                        return cleaned
    except Exception as e:
        print(f"[-] RSS fetch error for query '{query}': {e}")
    return None

def get_slot_topic_and_prompts(slot_index):
    """Returns topic, Md Sadique Amin look, YouTube Create Image prompt, Video prompt, and speech script."""
    slot = CATEGORIES[slot_index % len(CATEGORIES)]
    headline = fetch_rss_headline(slot["rss_query"])
    if not headline:
        defaults = {
            "tech": "AI breakthroughs in India transforming modern everyday productivity",
            "business": "Indian startup ecosystem reaching new heights in 2026",
            "education": "Top skill development trends shaping the future workforce",
            "lifestyle": "Smart wellness habits and modern balanced daily routines",
            "creative": "Digital media and creative storytelling revolution in India",
            "science": "India space missions and scientific advancements inspiring youth",
            "cultural": "Preserving rich Indian heritage with modern contemporary grace",
            "mindset": "Focus, calm, and consistency in high-speed digital lifestyle",
            "night_tech": "Next-gen tech frameworks and developer productivity insights",
            "global_trends": "Global technology innovations shaping tomorrow's world",
        }
        headline = defaults.get(slot["category"], "Inspiring innovations and modern lifestyle trends")

    look = slot["look"]

    # --- STEP 1: YOUTUBE CREATE IMAGE PROMPT (<850 chars) ---
    # Locks exact face geometry & biometrics, applies dynamic look & setting
    yt_image_prompt = (
        f"Masterpiece portrait of 22-year-old Indian woman named Md Sadique Amin, "
        f"warm glowing fair wheatish skin tone #EAD5C3, unblemished porcelain texture, strictly zero moles zero marks, "
        f"deep almond hazel-brown eyes with dark espresso limbal rings #6B4423, delicate straight nose, natural soft rose lips, "
        f"dark espresso hair #231709 styled in {look['hair']}, {look['lipstick']} lipstick. "
        f"Wearing {look['attire']}. "
        f"Setting: {look['setting']}. "
        f"Vertical 9:16 portrait framing, soft bokeh depth of field, 8k master photography."
    )

    # --- STEP 2: YOUTUBE CREATE VIDEO ANIMATION PROMPT (<800 chars) ---
    # Commands YouTube Create to animate the generated Md Sadique Amin image speaking naturally about the topic
    yt_video_prompt = (
        f"Animate Md Sadique Amin speaking naturally, engaging direct eye contact with camera, gentle smile, "
        f"subtle natural head nodding and hand gestures discussing: {headline[:80]}. "
        f"Photorealistic natural lip-sync motion, smooth cinematic 60fps video, vertical 9:16 framing."
    )

    # --- STEP 3: MD_SADIQUE_AMIN SPEECH SCRIPT (Strict: Zero Namaste, Starts with 'Hello everyone') ---
    speech_script = (
        f"{GREETING}! Main hoon {PERSONA_NAME}. "
        f"Aaj ki badi khabar: {headline}. "
        f"Yeh dekhna sach me inspiring hai ki technology aur hamari duniya kis tezi se badal rahi hai. "
        f"Aapka is par kya raye hai? Comments me batayein aur follow zaroor karein!"
    )

    # --- STEP 4: SOCIAL MEDIA CAPTION ---
    caption = (
        f"✨ {headline}\n\n"
        f"Md Sadique Amin shares today's quick insight on {slot['name']}.\n"
        f"What are your thoughts on this? Drop a comment below!\n\n"
        f"#Md Sadique Amin #AI #TrendingIndia #{slot['category'].capitalize()} #DailyUpdate"
    )

    return {
        "slot_id": slot["id"],
        "slot_name": slot["name"],
        "category": slot["category"],
        "headline": headline,
        "look": look,
        "yt_image_prompt": yt_image_prompt,
        "yt_video_prompt": yt_video_prompt,
        "yt_prompt": yt_image_prompt, # backwards compatibility
        "speech_script": speech_script,
        "caption": caption,
    }

if __name__ == "__main__":
    import json
    data = get_slot_topic_and_prompts(0)
    print("SLOT 0 PREVIEW:")
    print(json.dumps(data, indent=2))
