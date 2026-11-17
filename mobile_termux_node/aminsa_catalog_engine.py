# -*- coding: utf-8 -*-
"""
Aminsa Master Dynamic Production Catalog Engine
================================================
Replaces old static matrix with 100% Real-Time Dynamic Live Feeds.
Strict Requirement: Video Prompts ONLY (Zero Image Prompts).
Generates Master Production Excel and feeds ChatGPT-style HTML Dashboard.
"""

import os
import sys
from datetime import datetime

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

from topic_engine import get_all_daily_slots


def get_current_day_data(target_date=None):
    """Returns (date_str, slots, None) powered entirely by the live dynamic topic engine."""
    if not target_date:
        target_date = datetime.now()
    date_str = target_date.strftime("%A, %d %B %Y")
    slots = get_all_daily_slots(target_date)
    return date_str, slots, None


def generate_master_excel(output_path: str, target_date=None) -> str:
    """Generates the professional production workbook with Video Prompts ONLY."""
    if not target_date:
        target_date = datetime.now()

    date_str, slots, _ = get_current_day_data(target_date)

    if not OPENPYXL_AVAILABLE:
        print("[-] openpyxl not installed, skipping excel generation.")
        return output_path

    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Mobile_Video_Shorts"

    # Styling Palette
    header_fill = PatternFill(start_color="10A37F", end_color="10A37F", fill_type="solid") # ChatGPT Green
    sub_fill = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid")
    alt_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    white_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=10, bold=True)
    normal_font = Font(name="Calibri", size=10)
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_wrap = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # Title Banner
    ws1.merge_cells("A1:K1")
    t_cell = ws1["A1"]
    t_cell.value = f"AMINSA 24/7 DYNAMIC VIDEO PRODUCTION CATALOG — {date_str.upper()}"
    t_cell.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    t_cell.fill = sub_fill
    t_cell.alignment = center_align
    ws1.row_dimensions[1].height = 36

    headers = [
        "Slot #",
        "Scheduled Time",
        "Domain Category",
        "Language",
        "Live Headline / Focus",
        "Spoken Script (Dialogue)",
        "Video Motion Prompt (YouTube Create / AI)",
        "YouTube Shorts Title (<100 Chars)",
        "Social Media Caption & Tags",
        "Wardrobe & Attire",
        "Setting / Location"
    ]

    for col_idx, h in enumerate(headers, 1):
        cell = ws1.cell(row=2, column=col_idx, value=h)
        cell.font = white_bold
        cell.fill = header_fill
        cell.alignment = center_align
    ws1.row_dimensions[2].height = 28

    # Populate Rows
    for row_idx, s in enumerate(slots, 3):
        row_values = [
            f"Slot #{s['slot']}",
            s["time"],
            s["category"],
            s.get("language", "Hinglish").upper(),
            s["title"],
            s["script"],
            s["video_prompt"],
            s.get("yt_shorts_posting", s["title"] + " #Aminsa #Shorts"),
            s["caption"],
            s.get("wardrobe", "Modern tailored chic"),
            s.get("location", "Studio")
        ]
        is_even = (row_idx % 2 == 0)
        for col_idx, val in enumerate(row_values, 1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.font = normal_font
            if col_idx in [1, 2, 4]:
                cell.alignment = center_align
            else:
                cell.alignment = left_wrap
            if is_even:
                cell.fill = alt_fill
        ws1.row_dimensions[row_idx].height = 80

    # Auto Column Widths
    col_widths = {1: 10, 2: 15, 3: 25, 4: 12, 5: 35, 6: 45, 7: 45, 8: 40, 9: 35, 10: 25, 11: 25}
    for col_idx, w in col_widths.items():
        ws1.column_dimensions[get_column_letter(col_idx)].width = w

    # Sheet 2: System Directives
    ws2 = wb.create_sheet(title="System_Rules")
    ws2.append(["Parameter", "Value", "Operational Rule"])
    for cell in ws2[1]:
        cell.font = white_bold
        cell.fill = sub_fill
        cell.alignment = center_align

    rules = [
        ("Persona Name", "Aminsa", "22-year-old AI creator locked across all platforms"),
        ("Face Geometry", "Warm wheatish porcelain (#EAD5C3)", "Strictly ZERO moles, ZERO blemishes, ZERO marks"),
        ("Eye Geometry", "Hazel-brown almond (#6B4423)", "Deep limbal rings, lively engaging expression"),
        ("Voice Synthesis", "hi-IN-SwaraNeural (224 Hz)", "Warm articulate natural delivery"),
        ("Greeting Protocol", "STRICTLY 'Hello everyone!'", "Strictly ZERO 'Namaste' across all scripts"),
        ("Tech Category Language", "Strictly English", "Slots 2 and 8 spoken completely in clear English"),
        ("India & Other Topics", "Conversational Hinglish", "Engaging and relatable Hinglish dialogue"),
        ("Special Days Integration", "Date-Triggered", "Observances included only if matching current calendar date"),
        ("Content Freshness", "100% Real-Time Live RSS", "Cascading multi-tier pipeline with zero hardcoded fallbacks"),
        ("Output Media Type", "Video Prompts ONLY", "Image prompts completely deprecated from all workflows")
    ]
    for r in rules:
        ws2.append(list(r))
    for col_idx in range(1, 4):
        ws2.column_dimensions[get_column_letter(col_idx)].width = 30

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    print(f"[✓] Dynamic Master Production Catalog saved: {output_path}")
    return output_path


# For backward compatibility with scripts importing MOBILE_SLOTS
MOBILE_SLOTS = get_all_daily_slots()


if __name__ == "__main__":
    test_out = os.path.join(os.path.dirname(__file__), "test_catalog.xlsx")
    generate_master_excel(test_out)
