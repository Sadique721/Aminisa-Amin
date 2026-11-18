# -*- coding: utf-8 -*-
"""
Aminsa Dynamic 7-Day Wardrobe & Setting Matrix Engine
====================================================
Eliminates static hardcoded outfits and locations.
Dynamically rotates Aminsa's attire and background setting across:
1. Day of the Week (Monday to Sunday)
2. Domain Category & Mood
3. Special Days & Festivals

Ensures Aminsa NEVER wears the exact same outfit two days in a row!
"""

from datetime import datetime

# 7-Day Thematic Matrix:
# Day 0: Monday    — Power Formal & Clean Structure
# Day 1: Tuesday   — Contemporary Smart Casual & Polished Pastels
# Day 2: Wednesday — Tech Innovator Chic & Minimalist Precision
# Day 3: Thursday  — Modern Indo-Western Tailored Fusion
# Day 4: Friday    — Vibrant Regional Handloom & Heritage Elegance
# Day 5: Saturday  — Creative Studio & Media Dynamic
# Day 6: Sunday    — Breathable Organic Wellness & Relaxed Poise

WARDROBE_MATRIX = {
    # 0 = Monday
    0: {
        "special_day_or_india_top": {
            "attire": "Graceful ivory khadi short kurti with subtle tricolor thread border",
            "setting": "Sunlit architectural Indian sandstone courtyard softly blurred",
            "attire_short": "ivory khadi kurti",
            "setting_short": "Sandstone courtyard"
        },
        "tech_ai": {
            "attire": "Crisp tailored midnight-navy blazer over a pristine white silk shell top",
            "setting": "Cutting-edge AI research studio with glass transparent data monitors",
            "attire_short": "midnight-navy blazer",
            "setting_short": "AI research studio"
        },
        "cricket_sports": {
            "attire": "Dynamic royal blue athletic zip-up jacket with structured white piping",
            "setting": "High-energy sports broadcast studio desk with backlit stadium lights",
            "attire_short": "royal blue athletic jacket",
            "setting_short": "Sports broadcast desk"
        },
        "economy_business": {
            "attire": "Elegantly tailored charcoal pinstripe blazer over emerald silk blouse",
            "setting": "Modern minimalist corporate boardroom overlooking high-rise skyline",
            "attire_short": "charcoal pinstripe blazer",
            "setting_short": "Corporate boardroom"
        },
        "culture_heritage": {
            "attire": "Vibrant mustard-yellow embroidered chanderi kurta with silver jhumkas",
            "setting": "Aesthetic heritage palace courtyard illuminated with warm brass lamps",
            "attire_short": "mustard chanderi kurta",
            "setting_short": "Heritage palace courtyard"
        },
        "bollywood_trends": {
            "attire": "Chic contemporary deep wine satin co-ord set with minimalist gold pendant",
            "setting": "Warm cinematic studio lounge with golden fairy lights and bokeh",
            "attire_short": "deep wine satin co-ord",
            "setting_short": "Cinematic lounge"
        },
        "science_isro": {
            "attire": "Clean slate grey tailored jacket with subtle metallic brushed accents",
            "setting": "High-tech space mission telemetry operations center with glowing screens",
            "attire_short": "slate grey smart jacket",
            "setting_short": "Space telemetry center"
        },
        "future_tech": {
            "attire": "Sleek jet-black technical blazer over obsidian mock-neck top",
            "setting": "Late-night modern developer laboratory with ambient cyan rim lighting",
            "attire_short": "black technical blazer",
            "setting_short": "Developer laboratory"
        },
        "global_affairs": {
            "attire": "Classic navy formal collared shirt with neatly rolled cuffs and gold watch",
            "setting": "Sophisticated global affairs briefing room with muted world map backdrop",
            "attire_short": "navy formal collared shirt",
            "setting_short": "Briefing studio room"
        },
        "wellness_health": {
            "attire": "Pastel peach breathable cotton yoga kurta with comfortable drawstring accents",
            "setting": "Lush green outdoor botanical terrace at sunrise with golden dawn mist",
            "attire_short": "pastel peach cotton kurta",
            "setting_short": "Botanical terrace"
        }
    },
    # 1 = Tuesday
    1: {
        "special_day_or_india_top": {
            "attire": "Earthy sage-green linen short kurta with delicate Kantha embroidery",
            "setting": "Aesthetic Indian university quadrangle with heritage arches",
            "attire_short": "sage-green linen kurta",
            "setting_short": "University quadrangle"
        },
        "tech_ai": {
            "attire": "Tailored graphite blazer with minimalist collarless neckline",
            "setting": "Futuristic cloud compute studio with violet and teal light accents",
            "attire_short": "graphite collarless blazer",
            "setting_short": "Cloud compute studio"
        },
        "cricket_sports": {
            "attire": "Sporty deep indigo breathable polo jersey with clean team trim",
            "setting": "Virtual sports arena analysis screen with live match scoreboards",
            "attire_short": "indigo sports polo",
            "setting_short": "Virtual sports arena"
        },
        "economy_business": {
            "attire": "Sharp coffee-brown structured formal blazer over ivory satin top",
            "setting": "Fintech innovation hub with modern wooden acoustic panels",
            "attire_short": "coffee-brown blazer",
            "setting_short": "Fintech hub"
        },
        "culture_heritage": {
            "attire": "Rich indigo blue Ajrakh block-print kurta with oxidized silver stud earrings",
            "setting": "Artisan craft gallery courtyard with handcrafted terracotta decor",
            "attire_short": "indigo Ajrakh kurta",
            "setting_short": "Craft gallery courtyard"
        },
        "bollywood_trends": {
            "attire": "Glamorous rose-gold accented modern blazer dress with sleek hair",
            "setting": "Contemporary entertainment podcast studio with acoustic wave panels",
            "attire_short": "rose-gold blazer dress",
            "setting_short": "Podcast studio lounge"
        },
        "science_isro": {
            "attire": "Clean arctic-white fitted smart jacket with deep blue lapel piping",
            "setting": "Spacecraft clean-room observation gallery with satellite blueprint displays",
            "attire_short": "arctic-white smart jacket",
            "setting_short": "Clean-room observation gallery"
        },
        "future_tech": {
            "attire": "Dark charcoal minimalist hoodie with subtle neon teal geometric logo",
            "setting": "Open-source developer workstation with dual curved 4K code screens",
            "attire_short": "charcoal designer hoodie",
            "setting_short": "Dual-screen workstation"
        },
        "global_affairs": {
            "attire": "Tailored charcoal grey single-breasted suit jacket over powder blue shirt",
            "setting": "International diplomatic media center with translucent glass podium",
            "attire_short": "charcoal suit jacket",
            "setting_short": "Diplomatic media center"
        },
        "wellness_health": {
            "attire": "Crisp mint-green organic cotton wellness tunic with relaxed fit",
            "setting": "Serene bamboo garden with natural morning dew and stone water fountain",
            "attire_short": "mint-green cotton tunic",
            "setting_short": "Bamboo garden terrace"
        }
    },
    # 2 = Wednesday
    2: {
        "special_day_or_india_top": {
            "attire": "Pristine white handloom khadi shirt kurta with tricolor silk pocket square",
            "setting": "Historic colonial Indian portico bathed in soft natural daylight",
            "attire_short": "white handloom khadi kurta",
            "setting_short": "Colonial portico"
        },
        "tech_ai": {
            "attire": "Modern cobalt blue structured blazer over minimalist dark grey top",
            "setting": "Sleek neural network visualization lounge with holographic blue rings",
            "attire_short": "cobalt blue blazer",
            "setting_short": "Neural network studio"
        },
        "cricket_sports": {
            "attire": "Athletic black track jacket with electric blue sleeve stripes",
            "setting": "High-tech sports biomechanics testing pavilion with track view",
            "attire_short": "black & blue track jacket",
            "setting_short": "Sports testing pavilion"
        },
        "economy_business": {
            "attire": "Warm camel-tan tailored blazer paired with a crisp cream silk shirt",
            "setting": "Venture capital investor lounge with panoramic city skyline windows",
            "attire_short": "camel-tan blazer",
            "setting_short": "VC investor lounge"
        },
        "culture_heritage": {
            "attire": "Graceful maroon and gold Bagru printed kurti with delicate silver cuffs",
            "setting": "Traditional Indian courtyard with carved jharokha window balconies",
            "attire_short": "maroon Bagru printed kurti",
            "setting_short": "Carved jharokha courtyard"
        },
        "bollywood_trends": {
            "attire": "Sleek emerald green contemporary trouser suit with dainty gold layered chain",
            "setting": "Modern cinema studio set with warm ambient spotlights and directors chair",
            "attire_short": "emerald green trouser suit",
            "setting_short": "Cinema studio set"
        },
        "science_isro": {
            "attire": "Astronomy-inspired deep navy tailored blazer with silver stellar badge",
            "setting": "Astronomical telescope dome facility looking out at star field",
            "attire_short": "navy blazer with stellar badge",
            "setting_short": "Telescope dome facility"
        },
        "future_tech": {
            "attire": "Futuristic matte obsidian cyber-jacket with clean mandarin collar",
            "setting": "Quantum computing server hall with ambient purple luminescence",
            "attire_short": "obsidian cyber-jacket",
            "setting_short": "Quantum computing server hall"
        },
        "global_affairs": {
            "attire": "Deep olive-grey formal blazer over an off-white silk shell top",
            "setting": "Global multilateral conference hall with polished mahogany desk",
            "attire_short": "olive-grey formal blazer",
            "setting_short": "Multilateral conference hall"
        },
        "wellness_health": {
            "attire": "Pure white breathable organic cotton kurta with pale lavender piping",
            "setting": "Sunlit meditation deck surrounded by calming water lilies and greenery",
            "attire_short": "white organic kurta",
            "setting_short": "Sunlit meditation deck"
        }
    },
    # 3 = Thursday
    3: {
        "special_day_or_india_top": {
            "attire": "Royal saffron-tinted khadi short kurta with mother-of-pearl buttons",
            "setting": "Vibrant Indian central vista promenade with lush green lawns",
            "attire_short": "saffron khadi kurta",
            "setting_short": "Central vista promenade"
        },
        "tech_ai": {
            "attire": "Sleek metallic titanium blazer over charcoal ribbed modal top",
            "setting": "Robotics innovation incubator with glowing robotic arms in background",
            "attire_short": "titanium blazer",
            "setting_short": "Robotics incubator"
        },
        "cricket_sports": {
            "attire": "Crisp white cricket-commentator polo jacket with navy chest crest",
            "setting": "Cricket commentary box overlooking iconic stadium pitch and crowd",
            "attire_short": "commentator polo jacket",
            "setting_short": "Commentary box"
        },
        "economy_business": {
            "attire": "Deep navy pinstripe tailored jacket over champagne silk blouse",
            "setting": "Stock exchange trading terminal gallery with real-time ticker glow",
            "attire_short": "navy pinstripe jacket",
            "setting_short": "Trading terminal gallery"
        },
        "culture_heritage": {
            "attire": "Teal and gold woven Chanderi kurti with delicate pearl ear drops",
            "setting": "Historic temple stepwell architecture with symmetrical stone arches",
            "attire_short": "teal Chanderi kurti",
            "setting_short": "Historic stepwell arches"
        },
        "bollywood_trends": {
            "attire": "Sophisticated black velvet tailored blazer over champagne silk cami",
            "setting": "Film festival media lounge with subtle spotlight bokeh and awards glow",
            "attire_short": "black velvet blazer",
            "setting_short": "Film festival media lounge"
        },
        "science_isro": {
            "attire": "Clean aerospace-blue zip utility jacket with clean technical pockets",
            "setting": "Rocket integration facility with modular launch vehicle components",
            "attire_short": "aerospace-blue utility jacket",
            "setting_short": "Rocket integration facility"
        },
        "future_tech": {
            "attire": "Modern slate-grey asymmetric designer jacket over dark grey tee",
            "setting": "Web3 decentralized computing lab with flowing data matrix backdrop",
            "attire_short": "asymmetric designer jacket",
            "setting_short": "Decentralized computing lab"
        },
        "global_affairs": {
            "attire": "Elegant burgundy formal blazer over a crisp ivory shirt",
            "setting": "Sovereign diplomacy summit press briefing room with international flags",
            "attire_short": "burgundy formal blazer",
            "setting_short": "Diplomacy summit room"
        },
        "wellness_health": {
            "attire": "Soft amber-toned breathable linen yoga tunic with loose cotton pants",
            "setting": "Himalayan pine wood open-air yoga shala with mist in the background",
            "attire_short": "amber linen yoga tunic",
            "setting_short": "Himalayan yoga shala"
        }
    },
    # 4 = Friday
    4: {
        "special_day_or_india_top": {
            "attire": "Graceful deep indigo handloom kurta with silver zari thread border",
            "setting": "Grand stone heritage courtyard illuminated with golden evening torches",
            "attire_short": "indigo handloom kurta",
            "setting_short": "Heritage courtyard with torches"
        },
        "tech_ai": {
            "attire": "Ultra-sleek carbon-black tailored blazer with neon cyan lapel stitching",
            "setting": "Autonomous AI compute center with blue fiber-optic server arrays",
            "attire_short": "carbon-black blazer",
            "setting_short": "AI compute center"
        },
        "cricket_sports": {
            "attire": "Electric cyan sporty bomber jacket over charcoal athletic crewneck",
            "setting": "High-tech locker room broadcast corridor with digital tactical board",
            "attire_short": "cyan athletic bomber jacket",
            "setting_short": "Tactical broadcast corridor"
        },
        "economy_business": {
            "attire": "Impeccably tailored steel-blue formal suit jacket with ivory blouse",
            "setting": "Modern startup incubator glass atrium with lush indoor vertical garden",
            "attire_short": "steel-blue formal jacket",
            "setting_short": "Startup incubator atrium"
        },
        "culture_heritage": {
            "attire": "Regal ruby-red Banarasi silk short kurta with antique gold jhumkas",
            "setting": "Illuminated classical Indian music amphitheater with marigold decor",
            "attire_short": "ruby-red Banarasi kurta",
            "setting_short": "Music amphitheater"
        },
        "bollywood_trends": {
            "attire": "Contemporary midnight-blue satin shirt with statement silver cuffs",
            "setting": "Celebrity studio talk-show set with plush velvet chairs and warm glow",
            "attire_short": "midnight-blue satin shirt",
            "setting_short": "Talk-show studio set"
        },
        "science_isro": {
            "attire": "Technical graphite-grey lab jacket with embroidered mission insignia",
            "setting": "Deep space tracking antenna station under clear twilight skies",
            "attire_short": "graphite lab jacket",
            "setting_short": "Space tracking station"
        },
        "future_tech": {
            "attire": "Minimalist onyx designer hoodie with geometric holographic chest print",
            "setting": "Late-night cyber-security command workstation with multimonitor glow",
            "attire_short": "onyx designer hoodie",
            "setting_short": "Cyber command workstation"
        },
        "global_affairs": {
            "attire": "Polished charcoal tailored blazer over fine-weave white cotton shirt",
            "setting": "Global geopolitical round-table studio with interactive digital globe",
            "attire_short": "charcoal tailored blazer",
            "setting_short": "Round-table studio"
        },
        "wellness_health": {
            "attire": "Calming seafoam-green bamboo cotton kurta with relaxed drape",
            "setting": "Peaceful herbal botanical conservatory filled with medicinal plants",
            "attire_short": "seafoam bamboo kurta",
            "setting_short": "Botanical conservatory"
        }
    },
    # 5 = Saturday
    5: {
        "special_day_or_india_top": {
            "attire": "Casual chic ivory linen blazer over terracotta cotton short top",
            "setting": "Modern Indian cultural center terrace overlooking historic monuments",
            "attire_short": "linen blazer over terracotta top",
            "setting_short": "Cultural center terrace"
        },
        "tech_ai": {
            "attire": "Smart casual navy knit blazer over a crisp minimalist grey tee",
            "setting": "Open tech co-working space with floor-to-ceiling glass and green plants",
            "attire_short": "navy knit blazer",
            "setting_short": "Open co-working space"
        },
        "cricket_sports": {
            "attire": "Stylish tri-color accented track jacket with clean aerodynamic cut",
            "setting": "Weekend sports fan zone studio with dynamic LED match screens",
            "attire_short": "tri-color track jacket",
            "setting_short": "Sports fan zone studio"
        },
        "economy_business": {
            "attire": "Modern structured olive green blazer over crisp white linen top",
            "setting": "Contemporary rooftop executive cafe overlooking weekend business bay",
            "attire_short": "olive green blazer",
            "setting_short": "Rooftop business cafe"
        },
        "culture_heritage": {
            "attire": "Handcrafted mustard and indigo block-printed contemporary shirt tunic",
            "setting": "Open-air Indian craft bazaar with vibrant textiles and pottery displays",
            "attire_short": "block-printed shirt tunic",
            "setting_short": "Craft bazaar set"
        },
        "bollywood_trends": {
            "attire": "Effortlessly stylish emerald satin blazer dress with delicate earrings",
            "setting": "Weekend entertainment lounge with warm fairy lights and acoustic guitars",
            "attire_short": "emerald satin blazer dress",
            "setting_short": "Weekend entertainment lounge"
        },
        "science_isro": {
            "attire": "Deep navy technical bomber jacket with clean national space crest",
            "setting": "Interactive science museum dome with planetary projection overhead",
            "attire_short": "navy space bomber jacket",
            "setting_short": "Science museum dome"
        },
        "future_tech": {
            "attire": "Dark heather-grey technical jacket over clean graphic developer tee",
            "setting": "Hackathon maker lab with 3D printers and glowing dev terminals",
            "attire_short": "technical grey jacket",
            "setting_short": "Hackathon maker lab"
        },
        "global_affairs": {
            "attire": "Tailored navy blazer over powder-blue polo shirt with subtle watch",
            "setting": "Weekend global intelligence debrief lounge with world news wall",
            "attire_short": "navy blazer with polo",
            "setting_short": "Global debrief lounge"
        },
        "wellness_health": {
            "attire": "Pure white breathable organic cotton kurta with relaxed linen trousers",
            "setting": "Weekend sunrise yoga retreat deck surrounded by mist-covered hills",
            "attire_short": "white organic kurta",
            "setting_short": "Sunrise retreat deck"
        }
    },
    # 6 = Sunday
    6: {
        "special_day_or_india_top": {
            "attire": "Serene white cotton Lucknowi Chikankari short kurta with pearl studs",
            "setting": "Tranquil Sunday morning courtyard filled with golden morning sunlight",
            "attire_short": "white Chikankari kurta",
            "setting_short": "Morning courtyard"
        },
        "tech_ai": {
            "attire": "Clean modern ivory tailored jacket over dark slate mock-neck top",
            "setting": "Futuristic glass greenhouse lab merging biotechnology and AI arrays",
            "attire_short": "ivory tailored jacket",
            "setting_short": "Bio-AI greenhouse lab"
        },
        "cricket_sports": {
            "attire": "Classic navy sports jacket with clean white collar and athletic crest",
            "setting": "Sunday match preview broadcast lounge with comfortable leather seating",
            "attire_short": "navy sports jacket",
            "setting_short": "Match preview lounge"
        },
        "economy_business": {
            "attire": "Relaxed tailored beige blazer over soft champagne crewneck silk top",
            "setting": "Quiet Sunday executive library with floor-to-ceiling wooden bookshelves",
            "attire_short": "beige tailored blazer",
            "setting_short": "Executive library"
        },
        "culture_heritage": {
            "attire": "Graceful saffron and cream handspun khadi kurta with delicate silver hoops",
            "setting": "Heritage stepwell pavilion surrounded by lush green marigold gardens",
            "attire_short": "saffron & cream khadi kurta",
            "setting_short": "Stepwell pavilion"
        },
        "bollywood_trends": {
            "attire": "Chic mauve-pink contemporary tailored blazer over white silk top",
            "setting": "Sunday cinema retrospective lounge with warm golden tungsten lights",
            "attire_short": "mauve-pink blazer",
            "setting_short": "Cinema retrospective lounge"
        },
        "science_isro": {
            "attire": "Clean slate-blue smart casual blazer with polished silver lapel pin",
            "setting": "Solar observatory rooftop overlooking morning horizon and clear skies",
            "attire_short": "slate-blue smart blazer",
            "setting_short": "Solar observatory rooftop"
        },
        "future_tech": {
            "attire": "Sleek dark olive technical hoodie with subtle minimalist branding",
            "setting": "Open creative design lab with drafting tables and digital stylus monitors",
            "attire_short": "dark olive technical hoodie",
            "setting_short": "Creative design lab"
        },
        "global_affairs": {
            "attire": "Classic dark navy formal collared shirt with structured trousers",
            "setting": "Diplomatic weekend retrospective studio with soft ambient warm lights",
            "attire_short": "dark navy collared shirt",
            "setting_short": "Retrospective studio"
        },
        "wellness_health": {
            "attire": "Ultra-breathable natural linen kurta in calming sage green",
            "setting": "Peaceful Ayurvedic wellness sanctuary garden with stone walkways",
            "attire_short": "sage green linen kurta",
            "setting_short": "Sanctuary garden"
        }
    }
}


def get_dynamic_wardrobe_and_setting(category_key: str, target_dt=None) -> dict:
    """
    Returns the dynamically rotated wardrobe and contextual setting
    based on the day of week (0=Mon .. 6=Sun) and category.
    """
    if not target_dt:
        target_dt = datetime.now()
    
    day_idx = target_dt.weekday()  # 0 to 6
    day_matrix = WARDROBE_MATRIX.get(day_idx, WARDROBE_MATRIX[0])
    
    # Category fallback
    look = day_matrix.get(category_key, day_matrix.get("special_day_or_india_top"))
    if not look:
        look = {
            "attire": "Elegantly tailored modern chic blazer over minimalist top",
            "setting": "Contemporary high-tech studio lounge with ambient rim lighting",
            "attire_short": "tailored modern blazer",
            "setting_short": "Modern studio lounge"
        }
    return look
