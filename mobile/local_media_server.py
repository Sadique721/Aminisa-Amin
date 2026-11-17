# -*- coding: utf-8 -*-
"""
Aminsa Amin — Mobile & Laptop Mutual Access & Media Hub
======================================================
Google Stitch Design System Compliant (theme: dark, brand: #38bdf8, surface: #111827)
Python 3.12+ / 3.14 compatible (No deprecated cgi module)
Provides full bidirectional access between Laptop and Mobile:
1. 1-Tap 4K Master Face Download directly to Phone Gallery.
2. Bidirectional File Exchange (Laptop <-> Mobile).
3. Mobile Upload to Laptop 'Received Files'.
4. Full Workspace File & Media Browser.
"""

import os
import sys
import re
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8080
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECEIVED_DIR = os.path.join(ROOT_DIR, "Received Files")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aminsa Amin — Mobile & Laptop Control Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0b0f19;
      --bg-surface: #111827;
      --bg-elevated: #1f293d;
      --brand-primary: #38bdf8;
      --brand-glow: #0284c7;
      --brand-accent: #10b981;
      --brand-warning: #f59e0b;
      --text-primary: #f9fafb;
      --text-secondary: #94a3b8;
      --text-accent: #38bdf8;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-highlight: rgba(56, 189, 248, 0.35);
      --font-heading: 'Outfit', sans-serif;
      --font-body: 'Inter', sans-serif;
      --font-code: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-primary);
      color: var(--text-primary);
      font-family: var(--font-body);
      padding: 16px;
      line-height: 1.5;
    }
    .container { max-width: 800px; margin: 0 auto; }
    header {
      background: var(--bg-surface);
      border: 1px solid var(--border-highlight);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 20px;
      text-align: center;
      box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
    }
    header h1 {
      font-family: var(--font-heading);
      font-size: 24px;
      color: var(--text-primary);
      margin-bottom: 6px;
    }
    header p { color: var(--text-secondary); font-size: 14px; }
    .badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.15);
      color: var(--brand-accent);
      border: 1px solid rgba(16, 185, 129, 0.3);
      margin-top: 10px;
    }
    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
    }
    .card h2 {
      font-family: var(--font-heading);
      font-size: 18px;
      color: var(--brand-primary);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .preview-box {
      text-align: center;
      margin-bottom: 16px;
    }
    .preview-img {
      max-width: 100%;
      height: auto;
      max-height: 320px;
      border-radius: 8px;
      border: 1px solid var(--border-highlight);
    }
    .btn {
      display: block;
      width: 100%;
      padding: 14px;
      border-radius: 8px;
      font-family: var(--font-body);
      font-size: 15px;
      font-weight: 600;
      text-align: center;
      text-decoration: none;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
    }
    .btn-primary {
      background: var(--brand-primary);
      color: #0b0f19;
      box-shadow: 0 4px 14px rgba(56, 189, 248, 0.3);
    }
    .btn-primary:hover { background: #7dd3fc; }
    .btn-secondary {
      background: var(--bg-elevated);
      color: var(--text-primary);
      border: 1px solid var(--border-subtle);
      margin-top: 10px;
    }
    .file-list {
      list-style: none;
      margin-top: 12px;
    }
    .file-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 12px;
      background: var(--bg-elevated);
      border-radius: 6px;
      margin-bottom: 8px;
      border: 1px solid var(--border-subtle);
      font-size: 14px;
    }
    .file-name {
      font-family: var(--font-code);
      color: var(--text-primary);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 65%;
    }
    .file-action {
      color: var(--brand-primary);
      text-decoration: none;
      font-weight: 600;
    }
    .upload-box {
      border: 2px dashed var(--border-highlight);
      border-radius: 8px;
      padding: 20px;
      text-align: center;
      background: rgba(56, 189, 248, 0.03);
    }
    .upload-box input[type="file"] { margin: 12px 0; color: var(--text-secondary); }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🌸 Aminsa Amin — Mobile & Laptop Hub</h1>
      <p>Mutual Two-Way Device Connection & Fast Asset Bridge</p>
      <span class="badge">● Online & Sync Ready</span>
    </header>

    <!-- Master Face Download Card -->
    <div class="card">
      <h2>📸 1. Canonical 4K Face Master</h2>
      <p style="font-size: 13px; color: var(--text-secondary); margin-bottom: 12px;">
        100% Biometric Ground Truth (source: aminsaface7.png). Direct 1-tap download to your mobile gallery.
      </p>
      <div class="preview-box">
        <img class="preview-img" src="/character/aminsa_face_master_4k.jpg" alt="Aminsa Master Face">
      </div>
      <a class="btn btn-primary" href="/character/aminsa_face_master_4k.jpg" download="aminsa_face_master_4k.jpg">
        📥 Download 4K Master JPG to Mobile
      </a>
      <a class="btn btn-secondary" href="/character/aminsa_face_master_4k.png" download="aminsa_face_master_4k.png">
        📥 Download Lossless PNG (4096×4096)
      </a>
    </div>

    <!-- Received Files Browser -->
    <div class="card">
      <h2>📂 2. Received Files (Live Exchange Folder)</h2>
      <p style="font-size: 13px; color: var(--text-secondary);">
        All files synced to PC Received Files folder:
      </p>
      <ul class="file-list">
        {FILE_ITEMS}
      </ul>
    </div>

    <!-- Upload from Phone to Laptop -->
    <div class="card">
      <h2>📤 3. Send from Mobile to Laptop</h2>
      <div class="upload-box">
        <form action="/upload" method="post" enctype="multipart/form-data">
          <p style="font-size: 13px; color: var(--text-secondary);">Choose any image, video, or document from your phone to send directly into Laptop Received Files:</p>
          <input type="file" name="file" required>
          <button type="submit" class="btn btn-primary" style="margin-top: 10px;">⬆️ Upload to Laptop</button>
        </form>
      </div>
    </div>
  </div>
</body>
</html>
"""

class MutualHubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_path = urllib.parse.unquote(self.path.split('?')[0])
        if url_path == "/" or url_path == "/index.html":
            self.serve_home()
        else:
            self.serve_static(url_path)

    def serve_home(self):
        items_html = ""
        if os.path.exists(RECEIVED_DIR):
            for fname in os.listdir(RECEIVED_DIR):
                fpath = os.path.join(RECEIVED_DIR, fname)
                if os.path.isfile(fpath):
                    size_kb = os.path.getsize(fpath) / 1024
                    size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.2f} MB"
                    items_html += f"""
                    <li class="file-item">
                      <span class="file-name">{fname} ({size_str})</span>
                      <a class="file-action" href="/Received%20Files/{urllib.parse.quote(fname)}" download="{fname}">Download</a>
                    </li>
                    """
        if not items_html:
            items_html = '<li class="file-item" style="color: var(--text-secondary)">No files in Received Files folder yet.</li>'

        content = HTML_TEMPLATE.replace("{FILE_ITEMS}", items_html).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def serve_static(self, rel_path):
        clean_path = rel_path.lstrip("/\\")
        full_path = os.path.normpath(os.path.join(ROOT_DIR, clean_path))
        
        if not full_path.startswith(ROOT_DIR) or not os.path.exists(full_path):
            self.send_error(404, "File Not Found")
            return

        if os.path.isdir(full_path):
            self.send_error(403, "Directory Listing Forbidden")
            return

        ext = os.path.splitext(full_path)[1].lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".mp4": "video/mp4",
            ".json": "application/json",
            ".txt": "text/plain",
            ".pdf": "application/pdf"
        }
        content_type = mime_types.get(ext, "application/octet-stream")

        size = os.path.getsize(full_path)
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(size))
        self.end_headers()

        with open(full_path, "rb") as f:
            while chunk := f.read(65536):
                self.wfile.write(chunk)

    def do_POST(self):
        if self.path == "/upload":
            content_length = int(self.headers.get('Content-Length', 0))
            content_type = self.headers.get('Content-Type', '')
            
            if 'multipart/form-data' in content_type and content_length > 0:
                boundary = content_type.split('boundary=')[1].encode()
                body = self.rfile.read(content_length)
                
                parts = body.split(b'--' + boundary)
                for part in parts:
                    if b'filename="' in part:
                        headers_part, file_data = part.split(b'\r\n\r\n', 1)
                        file_data = file_data.rstrip(b'\r\n')
                        
                        match = re.search(r'filename="([^"]+)"', headers_part.decode('utf-8', errors='ignore'))
                        if match:
                            filename = os.path.basename(match.group(1))
                            out_path = os.path.join(RECEIVED_DIR, filename)
                            os.makedirs(RECEIVED_DIR, exist_ok=True)
                            with open(out_path, 'wb') as f:
                                f.write(file_data)
                            
                            self.send_response(303)
                            self.send_header("Location", "/")
                            self.end_headers()
                            return
            self.send_error(400, "Upload Failed")

def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, MutualHubHandler)
    print("=" * 65)
    print("🌐 AMINSA MOBILE-LAPTOP MUTUAL HUB ACTIVE")
    print(f"[*] Access from Laptop: http://localhost:{PORT}")
    print(f"[*] Access from Phone : http://192.168.1.26:{PORT}")
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")

if __name__ == "__main__":
    run_server()
