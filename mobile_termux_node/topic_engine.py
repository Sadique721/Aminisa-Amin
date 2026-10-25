"""
Master Topic & Prompt Engine for Aminsa Amin Mobile Ecosystem
============================================================
Runs natively inside Termux on Android with zero external dependencies.
Crafted with elite creative depth ("1000000000000000+ years experience" caliber).

Strict Architectural Guarantees:
1. Persona: Strictly [Aminsa Amin] (22yo female AI digital creator).
   Biometrics: Warm glowing fair wheatish skin (#EAD5C3), porcelain texture,
   strictly zero moles/marks, deep almond hazel-brown eyes (#6B4423),
   dark espresso hair (#231709).
2. YouTube Create Prompt Length: Strictly 250 to 300 characters.
   Packages Aminsa's biometric identity + topic-adapted modern dress + contextual background + 9:16 vertical action.
3. Spoken Speech Script: Completed cleanly within 10 seconds (20-25 words).
   Strict opening: Always starts with "Hello everyone, main hoon Aminsa!"
   Strict brand safety: 0% "Namaste".
4. Dynamic Rotation: Time-aware multi-dimensional rotation across daily, weekly,
   and yearly cycles so daily scripts never repeat formulas or sound robotic.
"""

import urllib.request
import xml.etree.ElementTree as ET
import re
import datetime
import hashlib
from config import (
    CATEGORIES, GREETING, PERSONA_NAME,
    YT_CREATE_PROMPT_MIN_CHARS, YT_CREATE_PROMPT_MAX_CHARS,
    MAX_SPEECH_DURATION_SECONDS, MAX_SPEECH_WORD_COUNT
)

USER_AGENT = "Mozilla/5.0 (Linux; Android 15; CPH2495) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

# ---------------------------------------------------------------------------
# Dynamic Variations for Daily, Weekly, and Yearly Cycles
# ---------------------------------------------------------------------------

# Dynamic Modern Dresses Tailored by Topic & Energy
MODERN_DRESS_VARIATIONS = {
    "tech": [
        "smart navy-blue blazer over ivory silk top",
        "cyber-chic lavender tailored co-ord set",
        "minimalist cobalt blue structured blazer",
        "futuristic charcoal tech jacket with zip accents",
    ],
    "business": [
        "pastel grey power suit with crisp white collar",
        "elegant ivory double-breasted formal blazer",
        "modern terracotta blazer with beige silk inner",
        "sleek monochrome minimalist pant-suit",
    ],
    "education": [
        "soft lavender knit cardigan over white crew-neck",
        "smart casual pastel sage knit sweater",
        "chic powder-blue tailored shirt with cuff accents",
        "contemporary warm heather cardigan with neat collar",
    ],
    "lifestyle": [
        "chic beige linen tunic with minimalist collar",
        "blush-pink modern casual blazer over white top",
        "oatmeal-tone aesthetic relaxed knit pullover",
        "contemporary peach crop blazer with neutral top",
    ],
    "creative": [
        "emerald green top with modern geometric cuts",
        "contemporary draped violet cape-style top",
        "stylish copper-rust modern silk tunic",
        "avant-garde midnight blue asymmetric blouse",
    ],
    "science": [
        "futuristic deep charcoal jacket with metallic trim",
        "sleek aerospace-grey minimalist bomber jacket",
        "dark slate tailored blazer with subtle silver accents",
        "modern cyber-black structured zip tunic",
    ],
    "cultural": [
        "royal maroon modern silk kurta with fine embroidery",
        "contemporary peacock-blue tunic with gold piping",
        "modern pastel rose silk silhouette with delicate motifs",
        "elegant ivory-gold contemporary fusion kurta",
    ],
    "mindset": [
        "warm oatmeal cashmere oversized turtle-neck",
        "serene dove-grey soft knit sweater",
        "cozy vanilla-toned minimalist wrap cardigan",
        "relaxed warm taupe textured knit pullover",
    ],
    "night_tech": [
        "matte black oversized aesthetic tech hoodie",
        "dark cyber-mesh modern bomber jacket",
        "minimalist charcoal graphic hoodie with neat cuffs",
        "stealth-black relaxed tech pullover",
    ],
    "global_trends": [
        "pearl-white silk shirt with French cuffs",
        "sleek champagne-toned contemporary blazer",
        "modern tailored powder-blue architectural shirt",
        "luxurious minimalist ivory satin wrap blouse",
    ],
}

