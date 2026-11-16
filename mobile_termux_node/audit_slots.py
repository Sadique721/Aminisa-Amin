# -*- coding: utf-8 -*-
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from topic_engine import get_all_daily_slots

def run_audit():
    print("=" * 75)
    print("        AUDIT OF ALL 10 AMINSA SLOTS: SCRIPT & VIDEO PROMPT")
    print("=" * 75)
    slots = get_all_daily_slots()
    
    tech_count = 0
    hinglish_count = 0
    
    for s in slots:
        num = s["slot"]
        time_str = s["time"]
        cat = s["category"]
        lang = s["language"].upper()
        script = s["script"]
        vid = s["video_prompt"]
        
        is_tech = (s["category_key"] in ["tech_ai", "future_tech"])
        
        if is_tech:
            tech_count += 1
            expected_lang = "ENGLISH"
            greeting_expected = "Hello everyone! I'm Aminsa. Today's top tech breakthrough:"
        else:
            hinglish_count += 1
            expected_lang = "HINGLISH"
            greeting_expected = "Hello everyone! Main hoon Aminsa. Aaj ki sabse badi khabar:"
            
        lang_match = (lang == expected_lang)
        greeting_match = script.startswith(greeting_expected) or ("Aaj desh mana raha hai" in script)
        
        status_icon = "✅" if (lang_match and greeting_match) else "❌"
        
        print(f"\n{status_icon} SLOT #{num} [{time_str}] - {cat}")
        print(f"   Domain Category Key : {s['category_key']}")
        print(f"   Designated Language : {lang} (Expected: {expected_lang})")
        print(f"   Spoken Voice Script : \"{script[:85]}...\"")
        print(f"   Video Motion Prompt : \"{vid[:85]}...\"")
        print(f"   Video Prompt Length : {len(vid)} chars (YouTube Create <300: {'PASS' if len(vid) < 300 else 'FAIL'})")
        
    print("\n" + "=" * 75)
    print(f"TOTAL AUDIT SUMMARY:")
    print(f"  • Tech Slots (English Script & Voice)   : {tech_count} / 2 (Slots #2, #8)")
    print(f"  • Indian/Other Slots (Hinglish Voice)    : {hinglish_count} / 8 (Slots #1, #3, #4, #5, #6, #7, #9, #10)")
    print(f"  • Total Slots Analyzed                   : {len(slots)} / 10")
    print("=" * 75)

if __name__ == "__main__":
    run_audit()
