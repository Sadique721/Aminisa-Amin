"""
Md Sadique Amin Master Credentials Verification & Auto-Lock Tool
Safely tests and validates username & password before saving across the entire workspace.
"""

import os
import sys
import json
from instagrapi import Client
from instagrapi.exceptions import BadPassword, ChallengeRequired, TwoFactorRequired

USERNAME = "md_sadique_amin.official"
CANDIDATE_PASSWORDS = [
    "Md Sadique AminAI@Creator2026!",
    "Md Sadique AminCreator@2026"
]

CONFIG_FILE = "accounts_config.json"
ENV_FILE = ".env"
SESSION_FILE = "config/ig_session.json"

def save_verified_credentials(username, password):
    print("\n" + "=" * 70)
    print(f"[+] LOCKING & SAVING VERIFIED CREDENTIALS PERMANENTLY")
    print("=" * 70)
    
    # 1. Update accounts_config.json
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["system_info"]["master_username"] = username
        data["system_info"]["master_password"] = password
        data["system_info"]["status"] = "VERIFIED_AND_LOCKED"
        
        for acc in data.get("meta_channels", {}).get("instagram_accounts", []):
            acc["username"] = username
            acc["password"] = password
            
        for acc in data.get("meta_channels", {}).get("threads_accounts", []):
            acc["username"] = username
            acc["password"] = password
            
        for page in data.get("meta_channels", {}).get("facebook_pages", []):
            page["admin_password"] = password
            
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[✓] Verified credentials locked into: {CONFIG_FILE}")

    # 2. Update .env
    env_content = f"""# Md Sadique Amin Autonomous Master Credentials (VERIFIED & LOCKED)
MASTER_EMAIL=mdsadiqueamin721721@gmail.com
MASTER_USERNAME={username}
MASTER_PASSWORD={password}

# Meta Ecosystem
IG_USERNAME={username}
IG_PASSWORD={password}
FB_PAGE_ID=61594814066987
FB_PAGE_NAME=Md Sadique Amin
THREADS_USERNAME={username}
THREADS_PASSWORD={password}

# YouTube Ecosystem
YT_CHANNEL_NAME=Md Sadique Amin Global
YT_ADMIN_EMAIL=mdsadiqueamin721721@gmail.com

# Persona Voice & Greeting
GREETING_RULE=NEVER_NAMASTE_ALWAYS_HELLO_EVERYONE
VOICE_NAME=hi-IN-SwaraNeural
VOICE_PITCH=+0Hz
VOICE_RATE=+0%
VOICE_FREQUENCY_F0=224Hz
"""
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(env_content)
    print(f"[✓] Verified credentials locked into: {ENV_FILE}")
    print("=" * 70)

def test_credentials(custom_pwd=None):
    passwords_to_try = [custom_pwd] if custom_pwd else CANDIDATE_PASSWORDS
    
    cl = Client()
    cl.delay_range = [2, 4]
    cl.set_user_agent("Instagram 324.0.0.38.106 Android (33/13; 420dpi; 1080x2400; OPPO; CPH2565; oppo_cph2565; mt6833; en_US; 578635841)")
    
    print(f"[*] Starting Credential Verification for username: '{USERNAME}'...")
    
    for pwd in passwords_to_try:
        if not pwd:
            continue
        masked = pwd[:3] + "*" * (len(pwd) - 5) + pwd[-2:] if len(pwd) > 5 else "***"
        print(f"\n[*] Testing password candidate: {masked} ...")
        
        try:
            cl.login(USERNAME, pwd)
            print(f"[✓] SUCCESS! Password verified and authenticated successfully!")
            
            # Save session cache
            os.makedirs("config", exist_ok=True)
            cl.dump_settings(SESSION_FILE)
            print(f"[✓] Instagram session dumped to: {SESSION_FILE}")
            
            # Save to configuration files
            save_verified_credentials(USERNAME, pwd)
            return True, pwd
            
        except BadPassword:
            print(f"[-] Incorrect password: {masked}")
        except TwoFactorRequired:
            print(f"[!] 2-Factor Authentication (2FA) is enabled for this account.")
            save_verified_credentials(USERNAME, pwd)
            return True, pwd
        except ChallengeRequired:
            print(f"[!] Instagram checkpoint challenge required (email/SMS security code).")
            save_verified_credentials(USERNAME, pwd)
            return True, pwd
        except Exception as e:
            print(f"[!] Verification response note: {e}")
            
    print("\n[-] None of the automatic candidate passwords matched.")
    return False, None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pwd_arg = sys.argv[1]
        test_credentials(pwd_arg)
    else:
        test_credentials()
