"""
Md Sadique Amin 24-Hour Continuous Telemetry & Audit Logger
Maintains a structured Excel audit spreadsheet at reports/daily_performance.xlsx.
"""

import os
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EXCEL_FILE = os.path.join("reports", "daily_performance.xlsx")

HEADERS = [
    "Cycle ID",
    "Timestamp (IST)",
    "Viral Topic / Content Hook",
    "Category Pillar",
    "Media Format",
    "Local Artifact Path",
    "Audio F0 Target",
    "Target Channels",
    "Execution Status",
    "Latency (Sec)"
]

def initialize_workbook():
    os.makedirs("reports", exist_ok=True)
    if os.path.exists(EXCEL_FILE):
        try:
            wb = openpyxl.load_workbook(EXCEL_FILE)
            ws = wb.active
            return wb, ws
        except Exception:
            pass

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Md Sadique Amin Daily Performance"
    
    # Header styling
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws.append(HEADERS)
    for col_num in range(1, len(HEADERS) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align
        
    wb.save(EXCEL_FILE)
    return wb, ws

def log_execution_cycle(cycle_id, topic, category, media_format, media_path, status="SUCCESS", latency=5.2):
    wb, ws = initialize_workbook()
    
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row_data = [
        cycle_id,
        now_str,
        topic,
        category,
        media_format,
        media_path,
        "224 Hz (Locked)",
        "Instagram, Facebook, Threads, YouTube",
        status,
        round(latency, 2)
    ]
    
    ws.append(row_data)
    
    # Auto-adjust column widths
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
        
    wb.save(EXCEL_FILE)
    print(f"[+] Logged cycle '{cycle_id}' to Excel: {EXCEL_FILE}")
    return EXCEL_FILE

if __name__ == "__main__":
    log_execution_cycle(
        cycle_id="CYC-INIT-001",
        topic="Initial Setup & Pipeline Verification",
        category="System Architecture",
        media_format="Reel MP4",
        media_path="md_sadique_amin_official_intro_reel.mp4",
        status="VERIFIED",
        latency=4.8
    )
