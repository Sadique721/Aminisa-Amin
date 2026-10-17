"""
Md Sadique Amin Topic & Appearance Engine
=================================
Automatically:
1. Fetches & classifies trending topics into categories
2. Maps each category to Md Sadique Amin's dynamic appearance:
   - IT/Tech     → Formal blazer, sleek ponytail, clean office BG
   - Festival    → Traditional lehenga/kurta, heavy dupatta, festive BG
   - Personal    → Casual chic, natural waves, warm café/home BG
   - Political   → Formal sari/suit, elegant updo, neutral studio BG
   - Fashion     → Trendy western outfit, styled curls, fashion BG
   - Travel      → Travel-ready casual, natural outdoor BG
   - Food/Agri   → Warm traditional look, kitchen/market BG
   - Education   → Smart casual, library BG
   - Health/Fit  → Active wear, gym/nature BG
   - Finance/Biz → Business formal, corporate BG
3. Generates YouTube Create image prompt + video script
"""

import sys
import urllib.request
import xml.etree.ElementTree as ET
import json
import re

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ─────────────────────────────────────────────
# MD_SADIQUE_AMIN APPEARANCE MAP — Dynamic per Category
# ─────────────────────────────────────────────
APPEARANCE_MAP = {
    "tech": {
        "label": "IT / Tech",
        "outfit": "sleek formal white blazer over pastel blouse, minimal gold stud earrings",
        "hair": "sleek high ponytail with side-swept front strands",
        "makeup": "subtle nude lips, light contour, defined brows",
        "background": "modern glass-and-steel tech office, dual monitors glowing blue, bokeh city lights",
        "mood": "confident, professional, forward-thinking",
        "color_tone": "cool blue and white tones, crisp lighting",
        "emoji": "💻",
    },
    "festival": {
        "label": "Festival / Culture",
        "outfit": "vibrant handcrafted Banarasi lehenga with heavy embroidered dupatta, colorful bangles, maang tikka",
        "hair": "traditional braided half-bun with marigold flowers woven in",
        "makeup": "bright red lips, golden kajal, bold bindi, festive glow",
        "background": "marigold-decorated temple courtyard, oil diyas glowing, warm golden hour",
        "mood": "joyful, celebratory, culturally radiant",
        "color_tone": "rich saffron, gold, deep red tones, warm bokeh",
        "emoji": "🎊",
    },
    "personal": {
        "label": "Personal / Lifestyle",
        "outfit": "chic beige ribbed turtleneck sweater with gold chain necklace",
        "hair": "natural loose dark espresso waves falling over shoulders",
        "makeup": "soft rosy lips, dewy skin, light mascara",
        "background": "cozy aesthetic café with warm pendant lights, wooden shelves, bokeh",
        "mood": "warm, relatable, authentic, friendly",
        "color_tone": "warm amber and cream tones, soft natural light",
        "emoji": "☕",
    },
    "political": {
        "label": "Political / Social",
        "outfit": "elegant solid-color formal cotton sari with minimalist border, subtle pearl earrings",
        "hair": "neat low chignon bun, minimal accessories",
        "makeup": "sophisticated nude lips, defined eyes, professional finish",
        "background": "clean neutral studio with soft gradient background, subtle Indian flag motif",
        "mood": "composed, authoritative, socially aware",
        "color_tone": "neutral greys, white, dignified warm tones",
        "emoji": "🗣️",
    },
    "fashion": {
        "label": "Fashion / Beauty",
        "outfit": "trendy coord set in pastel lavender with statement belt, modern gold hoops",
        "hair": "voluminous styled loose curls with hair serum shine",
        "makeup": "bold nude-mauve lips, sculpted contour, glossy lids",
        "background": "high-fashion editorial backdrop, neon accent wall, fashion week crowd blur",
        "mood": "glamorous, trendy, self-expressive, bold",
        "color_tone": "pastel purple, soft pink, editorial high-contrast",
        "emoji": "👗",
    },
    "travel": {
        "label": "Travel / Adventure",
        "outfit": "relaxed linen button-down shirt, minimalist watch, travel tote bag",
        "hair": "casual beach waves with subtle hair clip",
        "makeup": "fresh dewy no-makeup look, tinted lip balm",
        "background": "scenic outdoor destination — Himalayan valley OR coastal sunset, golden bokeh",
        "mood": "adventurous, free-spirited, exploratory",
        "color_tone": "earthy greens, sky blues, warm golden hour",
        "emoji": "✈️",
    },
    "food": {
        "label": "Food / Culture",
        "outfit": "traditional printed cotton kurti with wooden bangles, simple dupatta",
        "hair": "simple side-parted half-up bun",
        "makeup": "fresh natural look, coral lip tint",
        "background": "vibrant Indian street market OR warm home kitchen with spices",
        "mood": "warm, nurturing, culturally proud",
        "color_tone": "warm ochre, deep terracotta, bright spice tones",
        "emoji": "🍛",
    },
    "education": {
        "label": "Education / Career",
        "outfit": "smart formal shirt tucked into tailored trousers, subtle stud earrings",
        "hair": "clean side-parted straight blow-dry",
        "makeup": "professional light finish, subtle lip color",
        "background": "modern library with bookshelves, soft warm study lamps",
        "mood": "inspiring, motivational, intellectual",
        "color_tone": "warm beige and soft white tones, scholarly ambiance",
        "emoji": "📚",
    },
    "health": {
        "label": "Health / Fitness",
        "outfit": "modern active wear in mint green, sporty headband",
        "hair": "high ponytail, fresh and sporty",
        "makeup": "minimal fresh-faced look, clear gloss",
        "background": "bright yoga studio OR lush green park morning walk",
        "mood": "energetic, healthy, empowering",
        "color_tone": "fresh greens, whites, morning light tones",
        "emoji": "🧘",
    },
    "finance": {
        "label": "Finance / Business",
        "outfit": "sharp charcoal business blazer with inner silk blouse, minimalist watch",
        "hair": "sleek straight blow-dry, side-parted",
        "makeup": "professional matte lips, sharp eyeliner, clean finish",
        "background": "contemporary corporate boardroom, glass wall with city view",
        "mood": "confident, strategic, financially empowered",
        "color_tone": "slate grey, charcoal, silver, power tones",
        "emoji": "💼",
    },
}

