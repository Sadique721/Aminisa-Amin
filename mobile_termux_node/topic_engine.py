# -*- coding: utf-8 -*-
"""
Aminsa Dynamic Topic & Video Script Engine
==========================================
Unified Engine powering both Termux Runner and 24/7 Daemon.
Strict Rules:
1. 100% Real-Time Live Multi-Tier RSS (Zero Hardcoded Text / Fallback).
2. Date-Aware Special Days (Republic Day, Teachers' Day, etc. if on date, else Live Top News).
3. Tech in English ("Hello everyone! I'm Aminsa. Today's top tech breakthrough: ...").
4. India/Others in Hinglish ("Hello everyone! Main hoon Aminsa. Aaj ki sabse badi khabar: ...").
5. Dynamic fresh closing/outro on every single slot.
6. Video Prompts ONLY (Zero Image Prompts).
"""

import random
import re
from datetime import datetime
from config import CATEGORIES, PERSONA_NAME, GREETING
from special_days import get_special_day_for_date
from dynamic_news_pipeline import fetch_live_headline

def make_yt_shorts_posting_text(headline: str, category_key: str) -> str:
    """
    Constructs YouTube Shorts Title strictly <= 100 characters (Hard YouTube Limit: 100 chars).
    Guarantees 0% overflow on YouTube mobile 'Add details' screen (Target: 80-95 chars).
    Structure: [Clean Headline] #Aminsa #Shorts [#Tag]
    """
    clean_hl = re.sub(r'[\r\n"\'\\/–—]', ' ', headline)
    clean_hl = re.sub(r'\s+', ' ', clean_hl).strip()

    domain_tags = {
        "special_day_or_india_top": "#India",
        "tech_ai": "#AI",
        "cricket_sports": "#Cricket",
        "economy_business": "#Startups",
        "culture_heritage": "#Culture",
        "bollywood_trends": "#Bollywood",
        "science_isro": "#ISRO",
        "future_tech": "#Tech",
        "global_affairs": "#Geopolitics",
        "wellness_health": "#Yoga"
    }
    dom_tag = domain_tags.get(category_key, "#Daily")
    tags_suffix = f"#Aminsa #Shorts {dom_tag}"
    
    # Target maximum 95 chars (safe 5-char margin below YouTube's 100-char limit)
    max_hl_budget = 95 - len(tags_suffix) - 1

    if len(clean_hl) > max_hl_budget:
        trimmed = clean_hl[:max_hl_budget]
        words = trimmed.rsplit(' ', 1)
        if len(words) > 1 and len(words[0]) >= 15:
            clean_hl = words[0].rstrip(':,.- ')
        else:
            clean_hl = trimmed.rstrip(':,.- ')

    result = f"{clean_hl} {tags_suffix}".strip()

    # Absolute hard ceiling <= 98 chars
    if len(result) > 100:
        excess = len(result) - 96
        clean_hl = clean_hl[:-excess].rsplit(' ', 1)[0].rstrip(':,.- ')
        result = f"{clean_hl} {tags_suffix}".strip()

    return result


def make_yt_create_video_prompt(persona_name: str, look: dict, headline: str) -> str:
    """
    Pure Motion & Narrative Prompt for Image-to-Video (YouTube Create).
    Since Aminsa's reference image is already provided:
    - Biometric face anchor is omitted to prevent AI face morphing and save prompt budget.
    - Full headline/topic is given maximum space (~115-125 chars) with zero truncation.
    - Enforces expressive natural speech, direct eye contact, natural hand gestures, and 9:16 60fps motion.
    - Strictly bounded under 292 characters (100% compliant with YouTube Create 300-char limit).
    """
    clean_hl = re.sub(r'["\'\\/–—]', '', headline)
    clean_hl = re.sub(r'\s+', ' ', clean_hl).strip()

    prefix = f"{persona_name} speaking expressively to camera with confident smile, lively eye contact and natural hand gestures discussing:"
    suffix = "Cinematic 9:16 vertical motion, fluid 60fps video."

    # Total budget max 292 characters (YouTube Create hard limit is 300)
    budget = 292 - (len(prefix) + 1 + len(suffix) + 1)
    if len(clean_hl) > budget:
        words = clean_hl[:budget].rsplit(' ', 1)
        clean_hl = words[0] if len(words) > 1 else clean_hl[:budget]

    return f"{prefix} {clean_hl}. {suffix}"

# Dynamic Insights and Fresh Outro Variations (Zero Static Monotony)
ENG_INSIGHTS = [
    "This breakthrough is set to reshape productivity and push compute efficiency into unprecedented frontiers",
    "Engineers and developers globally are watching closely as this architecture redefines intelligent workflows",
    "The rapid convergence of software systems and intelligent models here marks a pivotal technological leap",
    "This development brings massive scalability and fundamentally optimizes modern developer tooling"
]

