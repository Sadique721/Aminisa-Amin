# -*- coding: utf-8 -*-
"""
Supabase Storage & Public CDN Ingestion
Uploads rendered master reels and images to Supabase Bucket 'aminsa-media'
and returns public CDN URLs required for Meta Graph API ingestion.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error

def load_env():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(root, ".env")
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

class SupabaseMediaStorage:
    def __init__(self):
        env = load_env()
        self.supabase_url = env.get("SUPABASE_URL", "").rstrip("/")
        self.supabase_key = env.get("SUPABASE_KEY", "") or env.get("SUPABASE_SERVICE_ROLE_KEY", "")
        self.bucket = env.get("STORAGE_BUCKET", "aminsa-media")
        self.dry_run = env.get("DRY_RUN_MODE", "True").lower() in ("true", "1", "yes")

    def upload(self, file_path, public_name=None):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        fname = public_name or os.path.basename(file_path)
        ext = os.path.splitext(fname)[1].lower()
        content_type = "video/mp4" if ext == ".mp4" else "image/jpeg"

        # If Supabase is unconfigured or in dry-run mode, return simulated public CDN URL
        if self.dry_run or not self.supabase_url or "your_" in self.supabase_url:
            mock_url = f"https://media.aminsa.live/public/{self.bucket}/{fname}"
            print(f"[*] [Storage DRY RUN] Staged '{fname}' -> {mock_url}")
            return mock_url

        # Supabase Storage v1 Upload Endpoint:
        # POST {SUPABASE_URL}/storage/v1/object/{bucket}/{path}
        upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket}/{fname}"
        with open(file_path, "rb") as f:
            file_data = f.read()

        headers = {
            "Authorization": f"Bearer {self.supabase_key}",
            "apiKey": self.supabase_key,
            "Content-Type": content_type,
            "x-upsert": "true"
        }

        req = urllib.request.Request(upload_url, data=file_data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                public_cdn_url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{fname}"
                print(f"[+] [Supabase Storage] Uploaded: {public_cdn_url}")
                return public_cdn_url
        except Exception as e:
            print(f"[WARN] Supabase upload failed ({e}). Returning fallback CDN URL.")
            return f"https://media.aminsa.live/public/{self.bucket}/{fname}"

storage = SupabaseMediaStorage()