# ─────────────────────────────────────────────
# TOPIC CATEGORY CLASSIFIER
# ─────────────────────────────────────────────
KEYWORD_RULES = {
    "tech":     ["artificial intelligence", "machine learning", "software", "startup tech",
                 "iphone", "android phone", "5g network", "semiconductor", "isro launch",
                 "nasa", "spacecraft", "cybersecurity", "cloud computing", "programming",
                 "neural network", "chatgpt", "openai", "deepmind", "robotics", "ev battery",
                 "electric vehicle launch", "satellite", "blockchain", "coding"],
    "festival": ["diwali", "eid", "holi", "navratri", "durga puja", "ganesh chaturthi",
                 "christmas", "new year celebration", "janmashtami", "independence day",
                 "republic day", "raksha bandhan", "onam", "bihu", "garba", "dandiya",
                 "dussehra", "baisakhi", "lohri", "pongal", "festival season", "celebration"],
    "political":["election results", "modi government", "parliament session", "minister",
                 "bjp", "congress party", "election commission", "vote", "policy reform",
                 "supreme court verdict", "constitution", "budget 2025", "pm modi",
                 "yojana scheme", "corruption case", "political party", "lok sabha"],
    "fashion":  ["fashion week", "style trend", "outfit ideas", "beauty tips", "makeup look",
                 "skincare routine", "fashion influencer", "luxury brand", "runway show",
                 "paris fashion", "designer collection", "jewelry trend", "aesthetic fashion",
                 "bollywood style", "celebrity outfit", "ethnic wear", "saree look"],
    "travel":   ["travel destination", "tourist spot", "trip to", "holiday package",
                 "vacation in", "visit india", "trekking", "hill station", "beach resort",
                 "mountain retreat", "tourism", "best places", "travel guide", "explore india"],
    "food":     ["street food", "recipe", "restaurant", "cuisine", "chef", "cooking tips",
                 "biryani", "food festival", "spice", "healthy meal", "indian food",
                 "snack", "sweet dish", "dessert", "food blog", "food vlog", "foodie"],
    "education":["school exam", "college admission", "upsc", "jee result", "neet exam",
                 "scholarship", "graduation", "teacher", "student", "learning app",
                 "skill development", "online course", "career guidance", "study tips",
                 "university", "campus", "education policy", "cbse"],
    "health":   ["health tips", "fitness routine", "yoga practice", "workout", "gym",
                 "mental health", "diet plan", "nutrition", "hospital", "medicine",
                 "doctor", "wellness", "weight loss", "meditation", "lung", "heart health",
                 "diabetes", "cancer awareness", "health day", "immunity"],
    "finance":  ["stock market", "sensex", "nifty", "mutual fund", "rbi policy", "rupee",
                 "cryptocurrency", "ipo", "business news", "startup funding", "fintech",
                 "bank", "interest rate", "investment tips", "economy", "gdp", "inflation"],
    "personal": ["motivation", "self improvement", "life tips", "mindset", "positivity",
                 "dream", "goal setting", "relationship advice", "family", "morning routine",
                 "productivity", "success story", "personal growth", "confidence"],
}