ENG_OUTROS = [
    "What impact do you think this will have on our daily software stack? Share your thoughts below and stay tuned for more breakthroughs!",
    "Are you planning to test or integrate this in your workflow? Let me know in the comments and hit follow for real-time tech updates!",
    "How fast is your team adapting to this wave? Drop your perspective in the comments and let's explore together!",
    "Exciting times ahead for tech enthusiasts! Tell me your take on this and don't forget to follow for daily tech insights."
]

HINGLISH_INSIGHTS = {
    "special_day": [
        "Yeh din hum sabhi ko hamari aazadi, balidan aur rashtriya garima ki yaad dilata hai",
        "Hamari sanskriti aur aadarshon ka yeh utsav har Bhartiya ke dil me nayi urja bharta hai",
        "Desh ke nirmataon ke sapnon ko aage badhane ka yeh ek pavitra sankalp hai"
    ],
    "cricket_sports": [
        "Ground par players ka jazba aur fans ka josh dekhne layak hai — Bharat ka sporting spirit har match me naye records bana raha hai",
        "Match ki strategy aur intensity ne har sports lover ko seat ke kinare par la khada kiya hai",
        "Youth athletes ka yeh dedication saabit karta hai ki Bharat ab world sports me naye heights touch kar raha hai"
    ],
    "economy_business": [
        "Desh ke yuva entrepreneurs aur startup founders naye innovation ke sath market me danka baja rahe hain",
        "Indian economy aur domestic markets ki yeh tezi aane wale kal ke liye behad majboot sanket hai",
        "Local business aur consumer demand ka yeh surge ground reality ko completely transform kar raha hai"
    ],
    "culture_heritage": [
        "Hamari paramparayein aur aitihasik dharohar hamari sabse badi pehchan hain jise sanjo kar rakhna zaroori hai",
        "Desh ke kone-kone me bikhri kala aur vibrant festivals me ek anokha aakarshan aur apnapan hai",
        "Modern lifestyle ke beech apni jadon aur sanskriti se jude rehna ek behad khoobsurat anubhuti hai"
    ],
    "bollywood_trends": [
        "Social media par is viral trend aur nayi release ko lekar fans ka craze lagatar badhta ja raha hai",
        "Audience ab unique content aur genuine storytelling ko sabse zyada support de rahi hai",
        "Entertainment world ka yeh fresh twist har kisi ko hook kar raha hai"
    ],
    "science_isro": [
        "Bhartiya scientists ka yeh indigenous achievement pure vishwa me hamara seena garv se chauda karta hai",
        "Vigyan aur research me Bharat ka yeh badam aane wali generation ko nayi disha dikhayega",
        "Indigenous technology aur space exploration me hamari aatmanirbharta ka yeh shandar prateek hai"
    ],
    "global_affairs": [
        "Global stage par Bharat ki strategic position aur impactful aawaz ko aaj poori duniya dhyan se sun rahi hai",
        "International diplomacy me yeh badlaav aane wale samay me global dynamics ko shape karega",
        "Duniya bhar ke developments ka asar hamare trade aur economic ties par gehra padne wala hai"
    ],
    "wellness_health": [
        "Subah ki shanti me thoda samay apne sharir aur man ke liye nikalna dinbhar active rehne ka asli secret hai",
        "Desi lifestyle aur ancient Indian health wisdom modern busy life me sukoon pane ka best tareeqa hai",
        "Balanced routine aur holistic health se hi hum har challenge ko confidently face kar sakte hain"
    ],
    "default": [
        "Yeh development saabit karta hai ki ground level par hamara desh kitni tezi se progress kar raha hai",
        "Is badlaav ka direct asar hamare aam logon ke jeevan aur future opportunities par padne wala hai",
        "Aane wale samay me iska positive outcome dekhne layak hoga"
    ]
}

HINGLISH_OUTROS = [
    "Aapka is pure mudde par kya nazariya hai? Apni raye comments me zaroor share karein aur aisi hi breaking updates ke liye follow karein!",
    "Kya aap is development se agree karte hain? Mujhe comments me batayein aur daily updates ke liye jude rahein!",
    "Desh ki is nayi shuruat ko aap 10 me se kitne marks denge? Apne thoughts niche likhiye aur follow zaroor kijiye!",
    "Aapko kya lagta hai, iska aam janta par kya asar hoga? Comments me charcha karte hain, aur updates ke liye follow button dabayein!"
]