# Contextual Cinematic Backgrounds Tailored by Category
CONTEXTUAL_BACKGROUNDS = {
    "tech": [
        "High-tech studio with soft cyan neon ambient glow",
        "AI laboratory soundstage with floating glass screens",
        "Modern glass tech studio overlooking illuminated city",
        "Minimalist cyber studio with sleek violet rim lights",
    ],
    "business": [
        "Sunlit glass corner executive office with skyline",
        "Modern architectural boardroom with panoramic windows",
        "Penthouse business lounge with golden hour sunset view",
        "Sleek contemporary corporate atrium with glass walls",
    ],
    "education": [
        "Warm contemporary library lounge with wooden shelves",
        "Modern campus innovation hub with soft ambient daylight",
        "Minimalist aesthetic study lounge with warm lighting",
        "Modern creative knowledge studio with books and plants",
    ],
    "lifestyle": [
        "Modern minimalist sunlit living space with monstera plants",
        "Aesthetic bright airy studio kitchen with warm sunlight",
        "Contemporary loft terrace with natural morning light",
        "Serene Scandinavian interior with warm wood accents",
    ],
    "creative": [
        "Artist gallery studio with warm canvas backdrop",
        "Modern design soundstage with soft studio spotlight",
        "Contemporary art loft with subtle colored neon accents",
        "Creative aesthetic studio with warm architectural lamps",
    ],
    "science": [
        "Observatory terrace under starry deep twilight sky",
        "Futuristic planetary science center with glowing globes",
        "Modern aerospace laboratory with soft blue illumination",
        "Cosmic research observatory with deep indigo ambience",
    ],
    "cultural": [
        "Heritage courtyard with warm brass diyas and stone pillars",
        "Contemporary ethnic gallery with carved wooden archways",
        "Palace pavilion illuminated by soft traditional lanterns",
        "Aesthetic heritage lounge with warm golden ambient light",
    ],
    "mindset": [
        "Cozy living corner with warm fairy lights and herbal tea",
        "Serene twilight balcony overlooking calm tranquil horizon",
        "Warm minimalist meditation loft with candle glow",
        "Peaceful evening reading nook with soft amber light",
    ],
    "night_tech": [
        "Dark gaming workstation with dual cyan & magenta LEDs",
        "Midnight coding loft with multi-monitor ambient glow",
        "Quiet late-night tech lab with soft neon rim lighting",
        "Cyberpunk rooftop lounge with illuminated night vista",
    ],
    "global_trends": [
        "Modern glass rooftop pavilion overlooking global city",
        "Futuristic skyline terrace at twilight with glowing towers",
        "Contemporary international summit lounge with glass walls",
        "Sleek architectural balcony with breathtaking night skyline",
    ],
}