def classify_topic(topic_text):
    """Classify a topic string into a category key."""
    lower = topic_text.lower()
    scores = {cat: 0 for cat in KEYWORD_RULES}
    for cat, keywords in KEYWORD_RULES.items():
        for kw in keywords:
            if kw in lower:
                scores[cat] += 1
    best = max(scores, key=lambda c: scores[c])
    if scores[best] == 0:
        return "personal"  # default fallback
    return best

# ─────────────────────────────────────────────
# TREND FETCHER (Multi-Source RSS)
# ─────────────────────────────────────────────
RSS_FEEDS = {
    "tech":        "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-IN&gl=IN&ceid=IN:en",
    "business":    "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-IN&gl=IN&ceid=IN:en",
    "entertain":   "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-IN&gl=IN&ceid=IN:en",
    "health":      "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=en-IN&gl=IN&ceid=IN:en",
    "science":     "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-IN&gl=IN&ceid=IN:en",
    "india":       "https://news.google.com/rss/headlines/section/geo/India?hl=en-IN&gl=IN&ceid=IN:en",
    "sport":       "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-IN&gl=IN&ceid=IN:en",
    "travel_food": "https://news.google.com/rss/search?q=travel+OR+food+OR+festival+india&hl=en-IN&gl=IN&ceid=IN:en",
    "lifestyle":   "https://news.google.com/rss/search?q=lifestyle+OR+fashion+OR+beauty+india&hl=en-IN&gl=IN&ceid=IN:en",
    "education":   "https://news.google.com/rss/search?q=education+OR+students+OR+career+india&hl=en-IN&gl=IN&ceid=IN:en",
}

def fetch_all_trends(limit_per_feed=3):
    """Fetch trending topics from multiple RSS feeds."""
    all_topics = []
    for section, url in RSS_FEEDS.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                root = ET.fromstring(resp.read())
                for item in root.findall(".//item")[:limit_per_feed]:
                    title_el = item.find("title")
                    if title_el is not None and title_el.text:
                        title = title_el.text.strip()
                        # Remove source name from Google News titles
                        title = re.sub(r'\s*-\s*[A-Za-z\s]+$', '', title).strip()
                        category = classify_topic(title)
                        all_topics.append({
                            "topic": title,
                            "category": category,
                            "appearance": APPEARANCE_MAP.get(category, APPEARANCE_MAP["personal"]),
                            "source": section,
                        })
        except Exception as e:
            print(f"[-] RSS fetch note ({section}): {e}")
    return all_topics

