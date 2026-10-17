# -*- coding: utf-8 -*-
"""
Meta Graph API & Threads API Token Refresh Daemon
Refreshes Meta long-lived user tokens and Threads 60-day tokens automatically.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
from .base_publisher import load_env

def refresh_threads_token():
    env = load_env()
    token = env.get("THREADS_TOKEN", "")
    if not token or "your_" in token:
        print("[*] Threads token not configured in .env. Skipping refresh.")
        return False

    url = f"https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={token}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "access_token" in data:
                new_token = data["access_token"]
                expires_in = data.get("expires_in", 5184000) # ~60 days
                print(f"[+] Threads token refreshed successfully! Valid for {expires_in // 86400} days.")
                _update_env_key("THREADS_TOKEN", new_token)
                return True
    except Exception as e:
        print(f"[-] Threads token refresh failed: {e}")
    return False

def _update_env_key(key, new_value):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(root, ".env")
    if os.path.exists(env_path):
        lines = []
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key}=") or line.startswith(f"{key} ="):
                    lines.append(f"{key}={new_value}\n")
                else:
                    lines.append(line)
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"[+] Updated {key} in .env")

if __name__ == "__main__":
    refresh_threads_token()