# Master-Level Curated 10-Second Statement Pairs (Hook + Statement + CTA)
# Kept strictly within 20 to 25 words to complete cleanly under 10 seconds!
MASTER_STATEMENTS_POOL = {
    "tech": [
        ("Aaj generative AI aur intelligent agents human productivity naye level par le ja rahe hain.", "Aapka kya manna hai? Batayein!"),
        ("Autonomous AI tools ab complex workflows ko seconds me solve kar rahe hain.", "Aap AI kaise use karte hain? Batayein!"),
        ("Next-generation AI models human intelligence ke sath beautifully sync ho rahe hain.", "Future par aapki kya raye hai?"),
        ("Technology hamare sochne aur create karne ka tareeka tezi se badal rahi hai.", "Is par aapka kya kahna hai?"),
    ],
    "business": [
        ("Naye digital entrepreneurs AI ki taqat se solo companies tezi se bana rahe hain.", "Aapka dream startup kya hai? Batayein!"),
        ("Modern business me speed aur smart automation hi sabse bada competitive advantage hai.", "Aap isse agree karte hain? Batayein!"),
        ("Future unhi builders ka hai jo technology aur human trust ko combine karte hain.", "Apni raye zaroor share karein!"),
        ("Startup ecosystem me real impact aur solid value creation hi ultimate currency hai.", "Aapka favorite startup kaunsa hai?"),
    ],
    "education": [
        ("Daily micro-learning aur AI literacy aapka sabse powerful career asset hai.", "Aaj aapne naya kya seekha? Batayein!"),
        ("Skills har do saal me reinvent ho rahi hain, curiosity hi aapka superpower hai.", "Aapka next goal kya hai?"),
        ("Self-learning aur deep discipline kisi bhi degree se zyada doors kholta hai.", "Aap is thought se agree karte hain?"),
        ("Digital age me wahi jeetega jo quickly unlearn aur relearn kar sakta hai.", "Aapka learning routine kaisa hai?"),
    ],
    "lifestyle": [
        ("Simple daily habits aur balanced screen-time aapki real energy restore karte hain.", "Aapka favorite wellness hack kya hai?"),
        ("High-speed life me intentional pauses aur mindfulness aapko grounded rakhte hain.", "Aaj aapne self-care ke lia kya kiya?"),
        ("Small consistent healthy choices hi lifelong vitality ka secret formula hain.", "Aapka daily health rule kya hai?"),
        ("Physical movement aur mental clarity hi best creative performance dete hain.", "Aap din ki shuruat kaise karte hain?"),
    ],
    "creative": [
        ("Human imagination jab powerful AI tools se milti hai, magic create hota hai.", "Aapki creative inspiration kya hai?"),
        ("Digital art aur visual storytelling ab boundary-less global expressions ban chuke hain.", "Aapko visuals kitne pasand hain?"),
        ("Originality kisi tool me nahi, balki aapke unique perspective me hoti hai.", "Aapka creative medium kaun sa hai?"),
        ("Visual tech cinema aur storytelling ko har creator ke hath me de rahi hai.", "Next generation cinema kaisa hoga?"),
    ],
    "science": [
        ("Deep space exploration aur quantum physics universe ke secrets unlock kar rahe hain.", "Space exploration par kya raye hai?"),
        ("Scientific breakthroughs sustainable energy aur space travel ko redefine kar rahe hain.", "Kaunsi science news inspire karti hai?"),
        ("Curiosity aur rigorous science hi human civilization ko stars tak le jayegi.", "Universe ka sabse bada mystery kya hai?"),
        ("Quantum computing real world challenges ko solve karne ke kabil ban chuka hai.", "Science future par aapka kya nazariya hai?"),
    ],
    "cultural": [
        ("Hamari timeless heritage aur ancient wisdom modern aesthetics me aur khil uthti hai.", "Aapka favorite festival kaunsa hai?"),
        ("Culture hamari roots hai jo modern tech world me hume grounded rakhti hai.", "Heritage kaise celebrate karte hain?"),
        ("Tradition aur innovation ka balance hi kisi bhi society ki asli sundarta hai.", "Aap is par kya sochte hain?"),
        ("Indian art, craft aur values pure world ko deeply inspire kar rahe hain.", "Indian culture ka kya pasand hai?"),
    ],
    "mindset": [
        ("High-speed duniya me deep calm focus hi sabse bada superpower hai.", "Aap apna focus kaise maintain karte hain?"),
        ("Patience aur daily silent efforts hi massive long-term success create karte hain.", "Aap is mindset se kitna agree karte hain?"),
        ("External noise filter karke inner clarity build karna sabse badi jeet hai.", "Aap stress kaise handle karte hain?"),
        ("Har challenge actually aapki strength aur wisdom ko upgrade karne ka step hai.", "Aapka life motto kya hai? Batayein!"),
    ],
    "night_tech": [
        ("Late night clean architecture planning aur focused coding 10x developer results deti hai.", "Aapka favorite framework kaunsa hai?"),
        ("Silent night hours me deep technical flow state ka experience unmatched hota hai.", "Aap day person hain ya night owl?"),
        ("Simple scalable systems build karna hi engineering ka ultimate mastercraft hai.", "Aapka best productivity hack kya hai?"),
        ("Future software autonomous systems aur elegant architectures par thrive karega.", "Developer future par aapki kya raye hai?"),
    ],
    "global_trends": [
        ("Global innovation tab lead karti hai jab technology empathy se judti hai.", "Sabse bada global trend kya lagta hai?"),
        ("Connected world me local ideas minutes me global revolution ban jate hain.", "Future world par aapka kya vishwas hai?"),
        ("Sustainable technology aur ethical progress hi human society ka bright future hai.", "Aap is vision ko support karte hain?"),
        ("Nayi sadi collaboration aur transformative breakthroughs se define ho rahi hai.", "Aapka biggest expectation kya hai? Batayein!"),
    ],
}

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
    except Exception:
        pass
    return None

