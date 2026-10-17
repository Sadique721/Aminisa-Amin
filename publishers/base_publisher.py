# -*- coding: utf-8 -*-
"""
Base Publisher Module for Aminsa Autonomous Social Media Handler
Manages .env credential loading, dry-run simulation, and HTTP API error handling.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
import urllib.parse

def load_env(env_path=None):
    """Simple zero-dependency .env loader."""
    if not env_path:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(root, ".env")
    
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    env_vars[k] = v
                    os.environ[k] = v
    return env_vars

ENV = load_env()

class BasePublisher:
    def __init__(self, platform_name):
        self.platform = platform_name
        self.dry_run = os.getenv("DRY_RUN_MODE", "True").lower() in ("true", "1", "yes")

    def make_request(self, url, data=None, method="POST", headers=None):
        """Unified HTTP request with error decoding."""
        h = headers or {}
        encoded_data = None
        if data is not None:
            if isinstance(data, dict):
                encoded_data = urllib.parse.urlencode(data).encode("utf-8")
                h.setdefault("Content-Type", "application/x-www-form-urlencoded")
            elif isinstance(data, str):
                encoded_data = data.encode("utf-8")

        req = urllib.request.Request(url, data=encoded_data, headers=h, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_text = resp.read().decode("utf-8")
                return json.loads(resp_text)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_body)
                return {"error": err_json, "status_code": e.code}
            except Exception:
                return {"error": err_body, "status_code": e.code}
        except Exception as e:
            return {"error": str(e), "status_code": 500}