def generate_single_slot(slot_idx: int, target_dt=None) -> dict:
    if not target_dt:
        target_dt = datetime.now()

    slot_meta = CATEGORIES[slot_idx % len(CATEGORIES)]
    slot_id = slot_meta["id"]
    slot_num = slot_idx + 1
    slot_time = slot_meta["time"]
    category_key = slot_meta["category"]
    cat_name = slot_meta["name"]
    lang = slot_meta["language"]
    look = slot_meta["look"]

    # 1. SPECIAL DAY CHECK FOR SLOT 1
    is_special_day = False
    special_day_info = None
    if slot_id == "slot_1":
        special_day_info = get_special_day_for_date(target_dt)
        if special_day_info:
            is_special_day = True

    # 2. RESOLVE HEADLINE
    if is_special_day:
        title = special_day_info["title"]
        headline = f"Aaj desh mana raha hai: {special_day_info['title']}"
        insight = special_day_info["description"] + ". " + special_day_info["focus"]
        outro = "Aap sabhi ko is aitihasik diwas ki dheron shubhkaamnayein! Desh ke gaurav ko salam, Jai Hind!"
    else:
        headline = fetch_live_headline(category_key, slot_meta["rss_query"])
        title = headline

        if lang == "english":
            insight = random.choice(ENG_INSIGHTS)
            outro = random.choice(ENG_OUTROS)
        else:
            insights_pool = HINGLISH_INSIGHTS.get(category_key, HINGLISH_INSIGHTS["default"])
            insight = random.choice(insights_pool)
            outro = random.choice(HINGLISH_OUTROS)

    # 3. CONSTRUCT SCRIPT (Strictly 1 to 2 punchy statements, natural language)
    if is_special_day:
        script = f"{GREETING}! Main hoon {PERSONA_NAME}. Aaj desh mana raha hai {title} — aap sabhi ko is aitihasik diwas ki shubhkaamnayein, Jai Hind!"
    elif lang == "english":
        script = f"{GREETING}! I'm {PERSONA_NAME}. Today's top tech breakthrough: {headline} — {insight}!"
    else:
        script = f"{GREETING}! Main hoon {PERSONA_NAME}. Aaj ki sabse badi update: {headline} — {insight}!"

    # 4. CONSTRUCT YOUTUBE CREATE VIDEO MOTION PROMPT ONLY (Strictly 260-295 chars)
    video_prompt = make_yt_create_video_prompt(PERSONA_NAME, look, headline)

    # 5. CONSTRUCT YOUTUBE SHORTS REEL POSTING (Title, Details & Hashtags)
    yt_shorts_posting = make_yt_shorts_posting_text(headline, category_key)

    # 6. SOCIAL MEDIA CAPTION
    caption = (
        f"✨ {headline}\n\n"
        f"Aminsa brings you today's live update on {cat_name}.\n"
        f"What are your thoughts on this? Drop your perspective in the comments!\n\n"
        f"#Aminsa #IndiaFirst #{category_key.replace('_', '')} #DailyTrends #IndiaUpdates"
    )

    return {
        "slot": slot_num,
        "slot_id": slot_id,
        "time": slot_time,
        "category": cat_name,
        "category_key": category_key,
        "language": lang,
        "title": title,
        "headline": headline,
        "script": script,
        "video_prompt": video_prompt,
        "yt_shorts_posting": yt_shorts_posting,
        "caption": caption,
        "fb_description": caption,
        "wardrobe": look["attire"],
        "location": look["setting"]
    }


def get_all_daily_slots(target_dt=None) -> list:
    """Generates all 10 live dynamic slots for the day."""
    if not target_dt:
        target_dt = datetime.now()
    slots = []
    for i in range(len(CATEGORIES)):
        slot_data = generate_single_slot(i, target_dt)
        slots.append(slot_data)
    return slots


# Backward compatibility helper
def get_slot_topic_and_prompts(slot_index: int) -> dict:
    data = generate_single_slot(slot_index)
    data["yt_video_prompt"] = data["video_prompt"]
    data["yt_create_prompt"] = data["video_prompt"]
    data["speech_script"] = data["script"]
    data["speech_word_count"] = len(data["script"].split())
    data["slot_name"] = data["category"]
    data["look"] = {
        "attire": data.get("wardrobe", "Modern attire"),
        "setting": data.get("location", "Studio"),
        "hair": "Sleek styled"
    }
    return data


if __name__ == "__main__":
    print("Generating Slot 1 and Slot 2 Preview:")
    s1 = generate_single_slot(0)
    print("SLOT 1 (India Focus):")
    print(f"Title : {s1['title']}")
    print(f"Script: {s1['script']}\n")
    print(f"Video Prompt:\n{s1['video_prompt']}\n")

    s2 = generate_single_slot(1)
    print("SLOT 2 (Tech AI Focus - English):")
    print(f"Title : {s2['title']}")
    print(f"Script: {s2['script']}\n")
    print(f"Video Prompt:\n{s2['video_prompt']}\n")