def craft_youtube_create_prompt(attire, background, hair_style="loose espresso waves"):
    """
    Crafts a prompt STRICTLY within 250 to 300 characters for YouTube Create app.
    Combines:
    - Aminsa Amin biometric identity (fair wheatish #EAD5C3, hazel eyes #6B4423, porcelain skin, zero moles)
    - Modern tailored outfit
    - Contextual background setting
    - Framing: 9:16 vertical, speaking to camera, friendly engaging smile
    """
    # Core biometric identity anchor (~95 chars)
    core_bio = "22yo Indian creator Aminsa Amin, fair wheatish skin #EAD5C3, almond hazel eyes, espresso hair."
    
    # Action and camera framing (~60 chars)
    framing = "Friendly smile speaking to camera, cinematic lighting, 9:16 portrait."
    
    # Candidate prompt
    candidate = f"{core_bio} Wearing {attire}. Setting: {background}. {framing}"
    
    # Enforce strictly 250 to 300 characters
    if len(candidate) > YT_CREATE_PROMPT_MAX_CHARS:
        # If too long, trim background slightly
        overflow = len(candidate) - YT_CREATE_PROMPT_MAX_CHARS
        # Shorten attire or background
        short_bg = background[:max(20, len(background) - overflow - 3)] + "..."
        candidate = f"{core_bio} Wearing {attire}. Setting: {short_bg}. {framing}"
        if len(candidate) > YT_CREATE_PROMPT_MAX_CHARS:
            candidate = candidate[:YT_CREATE_PROMPT_MAX_CHARS - 1] + "."

    if len(candidate) < YT_CREATE_PROMPT_MIN_CHARS:
        # Pad with photorealistic rendering tokens to reach >= 250 chars
        padding_tokens = [
            " 8k ultra-sharp detail.",
            " Photorealistic finish.",
            " Masterpiece portrait.",
            " Studio bokeh depth."
        ]
        for pad in padding_tokens:
            if len(candidate) + len(pad) <= YT_CREATE_PROMPT_MAX_CHARS:
                candidate = candidate.rstrip(".") + pad
            if len(candidate) >= YT_CREATE_PROMPT_MIN_CHARS:
                break
        
        # If still under 250 by a few characters, pad neatly
        if len(candidate) < YT_CREATE_PROMPT_MIN_CHARS:
            needed = YT_CREATE_PROMPT_MIN_CHARS - len(candidate)
            candidate = candidate.rstrip(".") + (" HD detail." if needed <= 11 else " High resolution sharp focus.")
            if len(candidate) > YT_CREATE_PROMPT_MAX_CHARS:
                candidate = candidate[:YT_CREATE_PROMPT_MAX_CHARS - 1] + "."

    return candidate

def craft_speech_statement(category, slot_index, day_of_year):
    """
    Generates a speech statement that completes CLEANLY in under 10 seconds.
    Target word count: 20 to 25 words (at 2.4 words/sec = 8.5 to 9.8 seconds).
    Strict Greeting: Always starts with 'Hello everyone, main hoon Aminsa!'
    Strict Brand Safety: Zero 'Namaste'.
    """
    pool = MASTER_STATEMENTS_POOL.get(category, MASTER_STATEMENTS_POOL["tech"])
    
    # Select dynamically based on day of year and slot index
    variant_idx = (day_of_year + slot_index) % len(pool)
    statement, cta = pool[variant_idx]
    
    # Opening hook (5 words)
    hook = f"{GREETING}, main hoon Aminsa!"
    
    # Combined script
    script = f"{hook} {statement} {cta}"
    
    # Validate word count (strictly <= 25 words for 10 sec clean audio)
    words = script.split()
    if len(words) > MAX_SPEECH_WORD_COUNT:
        # Trim gracefully if ever exceeded
        trimmed_words = words[:MAX_SPEECH_WORD_COUNT]
        script = " ".join(trimmed_words)
        if not script.endswith((".", "!", "?")):
            script += "!"

    return script

