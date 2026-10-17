"""
Md Sadique Amin Local Wi-Fi Media Server
Serves all generated reels, audio, images, and Excel reports over local Wi-Fi.
Open http://192.168.1.7:8080 or http://localhost:8080 on any device connected to the same Wi-Fi!
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080

class Md Sadique AminMediaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def start_server():
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, Md Sadique AminMediaHandler)
    print("=" * 70)
    print(f"📡 MD_SADIQUE_AMIN LOCAL WI-FI MEDIA & GALLERY SERVER")
    print("=" * 70)
    print(f"  🟢 Local Access (Laptop): http://localhost:{PORT}")
    print(f"  🟢 Mobile Access (Phone) : http://192.168.1.7:{PORT}")
    print(f"  📁 Root Directory        : {os.getcwd()}")
    print("=" * 70)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")

if __name__ == "__main__":
    start_server()
