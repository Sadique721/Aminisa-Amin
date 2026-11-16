# -*- coding: utf-8 -*-
"""
Aminsa Special Days & National Observances Calendar Engine
Checks whether the current calendar date matches an official Indian National Day,
International Observance, or Major Festival.
Strict Rule: If today IS a special day, it is included. If NOT, it returns None.
"""

from datetime import datetime

# Comprehensive Indian National Days, Cultural Observances & Major Festivals
SPECIAL_DAYS = {
    (1, 1): {
        "title": "New Year's Day & Global Family Day",
        "category": "national_day",
        "description": "Naye saal ki shuruat aur parivaarik ekta ka din",
        "focus": "Fresh aspirations, positivity, family bonding, and new beginnings across India."
    },
    (1, 12): {
        "title": "National Youth Day (Swami Vivekananda Jayanti)",
        "category": "national_day",
        "description": "Rashtriya Yuva Diwas - Swami Vivekananda ke vichaar aur yuva shakti",
        "focus": "Youth empowerment, mental strength, nation-building, and Swami Vivekananda's ideals."
    },
    (1, 15): {
        "title": "Indian Army Day (Sena Diwas)",
        "category": "defense_day",
        "description": "Bhartiya Sena ka veerta aur balidan ko naman",
        "focus": "Saluting the valor, sacrifice, and dedication of Indian Army soldiers guarding our borders."
    },
    (1, 23): {
        "title": "Parakram Diwas (Netaji Subhash Chandra Bose Jayanti)",
        "category": "national_day",
        "description": "Netaji Subhash Chandra Bose ki veerta aur azadi ka sankalp",
        "focus": "Celebrating the fearless courage and patriotism of Netaji Subhash Chandra Bose."
    },
    (1, 24): {
        "title": "National Girl Child Day",
        "category": "observance",
        "description": "Desh ki betiyon ki shiksha, samman aur suraksha ka din",
        "focus": "Empowering the girl child with education, equal opportunities, and rights across India."
    },
    (1, 25): {
        "title": "National Voters' Day (Rashtriya Matdata Diwas)",
        "category": "national_day",
        "description": "Loktantra ki shakti aur vote dene ke kartavya ka din",
        "focus": "Democratic awareness and the power of every single citizen's vote in shaping the nation."
    },
    (1, 26): {
        "title": "Republic Day of India (Gantantra Diwas)",
        "category": "national_festival",
        "description": "Bhartiya Samvidhan aur loktantrik garima ka sabse bada tyohar",
        "focus": "Celebrating the Indian Constitution, cultural diversity, and sovereign strength at Kartavya Path."
    },
    (1, 30): {
        "title": "Martyrs' Day (Shaheed Diwas - Mahatma Gandhi Punya Tithi)",
        "category": "national_day",
        "description": "Bapu aur desh ke amar shaheedon ko koti-koti naman",
        "focus": "Remembering Mahatma Gandhi's principles of truth, non-violence, and supreme sacrifices."
    },
    (2, 4): {
        "title": "World Cancer Day",
        "category": "health_day",
        "description": "Cancer ke khilaf jagrukta aur sahi samay par ilaj ka sankalp",
        "focus": "Global cancer awareness, prevention, healthy lifestyle, and supporting fighters."
    },
    (2, 13): {
        "title": "National Women's Day (Sarojini Naidu Jayanti)",
        "category": "national_day",
        "description": "Bharat Kokila Sarojini Naidu ka janamdin aur nari shakti",
        "focus": "Honoring women's leadership, literary grace, and nation-building contributions."
    },
    (2, 28): {
        "title": "National Science Day (Raman Effect Discovery)",
        "category": "science_day",
        "description": "Sir C.V. Raman ki khoj aur Bhartiya vigyan ka gaurav",
        "focus": "Celebrating scientific temper, innovation, and Indian scientific achievements."
    },
    (3, 8): {
        "title": "International Women's Day (Antarrashtriya Mahila Diwas)",
        "category": "observance",
        "description": "Nari shakti, aatmanirbharta aur barabari ka samman",
        "focus": "Celebrating women's achievements, resilience, independence, and gender equality."
    },
    (3, 15): {
        "title": "World Consumer Rights Day",
        "category": "observance",
        "description": "Grahak jagrukta aur consumer rights ki suraksha",
        "focus": "Jago Grahak Jago - digital safety, fair trade, and consumer empowerment."
    },
    (3, 22): {
        "title": "World Water Day (Vishwa Jal Diwas)",
        "category": "environment_day",
        "description": "Pani ki ek-ek boond ka sanrakshan aur bhavishya",
        "focus": "Water conservation, clean drinking water access, and protecting Indian water bodies."
    },
    (3, 23): {
        "title": "Shaheed Diwas (Bhagat Singh, Sukhdev & Rajguru Shahadat)",
        "category": "national_day",
        "description": "Amar Krantikari Bhagat Singh, Sukhdev aur Rajguru ka balidan",
        "focus": "Inquilab Zindabad - remembering the supreme patriotism and sacrifice of revolutionary heroes."
    },
    (4, 7): {
        "title": "World Health Day (Vishwa Swasthya Diwas)",
        "category": "health_day",
        "description": "Swasth Bharat, Swasth Vishwa - sharirik aur mansik tandurusti",
        "focus": "Prioritizing physical and mental wellness, healthcare access for every citizen."
    },
    (4, 14): {
        "title": "Dr. B.R. Ambedkar Jayanti (Samanta Diwas)",
        "category": "national_day",
        "description": "Samvidhan nirmata Babasaheb Ambedkar ka gauravshali smaran",
        "focus": "Honoring Babasaheb's visionary ideals of social equality, education, and constitutional justice."
    },
    (4, 21): {
        "title": "National Civil Services Day",
        "category": "national_day",
        "description": "Desh ke steel frame - civil servants aur prashasan ka yogdan",
        "focus": "Recognizing dedicated public servants working relentlessly for public welfare and governance."
    },
    (4, 22): {
        "title": "Earth Day (Prithvi Diwas)",
        "category": "environment_day",
        "description": "Hamari dharati maa ka sanrakshan aur green lifestyle",
        "focus": "Environmental stewardship, sustainable habits, planting trees, and reducing plastic."
    },
    (4, 24): {
        "title": "National Panchayati Raj Day",
        "category": "national_day",
        "description": "Gramin vikas aur grassroots democracy ki shakti",
        "focus": "Decentralized governance, empowering Indian villages, and rural transformation."
    },
    (5, 1): {
        "title": "International Labour Day & Maharashtra/Gujarat Day",
        "category": "national_day",
        "description": "Mehnatkash shramikon ka samman aur rajya gaurav diwas",
        "focus": "Honoring the hard work of laborers who build our roads, factories, and nation."
    },
    (5, 7): {
        "title": "Rabindranath Tagore Jayanti",
        "category": "cultural_day",
        "description": "Gurudev Rabindranath Tagore ka sahitya aur sangeet gaurav",
        "focus": "Celebrating the immortal poetry, music, and philosophy of Asia's first Nobel laureate."
    },
    (5, 11): {
        "title": "National Technology Day (Pokhran-II Anniversary)",
        "category": "science_day",
        "description": "Bhartiya technology aur paramanu shakti ka aitihasik din",
        "focus": "India's technological leap, defense self-reliance, and homegrown indigenous innovations."
    },
    (5, 21): {
        "title": "National Anti-Terrorism Day",
        "category": "national_day",
        "description": "Shanti, sadbhav aur aatankwaad ke khilaf rashtriya sankalp",
        "focus": "Uniting for national security, communal harmony, peace, and standing against terrorism."
    },
    (5, 31): {
        "title": "World No Tobacco Day",
        "category": "health_day",
        "description": "Tambaku se mukti aur swasth jeevan ka sankalp",
        "focus": "Urging youth to say no to smoking and tobacco for a healthy heart and long life."
    },
    (6, 5): {
        "title": "World Environment Day (Paryavaran Diwas)",
        "category": "environment_day",
        "description": "Paryavaran bachaane aur prakriti ke sath jeene ka sandesh",
        "focus": "Living in harmony with nature, eco-friendly choices, and protecting our green future."
    },
    (6, 21): {
        "title": "International Day of Yoga & World Music Day",
        "category": "cultural_day",
        "description": "Bhartiya yoga ka vishwa me danka aur sangeet ka jashn",
        "focus": "India's gift of Yoga to the world for physical harmony, inner peace, and wellness."
    },
    (6, 23): {
        "title": "International Olympic Day",
        "category": "sports_day",
        "description": "Sportsmanship, athletics aur Olympic jazba",
        "focus": "Inspiring young Indian athletes to run, train, and shine on the world sporting stage."
    },
    (6, 29): {
        "title": "National Statistics Day (P.C. Mahalanobis Jayanti)",
        "category": "science_day",
        "description": "Sankhyiki gaurav aur data-driven planning",
        "focus": "The power of data and statistics in national economic planning and scientific growth."
    },
    (7, 1): {
        "title": "National Doctors' Day & CA Day",
        "category": "observance",
        "description": "Bhagwan roopi doctors aur financial pillars ka aabhar",
        "focus": "Expressing deep gratitude to frontline medical doctors and chartered accountants."
    },
    (7, 11): {
        "title": "World Population Day",
        "category": "observance",
        "description": "Santan shakti aur sustainable demographic growth",
        "focus": "Balancing demographic growth with education, health resources, and green infrastructure."
    },
    (7, 26): {
        "title": "Kargil Vijay Diwas",
        "category": "defense_day",
        "description": "Kargil yuddh me veeron ki aitihasik jeet aur shahadat",
        "focus": "Operation Vijay - saluting the courageous soldiers who recaptured Himalayan peaks in 1999."
    },
    (7, 30): {
        "title": "International Friendship Day",
        "category": "observance",
        "description": "Dosti, aapsi vishwas aur sacche yaaron ke sath ka jashn",
        "focus": "Celebrating true friends, unconditional support, childhood bonds, and the beautiful spirit of friendship."
    },
    (8, 2): {
        "title": "National Friendship Day",
        "category": "observance",
        "description": "Dosti ka tyohar - har dost zaroori hota hai",
        "focus": "Celebrating lifelong friends, chai tapri yaari, and unforgettable college memories across India."
    },
    (8, 7): {
        "title": "National Handloom Day (Swadeshi Movement)",
        "category": "cultural_day",
        "description": "Bhartiya bunkaron aur hathkargha udyog ka gaurav",
        "focus": "Vocal for Local - supporting India's traditional handloom weavers and ethnic textiles."
    },
    (8, 12): {
        "title": "International Youth Day",
        "category": "observance",
        "description": "Yuva urja, creativity aur badalte Bharat ka sankalp",
        "focus": "Celebrating the boundless creativity and startup spirit of today's ambitious youth."
    },
    (8, 15): {
        "title": "Independence Day of India (Swatantrata Diwas)",
        "category": "national_festival",
        "description": "Azadi ka sabse bada tyohar - Tirange ko salaam",
        "focus": "Remembering freedom fighters, celebrating sovereignty, and building a developed Viksit Bharat."
    },
    (8, 19): {
        "title": "World Photography Day",
        "category": "creative_day",
        "description": "Palon ko kaid karne wali visual art ka jashn",
        "focus": "Celebrating the visual storytellers capturing beauty, emotion, and life through camera lenses."
    },
    (8, 20): {
        "title": "Sadbhavana Diwas (Harmony Day)",
        "category": "national_day",
        "description": "Bhaichara, sahanubhuti aur aapsi prem ka sandesh",
        "focus": "Promoting national integration, communal goodwill, and mutual harmony among all Indians."
    },
    (8, 29): {
        "title": "National Sports Day (Major Dhyan Chand Jayanti)",
        "category": "sports_day",
        "description": "Hockey jadugar Major Dhyan Chand aur khel mahotsav",
        "focus": "Celebrating sporting spirit, fitness culture, and grassroots athletic champions of India."
    },
    (9, 5): {
        "title": "Teachers' Day (Shikshak Diwas - Dr. Radhakrishnan Jayanti)",
        "category": "national_day",
        "description": "Gurus aur shikshakon ke margdarshan ko naman",
        "focus": "Honoring our teachers, mentors, and educators who sculpt minds and build the nation's future."
    },
    (9, 8): {
        "title": "International Literacy Day (Saksharta Diwas)",
        "category": "observance",
        "description": "Padhega Bharat to badhega Bharat - saksharta sankalp",
        "focus": "Ensuring every child and adult in India has the gift of reading, writing, and digital literacy."
    },
    (9, 14): {
        "title": "Hindi Diwas (Rashtrabhasha Gaurav)",
        "category": "cultural_day",
        "description": "Hindi bhasha aur sahitya ki samriddhi ka utsav",
        "focus": "Celebrating the warmth, literature, and cultural resonance of the Hindi language."
    },
    (9, 15): {
        "title": "Engineers' Day (Sir M. Visvesvaraya Jayanti)",
        "category": "science_day",
        "description": "Desh nirman karne wale engineers ka aitihasik din",
        "focus": "Saluting the brilliance of Indian engineers designing dams, bridges, space rockets, and code."
    },
    (9, 16): {
        "title": "World Ozone Day",
        "category": "environment_day",
        "description": "Ozone parat ka sanrakshan aur global climate action",
        "focus": "Protecting the protective atmospheric shield for future generations."
    },
    (9, 27): {
        "title": "World Tourism Day (Paryatan Diwas)",
        "category": "cultural_day",
        "description": "Incredible India - Bharat ke dharohar aur paryatan sthal",
        "focus": "Exploring the majestic forts, pristine beaches, and spiritual ghats of Incredible India."
    },
    (10, 2): {
        "title": "Gandhi Jayanti & Lal Bahadur Shastri Jayanti",
        "category": "national_festival",
        "description": "Satya, Ahimsa aur Jai Jawan Jai Kisan ka amar sandesh",
        "focus": "Living the timeless principles of truth, simplicity, non-violence, and farmers-soldier empowerment."
    },
    (10, 8): {
        "title": "Indian Air Force Day (Vayu Sena Diwas)",
        "category": "defense_day",
        "description": "Nabhah Sprsham Deeptam - Vayu Sena ke veeron ko salaam",
        "focus": "Touching the sky with glory - honoring the fearless pilots guarding Indian airspaces."
    },
    (10, 11): {
        "title": "International Day of the Girl Child",
        "category": "observance",
        "description": "Betiyon ke sapne aur unki asimit udan ka din",
        "focus": "Amplifying girls' voices, leadership, education, and breaking all gender stereotypes."
    },
    (10, 15): {
        "title": "World Students' Day (Dr. A.P.J. Abdul Kalam Jayanti)",
        "category": "national_day",
        "description": "Missile Man Kalam Sahab ki smriti me Vidyarthi Diwas",
        "focus": "Dream big, think scientific, and work relentlessly - following Kalam Sir's message to youth."
    },
    (10, 21): {
        "title": "Police Commemoration Day (Police Smriti Diwas)",
        "category": "observance",
        "description": "Duty nibhate hue shaheed hue police jawano ko shradhanjali",
        "focus": "Remembering brave police and paramilitary personnel who sacrificed lives for citizen safety."
    },
    (10, 24): {
        "title": "United Nations Day",
        "category": "observance",
        "description": "Vishwa shanti, sahyog aur Vasudhaiva Kutumbakam",
        "focus": "Global peace, multilateral cooperation, and India's leadership in international harmony."
    },
    (10, 31): {
        "title": "Rashtriya Ekta Diwas (National Unity Day - Sardar Patel Jayanti)",
        "category": "national_day",
        "description": "Lauh Purush Sardar Vallabhbhai Patel aur Akhand Bharat",
        "focus": "Honoring the Iron Man who united 560+ princely states into one strong Indian republic."
    },
    (11, 1): {
        "title": "States Reorganisation Day (Karnataka Rajyotsava, Kerala Piravi, MP, Haryana)",
        "category": "cultural_day",
        "description": "Bhartiya rajyon ka gauravshali sthapna diwas",
        "focus": "Celebrating the distinct languages, festivals, and cultural richness of our vibrant states."
    },
    (11, 7): {
        "title": "National Cancer Awareness Day",
        "category": "health_day",
        "description": "Early detection aur cancer se bachaav ki jankari",
        "focus": "Promoting regular health checkups and healthy nutrition to prevent chronic diseases."
    },
    (11, 11): {
        "title": "National Education Day (Maulana Abul Kalam Azad Jayanti)",
        "category": "national_day",
        "description": "Bharat ke pehle Shiksha Mantri aur shiksha ka mahatva",
        "focus": "Education as the fundamental engine of human dignity, social growth, and national prosperity."
    },
    (11, 14): {
        "title": "Children's Day (Bal Diwas - Pandit Nehru Jayanti)",
        "category": "national_day",
        "description": "Chacha Nehru ka janamdin aur bachpan ki masoomiyat ka utsav",
        "focus": "Nurturing children with care, love, curiosity, and quality schooling for India's tomorrow."
    },
    (11, 19): {
        "title": "National Integration Day (Rashtriya Ekta Diwas - Indira Gandhi)",
        "category": "national_day",
        "description": "Rashtriya akhandata aur vividhta me ekta ka sankalp",
        "focus": "Cherishing unity in diversity, communal amity, and standing together as one India."
    },
    (11, 26): {
        "title": "Constitution Day of India (Samvidhan Diwas)",
        "category": "national_day",
        "description": "Hamara Samvidhan - hamari azaadi, adhikaar aur kartavya ki neev",
        "focus": "Honoring the Preamble, fundamental rights, and our sacred duties as Indian citizens."
    },
    (12, 1): {
        "title": "World AIDS Day",
        "category": "health_day",
        "description": "HIV/AIDS jagrukta aur empathy ka prateek",
        "focus": "Compassion, awareness, ending social stigma, and supporting healthcare access."
    },
    (12, 4): {
        "title": "Indian Navy Day (Nau Sena Diwas)",
        "category": "defense_day",
        "description": "Samudra ke pehredaron - Nau Sena ke veeron ko naman",
        "focus": "Operation Trident - celebrating the blue-water prowess, rescue missions, and maritime vigilance."
    },
    (12, 7): {
        "title": "Armed Forces Flag Day",
        "category": "defense_day",
        "description": "Sena ke jawano aur unke parivaron ke samman ka din",
        "focus": "Honoring martyr families, disabled soldiers, and wearing the patriotic flag with pride."
    },
    (12, 10): {
        "title": "Human Rights Day (Manav Adhikar Diwas)",
        "category": "observance",
        "description": "Har insaan ki garima, aazadi aur adhikar ka samman",
        "focus": "Protecting fundamental human dignity, equality, and justice across all societies."
    },
    (12, 16): {
        "title": "Vijay Diwas (1971 War Historic Victory)",
        "category": "defense_day",
        "description": "1971 yuddh me Bhartiya Sena ki aitihasik shaurya gatha",
        "focus": "Saluting the brave soldiers whose heroic courage liberated Bangladesh in 1971."
    },
    (12, 18): {
        "title": "Minorities Rights Day in India",
        "category": "national_day",
        "description": "Samvidhanik suraksha aur sabhi samudayon ka aadar",
        "focus": "Upholding communal harmony, cultural protection, and equal opportunities for all communities."
    },
    (12, 22): {
        "title": "National Mathematics Day (Srinivasa Ramanujan Jayanti)",
        "category": "science_day",
        "description": "Ganit ke jadugar Srinivasa Ramanujan ka gaurav",
        "focus": "Inspiring young minds with mathematical beauty, logic, and analytical problem-solving."
    },
    (12, 23): {
        "title": "Kisan Diwas (National Farmers' Day - Chaudhary Charan Singh)",
        "category": "national_day",
        "description": "Annadata kisan bhaiyon aur behnon ke parishram ko naman",
        "focus": "Saluting our farmers who work tirelessly in sun and rain to feed 1.4 billion Indians."
    },
    (12, 24): {
        "title": "National Consumer Rights Day",
        "category": "observance",
        "description": "Consumer Protection Act aur grahak jagrukta",
        "focus": "Educating consumers against misleading advertisements, digital fraud, and unfair practices."
    },
    (12, 25): {
        "title": "Good Governance Day (Atal Bihari Vajpayee Jayanti) & Christmas",
        "category": "national_day",
        "description": "Susashan, transparent technology aur Christmas ki shubhkaamnayein",
        "focus": "Celebrating citizen-first transparent governance alongside the joyful spirit of Christmas."
    }
}


def get_special_day_for_date(target_dt=None):
    """
    Returns the Special Day dictionary for the given or current date.
    Strict Rule: If today IS a special day, returns dict.
    If today is NOT a special day, returns None.
    """
    if not target_dt:
        target_dt = datetime.now()
    key = (target_dt.month, target_dt.day)
    return SPECIAL_DAYS.get(key, None)


if __name__ == "__main__":
    now = datetime.now()
    res = get_special_day_for_date(now)
    print(f"Checking special day for {now.strftime('%d-%b-%Y')}: {res}")
