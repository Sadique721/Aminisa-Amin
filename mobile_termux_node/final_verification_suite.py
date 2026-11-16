# -*- coding: utf-8 -*-
"""
Aminsa Comprehensive Deep Verification Suite
============================================
Runs all 7 test batteries directly on the mobile ecosystem:
1. File Integrity & Deployment
2. Live Multi-Tier RSS Harvester (Zero Fallback)
3. 10-Slot Language, Persona & Greeting Syntax
4. YouTube Create Video Prompt Bounds (<300 chars, No Image Prompts)
5. Special Days Calendar Triggers & Fallback to Live News
6. Live HTTP Web Daemon (Port 8765) & Restored Grid Layout Inspection
7. Excel Spreadsheet Structural Integrity
"""

import os
import sys
import urllib.request
import re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import CATEGORIES, PERSONA_NAME, GREETING, WEB_PORT
from topic_engine import get_all_daily_slots, generate_single_slot
from special_days import get_special_day_for_date
from dynamic_news_pipeline import fetch_live_headline

results = []

def record_test(suite_name: str, test_name: str, passed: bool, details: str):
    results.append({
        "suite": suite_name,
        "test": test_name,
        "passed": passed,
        "details": details
    })
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"[{status}] [{suite_name}] {test_name}: {details}")

print("\n" + "=" * 80)
print("        🧪 AMINSA COMPLETE DEEP VERIFICATION SUITE STARTING")
print("=" * 80 + "\n")

# ----------------------------------------------------
# 1. FILE INTEGRITY & DEPLOYMENT
# ----------------------------------------------------
suite = "1. File Integrity"
expected_files = [
    "config.py",
    "topic_engine.py",
    "dynamic_news_pipeline.py",
    "special_days.py",
    "aminsa_catalog_engine.py",
    "aminsa_mobile_runner.py",
    "aminsa_web_daemon.py",
    "build_chatgpt_style_html.py"
]
for ef in expected_files:
    p = os.path.join(SCRIPT_DIR, ef)
    exists = os.path.exists(p) and os.path.getsize(p) > 0
    record_test(suite, f"File {ef}", exists, f"Size: {os.path.getsize(p)} bytes" if exists else "Missing/Empty")

# ----------------------------------------------------
# 2. LIVE MULTI-TIER RSS HARVESTER (ZERO STATIC FALLBACK)
# ----------------------------------------------------
suite = "2. Live News Pipeline"
sample_hl = fetch_live_headline("cricket_sports", "india cricket match bcci team india sports")
has_headline = bool(sample_hl and len(sample_hl) > 10)
not_static = ("AI breakthroughs in India transforming modern everyday productivity" not in sample_hl)
record_test(suite, "Live Headline Harvested", has_headline, f"Headline: '{sample_hl[:60]}...'")
record_test(suite, "Zero Static Fallback", not_static, "No hardcoded default text detected")

# ----------------------------------------------------
# 3. 10-SLOT LANGUAGE & GREETING VALIDATION
# ----------------------------------------------------
suite = "3. Language & Greeting"
slots = get_all_daily_slots()
tech_slots = [2, 8]
hinglish_slots = [1, 3, 4, 5, 6, 7, 9, 10]

for s in slots:
    s_num = s["slot"]
    script = s["script"]
    lang = s["language"]
    
    # Check zero Namaste
    no_namaste = ("namaste" not in script.lower())
    record_test(suite, f"Slot #{s_num} Zero Namaste", no_namaste, "Protocol strictly followed")

    if s_num in tech_slots:
        is_eng = (lang == "english" and "Hello everyone! I'm Aminsa. Today's top tech breakthrough:" in script)
        record_test(suite, f"Slot #{s_num} Tech English Script", is_eng, f"Language: {lang.upper()}")
    else:
        is_hinglish = (lang == "hinglish" and "Hello everyone! Main hoon Aminsa. Aaj ki sabse badi khabar:" in script)
        record_test(suite, f"Slot #{s_num} Indian/Other Hinglish Script", is_hinglish, f"Language: {lang.upper()}")

# ----------------------------------------------------
# 4. YOUTUBE CREATE VIDEO PROMPT BOUNDS (<300 CHARS)
# ----------------------------------------------------
suite = "4. Video Prompt Bounds"
for s in slots:
    s_num = s["slot"]
    vp = s.get("video_prompt", "")
    vp_len = len(vp)
    is_bounded = (vp_len > 150 and vp_len < 300)
    no_biometric = ("unblemished porcelain texture" not in vp and "warm glowing fair wheatish" not in vp)
    no_img_prompt = ("img_prompt" not in s)
    record_test(suite, f"Slot #{s_num} Length < 300 Chars", is_bounded, f"Length: {vp_len} chars (Budget <300)")
    record_test(suite, f"Slot #{s_num} Biometric Free", no_biometric, "Pure motion & context prompt")
    record_test(suite, f"Slot #{s_num} Image Prompt Deprecated", no_img_prompt, "Video Prompt only")

