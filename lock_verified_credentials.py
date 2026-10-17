import os
import sys
import json

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

USERNAME = "md_sadique_amin.official"
PASSWORD = "Md Sadique AminAI@Creator2026!"
CONFIG_FILE = "accounts_config.json"
ENV_FILE = ".env"
SESSION_FILE = "config/ig_session.json"

def lock_credentials():
    print(f"[*] Locking verified credentials for '{USERNAME}' with password 'Md Sadique AminAI@Creator2026!'...")
    
    # 1. Update accounts_config.json
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["system_info"]["master_username"] = USERNAME
        data["system_info"]["master_password"] = PASSWORD
        data["system_info"]["status"] = "VERIFIED_ACTIVE_CREDENTIALS_LOCKED"
        
        for acc in data.get("meta_channels", {}).get("instagram_accounts", []):
            acc["username"] = USERNAME
            acc["password"] = PASSWORD
            
        for acc in data.get("meta_channels", {}).get("threads_accounts", []):
            acc["username"] = USERNAME
            acc["password"] = PASSWORD
            
        for page in data.get("meta_channels", {}).get("facebook_pages", []):
            page["admin_password"] = PASSWORD
            
        for yt in data.get("youtube_channels", []):
            yt["admin_password"] = PASSWORD
            
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[✓] Successfully saved and locked in {CONFIG_FILE}")

    # 2. Update .env
    env_content = f"""# Md Sadique Amin Autonomous Master Credentials (VERIFIED & LOCKED)
MASTER_EMAIL=mdsadiqueamin721721@gmail.com
MASTER_USERNAME={USERNAME}
MASTER_PASSWORD={PASSWORD}

# Meta Ecosystem
IG_USERNAME={USERNAME}
IG_PASSWORD={PASSWORD}
FB_PAGE_ID=61594814066987
FB_PAGE_NAME=Md Sadique Amin
THREADS_USERNAME={USERNAME}
THREADS_PASSWORD={PASSWORD}

# YouTube Ecosystem
YT_CHANNEL_NAME=Md Sadique Amin Global
YT_ADMIN_EMAIL=mdsadiqueamin721721@gmail.com
YT_ADMIN_PASSWORD={PASSWORD}

# Persona Voice & Greeting
GREETING_RULE=NEVER_NAMASTE_ALWAYS_HELLO_EVERYONE
VOICE_NAME=hi-IN-SwaraNeural
VOICE_PITCH=+0Hz
VOICE_RATE=+0%
VOICE_FREQUENCY_F0=224Hz
"""
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(env_content)
    print(f"[✓] Successfully saved and locked in {ENV_FILE}")

if __name__ == "__main__":
    lock_credentials()
