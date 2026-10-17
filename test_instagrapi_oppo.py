import os
import sys
from instagrapi import Client

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

USERNAME = "md_sadique_amin.official"
PASSWORD = "Md Sadique AminAI@Creator2026!"
SESSION_FILE = "config/ig_session.json"

def test_login():
    cl = Client()
    # Use modern official OPPO A78 5G user-agent string
    cl.set_user_agent("Instagram 335.0.0.35.95 Android (34/14; 420dpi; 1080x2400; OPPO; CPH2565; oppo_cph2565; mt6833; en_US; 604928154)")
    cl.delay_range = [2, 4]
    
    print(f"[*] Testing modern login for @{USERNAME}...")
    try:
        cl.login(USERNAME, PASSWORD)
        os.makedirs("config", exist_ok=True)
        cl.dump_settings(SESSION_FILE)
        print(f"[✓] SUCCESS! Logged in as @{USERNAME}!")
        print(f"[✓] User ID: {cl.user_id}")
        return cl
    except Exception as e:
        print(f"[-] Login failed: {e}")
        return None

if __name__ == "__main__":
    test_login()
