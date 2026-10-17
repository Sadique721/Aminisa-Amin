# -*- coding: utf-8 -*-
"""
Aminsa Festival & Cultural Calendar Engine
Checks upcoming and active Indian festivals across all religions:
1. Python `holidays` library (IN)
2. Static verified fallback pan-Indian calendar
3. Google News India RSS query for cultural context
"""

import datetime as dt
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# Verified Pan-Indian Cultural & Multi-Faith Festivals
# Note: Lunar/solar dates are verified for 2026
STATIC_FESTIVALS_2026 = {
    # Date format: (Month, Day)
    (1, 14): {"name": "Makar Sankranti / Pongal", "faith": "Hindu / Cultural", "modest_ootd": "Vibrant festive mustard and cream raw silk kurta", "somber": False},
    (1, 26): {"name": "Republic Day of India", "faith": "National", "modest_ootd": "Crisp ivory khadi blazer with tricolor lapel pin", "somber": False},
    (2, 1): {"name": "Vasant Panchami", "faith": "Hindu", "modest_ootd": "Bright auspicious yellow cotton-silk salwar suit", "somber": False},
    (2, 15): {"name": "Maha Shivaratri", "faith": "Hindu", "modest_ootd": "Simple unadorned white linen modest kurta", "somber": True},
    (3, 4): {"name": "Holi", "faith": "Hindu / Cultural", "modest_ootd": "Comfortable pure white cotton kurta with floral accents", "somber": False},
    (3, 20): {"name": "Eid-ul-Fitr", "faith": "Islamic", "modest_ootd": "Elegant pastel emerald green embroidered modest Anarkali", "somber": False},
    (3, 22): {"name": "Ugadi / Gudi Padwa", "faith": "Hindu / Regional", "modest_ootd": "Rich bottle green and gold border Kasavu style saree", "somber": False},
    (4, 3): {"name": "Good Friday", "faith": "Christian", "modest_ootd": "Dignified dark navy modest button-down and trousers", "somber": True},
    (4, 5): {"name": "Easter Sunday", "faith": "Christian", "modest_ootd": "Soft lilac pastel modest blazer and cream trousers", "somber": False},
    (4, 14): {"name": "Baisakhi / Ambedkar Jayanti", "faith": "Sikh / National", "modest_ootd": "Bright royal blue and yellow Phulkari trimmed suit", "somber": False},
    (5, 1): {"name": "Buddha Purnima", "faith": "Buddhist", "modest_ootd": "Peaceful off-white khadi silk modest tunic", "somber": True},
    (5, 27): {"name": "Eid-ul-Adha", "faith": "Islamic", "modest_ootd": "Modest midnight blue georgette long kurta", "somber": False},
    (7, 26): {"name": "Muharram", "faith": "Islamic", "modest_ootd": "Sober black modest buttoned tunic and tailored trousers", "somber": True},
    (8, 15): {"name": "Independence Day", "faith": "National", "modest_ootd": "Tailored ivory blazer over saffron-accented formal top", "somber": False},
    (8, 28): {"name": "Raksha Bandhan", "faith": "Hindu / Cultural", "modest_ootd": "Soft peach and gold Banarasi woven modest suit", "somber": False},
    (9, 4): {"name": "Janmashtami", "faith": "Hindu", "modest_ootd": "Peacock blue silk kurta with delicate zari border", "somber": False},
    (9, 5): {"name": "Onam", "faith": "Cultural / Regional", "modest_ootd": "Classic Kerala Kasavu gold-bordered off-white attire", "somber": False},
    (9, 14): {"name": "Ganesh Chaturthi", "faith": "Hindu", "modest_ootd": "Vibrant marigold yellow and vermilion modest attire", "somber": False},
    (10, 11): {"name": "Navratri / Durga Puja", "faith": "Hindu / Cultural", "modest_ootd": "Traditional red and white Gorod silk modest drape", "somber": False},
    (10, 20): {"name": "Dussehra / Vijayadashami", "faith": "Hindu", "modest_ootd": "Deep crimson formal jacket and pleated trousers", "somber": False},
    (11, 8): {"name": "Diwali (Deepavali)", "faith": "Hindu / Pan-Indian", "modest_ootd": "Opulent royal purple and antique gold Banarasi silk", "somber": False},
    (11, 10): {"name": "Bhai Dooj", "faith": "Hindu / Cultural", "modest_ootd": "Warm blush pink Chanderi silk modest outfit", "somber": False},
    (11, 24): {"name": "Guru Nanak Jayanti", "faith": "Sikh", "modest_ootd": "Pure white modest attire with saffron scarf accent", "somber": True},
    (12, 25): {"name": "Christmas", "faith": "Christian", "modest_ootd": "Tailored ruby red wool blazer over cream knit top", "somber": False}
}

def festival_for(target_date=None):
    """
    Checks if given date (or today) is a festival day or a teaser day (day before).
    Returns dict with festival details or None.
    """
    d = target_date or dt.date.today()
    month, day = d.month, d.day

    # 1. Check Day of Festival
    if (month, day) in STATIC_FESTIVALS_2026:
        info = STATIC_FESTIVALS_2026[(month, day)]
        return {
            "status": "DAY_OF",
            "name": info["name"],
            "faith": info["faith"],
            "modest_ootd": info["modest_ootd"],
            "somber": info["somber"],
            "greeting_type": "somber_reflection" if info["somber"] else "joyful_celebration"
        }

    # 2. Check Teaser Day (Day before)
    tomorrow = d + dt.timedelta(days=1)
    t_month, t_day = tomorrow.month, tomorrow.day
    if (t_month, t_day) in STATIC_FESTIVALS_2026:
        info = STATIC_FESTIVALS_2026[(t_month, t_day)]
        return {
            "status": "TEASER",
            "name": info["name"],
            "faith": info["faith"],
            "modest_ootd": info["modest_ootd"],
            "somber": info["somber"],
            "greeting_type": "anticipation"
        }

    # 3. Dynamic Python holidays library check (if installed)
    try:
        import holidays
        in_holidays = holidays.country_holidays("IN")
        if d in in_holidays:
            hname = in_holidays.get(d)
            return {
                "status": "DAY_OF",
                "name": hname,
                "faith": "National / Public Holiday",
                "modest_ootd": "Smart professional ivory blazer and trousers",
                "somber": False,
                "greeting_type": "observance"
            }
    except Exception:
        pass

    return None