# ----------------------------------------------------
# 5. SPECIAL DAYS CALENDAR TRIGGERS
# ----------------------------------------------------
suite = "5. Special Days Calendar"
# Test A: Date with special day (Independence Day: August 15)
s_ind = generate_single_slot(0, target_dt=datetime(2026, 8, 15))
is_ind_day = ("Swatantrata Diwas" in s_ind["script"] or "Independence Day" in s_ind["script"])
record_test(suite, "Independence Day Trigger (Aug 15)", is_ind_day, f"Generated: {s_ind['title']}")

# Test B: Date with Friendship Day (August 2)
s_friend = generate_single_slot(0, target_dt=datetime(2026, 8, 2))
is_friend_day = ("Friendship Day" in s_friend["script"])
record_test(suite, "Friendship Day Trigger (Aug 2)", is_friend_day, f"Generated: {s_friend['title']}")

# Test C: Date without special day (e.g., Nov 16 normal day) -> Fallback to live breaking news
s_norm = generate_single_slot(0, target_dt=datetime(2026, 11, 16))
is_live_news = bool(s_norm["headline"] and "Aaj desh mana raha hai" not in s_norm["script"])
record_test(suite, "Normal Date Falls Back to Live News", is_live_news, f"Headline: {s_norm['headline'][:50]}...")

# ----------------------------------------------------
# 6. WEB DAEMON (PORT 8765) & RESTORED GRID AUDIT
# ----------------------------------------------------
suite = "6. Web Daemon & Grid Layout"
try:
    req = urllib.request.Request(f"http://127.0.0.1:{WEB_PORT}/")
    with urllib.request.urlopen(req, timeout=5) as resp:
        html_content = resp.read().decode("utf-8")
        status_code = resp.status
except Exception as e:
    html_content = ""
    status_code = 0

daemon_alive = (status_code == 200 and len(html_content) > 1000)
record_test(suite, "Web Daemon 200 OK", daemon_alive, f"HTTP Status: {status_code}, Length: {len(html_content)} bytes")

# Verify Restored Original Grid Elements
grid_checks = [
    (".chatgpt-nav", "ChatGPT Header Bar"),
    (".gpt-pill", "Aminsa 4o Header Pill"),
    (".tab-switcher", "Segmented Tabs Switcher"),
    ("id=\"btn-tab-table\"", "Live Excel Grid Tab Button"),
    ("id=\"tab-table\"", "Excel Grid Tab Container"),
    (".table-responsive", "Responsive Table Container"),
    (".cat-cell", "Category Cell Styling"),
    (".title-cell", "Title Cell Styling"),
    (".text-cell", "Spoken Script Cell"),
    (".code-cell", "Video Prompt Code Cell"),
    (".table-copy-btn", "1-Tap Table Copy Button"),
    (".bottom-action-bar", "Floating Bottom Action Bar"),
    ("copyAll10Slots", "Copy All 10 Slots Action")
]

for cls_name, desc in grid_checks:
    present = (cls_name in html_content)
    record_test(suite, f"Restored Element: {desc}", present, f"Pattern '{cls_name}' found in HTML")

# ----------------------------------------------------
# 7. EXCEL SPREADSHEET STRUCTURAL INTEGRITY
# ----------------------------------------------------
suite = "7. Excel Master Workbook"
x_file = os.path.join(SCRIPT_DIR, "Aminsa_Master_Production_Catalog.xlsx")
excel_exists = os.path.exists(x_file) and os.path.getsize(x_file) > 2000
record_test(suite, "Excel Catalog Exists", excel_exists, f"File: {x_file} (Size: {os.path.getsize(x_file) if excel_exists else 0} bytes)")

try:
    import openpyxl
    wb = openpyxl.load_workbook(x_file)
    ws1 = wb["Mobile_Video_Shorts"]
    headers = [ws1.cell(row=2, column=c).value for c in range(1, 11)]
    has_video_col = any("Video Motion Prompt" in str(h) for h in headers)
    no_image_col = not any("Image Prompt" in str(h) for h in headers)
    row_count = ws1.max_row
    record_test(suite, "Excel Has Video Prompt Column", has_video_col, "Video Motion Prompt Column present")
    record_test(suite, "Excel Deprecated Image Prompt Column", no_image_col, "Image Prompt column absent")
    record_test(suite, "Excel 10 Slots Populated", (row_count >= 12), f"Total Rows: {row_count}")
except Exception as e:
    record_test(suite, "Excel Openpyxl Verification", False, str(e))

# ----------------------------------------------------
# FINAL SCORE SUMMARY
# ----------------------------------------------------
print("\n" + "=" * 80)
total_tests = len(results)
passed_tests = sum(1 for r in results if r["passed"])
failed_tests = total_tests - passed_tests

print(f"📊 FINAL VERIFICATION SCORE: {passed_tests} / {total_tests} TESTS PASSED ({passed_tests/total_tests*100:.1f}%)")
if failed_tests == 0:
    print("🏆 ALL TESTS PASSED! ECOSYSTEM IS 100% OPERATIONAL, BOUNDED & RESTORED.")
else:
    print(f"⚠️ {failed_tests} TESTS FAILED. PLEASE CHECK DETAILS ABOVE.")
print("=" * 80 + "\n")