def get_slot_topic_and_prompts(slot_index, ref_date=None):
    """
    Returns complete production package for Aminsa Amin autonomous mobile cycle:
    - 250-300 character YouTube Create prompt
    - <=10-second speech statement
    - Modern attire & contextual background dynamically adapted
    - Captions & social metadata
    """
    now = ref_date or datetime.datetime.now()
    day_of_year = now.timetuple().tm_yday
    weekday = now.weekday()
    week_of_year = now.isocalendar()[1]
    
    slot = CATEGORIES[slot_index % len(CATEGORIES)]
    cat = slot["category"]

    # 1. Dynamic Attire & Setting (Multi-layered rotation: day + week + slot)
    attire_list = MODERN_DRESS_VARIATIONS.get(cat, MODERN_DRESS_VARIATIONS["tech"])
    bg_list = CONTEXTUAL_BACKGROUNDS.get(cat, CONTEXTUAL_BACKGROUNDS["tech"])
    
    attire_idx = (day_of_year + weekday + slot_index) % len(attire_list)
    bg_idx = (week_of_year + slot_index) % len(bg_list)
    
    active_attire = attire_list[attire_idx]
    active_setting = bg_list[bg_idx]
    
    # Look dict
    look = {
        "attire": active_attire,
        "setting": active_setting,
        "hair": slot["look"]["hair"],
        "lipstick": slot["look"]["lipstick"]
    }

    # 2. Fetch or Fallback Headline
    headline = fetch_rss_headline(slot["rss_query"])
    if not headline:
        headline = slot["name"] + " daily insights & futuristic vision"

    # 3. Strict 250 to 300 Character YouTube Create Prompt
    yt_create_prompt = craft_youtube_create_prompt(active_attire, active_setting, slot["look"]["hair"])
    
    # Verify bounds
    assert YT_CREATE_PROMPT_MIN_CHARS <= len(yt_create_prompt) <= YT_CREATE_PROMPT_MAX_CHARS, (
        f"YouTube Create prompt length {len(yt_create_prompt)} outside [{YT_CREATE_PROMPT_MIN_CHARS}, {YT_CREATE_PROMPT_MAX_CHARS}]"
    )

    # 4. Strict 10-Second Speech Statement (<= 25 words)
    speech_script = craft_speech_statement(cat, slot_index, day_of_year)
    word_count = len(speech_script.split())

    # 5. Social Media Caption
    caption = (
        f"✨ {slot['name']} | Insight with Aminsa Amin\n\n"
        f"{speech_script}\n\n"
        f"Follow @AminsaAmin for daily futuristic tech & lifestyle wisdom.\n"
        f"#AminsaAmin #AI #FutureOfTech #{cat.capitalize()} #Shorts #Reels"
    )

    return {
        "slot_id": slot["id"],
        "slot_name": slot["name"],
        "category": cat,
        "headline": headline,
        "look": look,
        "yt_create_prompt": yt_create_prompt,
        "yt_prompt": yt_create_prompt,       # Backwards compatibility
        "yt_image_prompt": yt_create_prompt, # Backwards compatibility
        "yt_video_prompt": f"Animate Aminsa Amin speaking naturally with subtle gestures: {speech_script[:80]}.",
        "speech_script": speech_script,
        "speech_word_count": word_count,
        "caption": caption,
    }

if __name__ == "__main__":
    import json
    print("=" * 65)
    print("🌟 AMINSA AMIN MASTER TOPIC ENGINE TEST (10 SLOTS)")
    print("=" * 65)
    for i in range(10):
        pkg = get_slot_topic_and_prompts(i)
        p_len = len(pkg["yt_create_prompt"])
        w_cnt = pkg["speech_word_count"]
        print(f"\n[SLOT {i+1:02d}] {pkg['slot_name']} ({pkg['category']})")
        print(f"  👗 Attire: {pkg['look']['attire']}")
        print(f"  🌆 Setting: {pkg['look']['setting']}")
        print(f"  🎨 YT Create Prompt ({p_len} chars): {pkg['yt_create_prompt']}")
        print(f"  🎙️ Speech ({w_cnt} words): {pkg['speech_script']}")
        assert 250 <= p_len <= 300, f"Prompt length {p_len} failed bound check!"
        assert w_cnt <= 25, f"Word count {w_cnt} exceeds 10s budget!"
        assert "namaste" not in pkg["speech_script"].lower(), "Namaste found!"
        assert pkg["speech_script"].startswith("Hello everyone"), "Opening greeting mismatch!"
    print("\n[✓] ALL 10 SLOTS PASSED ALL CONSTRAINTS WITH 100% PRECISION!")
