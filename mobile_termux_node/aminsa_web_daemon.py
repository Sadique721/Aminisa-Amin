# -*- coding: utf-8 -*-
"""
Aminsa Dynamic Real-Time Mobile Web Daemon (Port 8765)
======================================================
100% Dynamic Just-In-Time (JIT) Production Dashboard & Live Excel Engine.
Strict Rules:
1. Auto-Invalidation: Re-harvests on date rollover (midnight) and 2.4h slot transition.
2. Zero Stale Files: Guarantees user ALWAYS sees fresh live data upon visiting.
3. 1-Tap Force Refresh: '/refresh' endpoint pulls immediate live breaking news.
4. Dynamic Excel Generator: Delivers up-to-the-minute real-time Excel workbooks.
"""

import os
import sys
import time
import socket
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from aminsa_catalog_engine import generate_master_excel, get_current_day_data
from build_chatgpt_style_html import build_chatgpt_html

PORT = 8765

SEARCH_DIRS = [
    SCRIPT_DIR,
    "/data/data/com.termux/files/home/aminsa_mobile_ecosystem",
    "/data/data/com.termux/files/home",
    "/sdcard/DCIM/Aminsa/mobile_termux_node",
    "/sdcard/DCIM/Aminsa",
    "/sdcard/Download",
    os.path.expanduser("~")
]

# Global in-memory cache
_CACHED_HTML = None
_CACHED_EXCEL_BYTES = None
_CACHED_DATE = None
_CACHED_SLOT_INDEX = None
_LAST_HARVEST_TIME = 0


def get_current_slot_index():
    now = datetime.now()
    minutes_since_midnight = now.hour * 60 + now.minute
    total_slot_minutes = 24 * 60 / 10  # 144 mins = 2.4 hours
    return int(minutes_since_midnight // total_slot_minutes) % 10


def ensure_fresh_catalog(force_refresh=False):
    global _CACHED_HTML, _CACHED_EXCEL_BYTES, _CACHED_DATE, _CACHED_SLOT_INDEX, _LAST_HARVEST_TIME
    
    now = datetime.now()
    date_key = now.strftime("%Y-%m-%d")
    curr_slot = get_current_slot_index()
    elapsed = time.time() - _LAST_HARVEST_TIME

    needs_refresh = (
        force_refresh or
        _CACHED_HTML is None or
        _CACHED_DATE != date_key or
        _CACHED_SLOT_INDEX != curr_slot or
        elapsed > 3600  # Stale after 1 hour
    )

    if not needs_refresh:
        return _CACHED_HTML

    print(f"[*] [Aminsa Web] Re-harvesting live data (Date: {date_key}, Slot: #{curr_slot + 1}, Force: {force_refresh})...")
    try:
        date_str, slots, dna = get_current_day_data(now)
        html_str = build_chatgpt_html(date_str, slots, dna)
        _CACHED_HTML = html_str.encode("utf-8")
        _CACHED_DATE = date_key
        _CACHED_SLOT_INDEX = curr_slot
        _LAST_HARVEST_TIME = time.time()

        # Update disk copies across all target directories
        primary_excel = os.path.join(SCRIPT_DIR, "Aminsa_Master_Production_Catalog.xlsx")
        primary_html = os.path.join(SCRIPT_DIR, "Aminsa_Master_Production_Catalog.html")

        generate_master_excel(primary_excel, now)
        with open(primary_html, "wb") as f:
            f.write(_CACHED_HTML)

        # Cache excel bytes
        if os.path.exists(primary_excel):
            with open(primary_excel, "rb") as f:
                _CACHED_EXCEL_BYTES = f.read()

        # Mirror updated files safely
        for d in SEARCH_DIRS:
            if os.path.exists(d) and d != SCRIPT_DIR:
                try:
                    dst_x = os.path.join(d, "Aminsa_Master_Production_Catalog.xlsx")
                    dst_h = os.path.join(d, "Aminsa_Master_Production_Catalog.html")
                    if _CACHED_EXCEL_BYTES:
                        with open(dst_x, "wb") as f:
                            f.write(_CACHED_EXCEL_BYTES)
                    with open(dst_h, "wb") as f:
                        f.write(_CACHED_HTML)
                except Exception:
                    pass

        print(f"[✓] [Aminsa Web] Live production catalog successfully regenerated & cached!")
    except Exception as e:
        print(f"[-] [Aminsa Web] Error regenerating catalog: {e}")

    return _CACHED_HTML


class AminsaWebHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silent logging to prevent console flood
        pass

    def do_GET(self):
        # 1. 1-Tap Manual Force Refresh Endpoint
        if self.path in ["/refresh", "/api/refresh"]:
            ensure_fresh_catalog(force_refresh=True)
            self.send_response(302)
            self.send_header("Location", "/")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            return

        # 2. Dynamic Excel Download Endpoint
        if self.path in ["/excel", "/download/excel", "/Aminsa_Master_Production_Catalog.xlsx"]:
            ensure_fresh_catalog()
            global _CACHED_EXCEL_BYTES
            if not _CACHED_EXCEL_BYTES:
                primary_excel = os.path.join(SCRIPT_DIR, "Aminsa_Master_Production_Catalog.xlsx")
                if os.path.exists(primary_excel):
                    with open(primary_excel, "rb") as f:
                        _CACHED_EXCEL_BYTES = f.read()

            if _CACHED_EXCEL_BYTES:
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                self.send_header("Content-Disposition", 'attachment; filename="Aminsa_Master_Production_Catalog.xlsx"')
                self.send_header("Content-Length", str(len(_CACHED_EXCEL_BYTES)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(_CACHED_EXCEL_BYTES)
                return

        # 3. Dynamic Real-Time HTML Dashboard Endpoint
        html_bytes = ensure_fresh_catalog()
        if html_bytes:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(html_bytes)
        else:
            msg = b"<h1>Aminsa Dashboard Generating... Please refresh in 3 seconds.</h1>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)


def is_running():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, AminsaWebHandler)
    print("=" * 65)
    print("🌟 AMINSA DYNAMIC REAL-TIME MOBILE WEB DAEMON ACTIVE")
    print(f"[*] Port: {PORT} (http://127.0.0.1:{PORT}/)")
    print(f"[*] Auto-Invalidation: Date Rollover + 2.4h Slot Transitions")
    print(f"[*] Manual Refresh Endpoint: http://127.0.0.1:{PORT}/refresh")
    print("=" * 65)
    
    # Pre-warm catalog on startup
    ensure_fresh_catalog()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Web Daemon stopped.")


if __name__ == "__main__":
    run_server()
