# -*- coding: utf-8 -*-
"""
Aminsa Persistent Mobile Web Daemon (Port 8765)
Serves the Interactive Production Dashboard & Excel Grid with Zero 404s.
Runs continuously inside Termux.
"""

import os
import sys
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8765
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIRS = [
    SCRIPT_DIR,
    "/data/data/com.termux/files/home",
    "/data/data/com.termux/files/home/aminsa_mobile_ecosystem",
    "/data/data/com.termux",
    os.path.expanduser("~")
]


def resolve_file(filename):
    for d in SEARCH_DIRS:
        cand = os.path.join(d, filename)
        if os.path.exists(cand) and os.path.getsize(cand) > 0:
            return cand
    return None


class AminsaWebHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silent logging to avoid console spam
        pass

    def do_GET(self):
        # 1. Excel Download Endpoint
        if self.path in ["/excel", "/download/excel", "/Aminsa_Master_Production_Catalog.xlsx"]:
            x_file = resolve_file("Aminsa_Master_Production_Catalog.xlsx")
            if x_file and os.path.exists(x_file):
                try:
                    with open(x_file, "rb") as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    self.send_header("Content-Disposition", 'attachment; filename="Aminsa_Master_Production_Catalog.xlsx"')
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
                except Exception:
                    pass

        # 2. Universal HTML Dashboard Endpoint
        h_file = resolve_file("Aminsa_Master_Production_Catalog.html")
        html_data = None
        if h_file and os.path.exists(h_file):
            try:
                with open(h_file, "rb") as f:
                    html_data = f.read()
            except Exception:
                pass

        if html_data:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_data)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(html_data)
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
    server_address = ("127.0.0.1", PORT)
    try:
        httpd = HTTPServer(server_address, AminsaWebHandler)
        print(f"[✓] Aminsa Web Daemon listening on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
    except Exception as e:
        print(f"[-] Server error: {e}")


if __name__ == "__main__":
    run_server()
