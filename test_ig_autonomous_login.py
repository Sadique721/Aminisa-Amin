import json
import os
from instagrapi import Client

SESSION_FILE = "config/ig_session.json"
USERNAME = "md_sadique_amin.official"
PASSWORD = "Md Sadique AminCreator@2026"

def login_and_verify():
    cl = Client()
    cl.delay_range = [2, 5]
    
    if os.path.exists(SESSION_FILE):
        try:
            print("[*] Found existing Instagram session. Loading...")
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            print("[+] Session loaded and verified successfully!")
            return cl
        except Exception as e:
            print(f"[-] Session expired or invalid: {e}. Re-logging in...")
            
    print(f"[*] Logging in as '{USERNAME}'...")
    try:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print(f"[+] Login SUCCESSFUL! Session dumped to {SESSION_FILE}")
        return cl
    except Exception as e:
        print(f"[!] Login error: {e}")
        return None

if __name__ == "__main__":
    login_and_verify()