# ─────────────────────────────────────────────
# YOUTUBE CREATE PROMPT GENERATOR
# ─────────────────────────────────────────────
MD_SADIQUE_AMIN_BASE = (
    "Md Sadique Amin, a 22-year-old Indian female social media creator, "
    "fair warm wheatish skin (#EAD5C3), strictly ZERO moles or marks on face, "
    "deep almond-shaped hazel-brown eyes with dark espresso limbal rings, "
    "delicate straight nose, natural soft rose lips, "
    "dark espresso wavy hair (#231709), "
    "athletic-slender figure 5'6\""
)

def generate_youtube_create_image_prompt(topic_entry):
    """Generate a YouTube Create image generation prompt for a given topic."""
    a = topic_entry["appearance"]
    topic = topic_entry["topic"]
    
    prompt = (
        f"Photorealistic 4K selfie-style vertical portrait of {MD_SADIQUE_AMIN_BASE}, "
        f"wearing {a['outfit']}, "
        f"hair styled as {a['hair']}, "
        f"makeup: {a['makeup']}, "
        f"standing in {a['background']}, "
        f"mood: {a['mood']}, "
        f"lighting: {a['color_tone']}, "
        f"9:16 vertical format, ultra-sharp face clarity, clean unblemished skin, "
        f"cinematic depth of field, photorealistic, no text, no watermark"
    )
    # Keep under 850 chars (YouTube Create limit ~900 chars)
    if len(prompt) > 850:
        prompt = prompt[:847] + "..."
    return prompt

def generate_script_and_caption(topic_entry):
    """Generate Md Sadique Amin's spoken script + social media caption."""
    topic = topic_entry["topic"]
    cat = topic_entry["category"]
    emoji = topic_entry["appearance"]["emoji"]
    
    # Hindi/Hinglish script (60-80 words for ~30 sec video)
    script = (
        f"Hello everyone! Main hoon Md Sadique Amin. "
        f"Aaj baat karte hain {topic} ke baare mein. "
        f"Ye topic aaj bahut trending hai aur iska aap ki zindagi par seedha asar pad sakta hai. "
        f"Mera maanna hai ke hum sab milke is change ko samajh sakte hain aur apne life mein apply kar sakte hain. "
        f"Aap ki is baare mein kya soch hai? "
        f"Neeche comment karein aur follow zaroor karein!"
    )
    
    # English caption with hashtags
    caption = (
        f"{emoji} {topic}\n\n"
        f"Let's talk about what's happening in {topic_entry['appearance']['label']} today! "
        f"This is something every one of us should know about. "
        f"Share your thoughts in the comments!\n\n"
        f"#Md Sadique Amin #AICreator #VirtualInfluencer #{cat.capitalize()} "
        f"#IndiaCreator #Trending #Reels #Shorts #ViralContent"
    )
    
    return script, caption

def generate_youtube_create_video_prompt(topic_entry, script):
    """Generate YouTube Create video/avatar generation prompt."""
    a = topic_entry["appearance"]
    
    prompt = (
        f"Talking head video of {MD_SADIQUE_AMIN_BASE}, "
        f"{a['outfit']}, {a['hair']}, {a['makeup']}, "
        f"{a['background']}, "
        f"speaking confidently to camera with natural lip sync, "
        f"natural eye blinks, subtle head movement, warm smile, "
        f"9:16 vertical 1080x1920, cinematic lighting, photorealistic, 30fps"
    )
    if len(prompt) > 850:
        prompt = prompt[:847] + "..."
    return prompt

# Preferred category order for 10-slot daily schedule (diversity-first)
DAILY_CATEGORY_PLAN = [
    "tech", "festival", "finance", "health", "fashion",
    "political", "travel", "food", "education", "personal"
]

def select_10_daily_topics():
    """
    Fetch all trends and select 10 diverse topics.
    Follows DAILY_CATEGORY_PLAN to ensure one topic per major category.
    Falls back to default topics for missing categories.
    Returns list of 10 topic_entry dicts.
    """
    print("[*] Fetching live trending topics from Google News India (10 feeds)...")
    all_topics = fetch_all_trends(limit_per_feed=3)
    print(f"[*] Fetched {len(all_topics)} raw topics. Building diverse 10-slot plan...")
    
    # Build category bucket
    category_bucket = {cat: [] for cat in DAILY_CATEGORY_PLAN}
    for t in all_topics:
        cat = t["category"]
        if cat in category_bucket:
            category_bucket[cat].append(t)
    
    # Select one best topic per category slot
    selected = []
    for cat in DAILY_CATEGORY_PLAN:
        if category_bucket[cat]:
            selected.append(category_bucket[cat][0])
        else:
            # No live topic for this category — use default
            selected.append(_default_for_category(cat))

    # Safety: deduplicate by topic text
    seen_topics = set()
    unique_selected = []
    for t in selected:
        key = t["topic"][:40]
        if key not in seen_topics:
            seen_topics.add(key)
            unique_selected.append(t)
        else:
            # Replace duplicate with random remaining topic
            for fallback in all_topics:
                fkey = fallback["topic"][:40]
                if fkey not in seen_topics:
                    seen_topics.add(fkey)
                    unique_selected.append(fallback)
                    break
    selected = unique_selected
    
    # If still not 10, pad with default personal topics
    defaults = [
        {"topic": "Morning productivity habits for young Indians", "category": "personal"},
        {"topic": "AI tools every student must know in 2025", "category": "tech"},
        {"topic": "Budget-friendly fashion tips for everyday style", "category": "fashion"},
        {"topic": "Indian street food culture in 2025", "category": "food"},
        {"topic": "Fitness routines you can do at home", "category": "health"},
    ]
    for d in defaults:
        if len(selected) >= 10:
            break
        d["appearance"] = APPEARANCE_MAP.get(d["category"], APPEARANCE_MAP["personal"])
        selected.append(d)
    
    return selected[:10]

def _default_for_category(cat):
    """Return a hand-crafted default topic for when RSS has no live match."""
    defaults = {
        "tech":      "AI tools transforming Indian education and work in 2025",
        "festival":  "How to celebrate Indian festivals beautifully on a budget",
        "finance":   "Smart money habits every young Indian must build now",
        "health":    "Simple daily fitness habits for working professionals in India",
        "fashion":   "Top ethnic fashion trends every Indian woman is loving right now",
        "political": "What India's policy changes mean for young citizens",
        "travel":    "Hidden gems in India you must visit before 2026",
        "food":      "Best Indian street foods and how to make them at home",
        "education": "Career tips that helped me grow as a young Indian professional",
        "personal":  "Morning routines of successful young Indian women",
    }
    topic_text = defaults.get(cat, "Inspiring stories of young Indian changemakers")
    return {
        "topic": topic_text,
        "category": cat,
        "appearance": APPEARANCE_MAP.get(cat, APPEARANCE_MAP["personal"]),
        "source": "default"
    }

if __name__ == "__main__":
    print("\n" + "="*70)
    print("MD_SADIQUE_AMIN TOPIC & APPEARANCE ENGINE — TEST RUN")
    print("="*70)
    topics = select_10_daily_topics()
    for i, t in enumerate(topics, 1):
        print(f"\n[Slot {i:02d}] {t['appearance']['emoji']} [{t['appearance']['label']}]")
        print(f"  Topic   : {t['topic'][:70]}")
        img_prompt = generate_youtube_create_image_prompt(t)
        print(f"  Img Prompt ({len(img_prompt)} chars): {img_prompt[:80]}...")
        script, caption = generate_script_and_caption(t)
        print(f"  Script  : {script[:80]}...")
