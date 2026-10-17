"""
Md Sadique Amin Mobile Device Controller (OPPO A78 5G via ADB)
Manages mobile apps: YouTube Create, Termux, Instagram, Threads.
Transfers generated assets into /sdcard/DCIM/Md Sadique Amin/ & /sdcard/DCIM/Camera/ and triggers media scanners.
Passes explicit device serial (-s) to support multiple devices seamlessly.
"""

import os
import sys
import subprocess
import time

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ADB_EXE = r"C:\platform-tools\adb.exe"

# Target Apps to verify on OPPO A78 5G
TARGET_APPS = {
    "YouTube Create": "com.google.android.apps.youtube.producer",
    "YouTube": "com.google.android.youtube",
    "Instagram": "com.instagram.android",
    "Threads": "com.instagram.barcelona",
    "Termux": "com.termux",
    "Termux:API": "com.termux.api"
}

def get_adb_device():
    res = subprocess.run([ADB_EXE, "devices"], capture_output=True, text=True)
    lines = res.stdout.strip().split("\n")[1:]
    connected = []
    pending_state = None
    pending_serial = None
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            if parts[1] == "device":
                connected.append(parts[0])
            elif parts[1] in ("offline", "unauthorized"):
                pending_serial = parts[0]
                pending_state = parts[1]
            
    # Prefer USB hardware serial over Wi-Fi IP
    for serial in connected:
        if not serial.startswith("192.168."):
            return serial, "device"
            
    if connected:
        return connected[0], "device"

    if pending_serial:
        if pending_state == "offline":
            return pending_serial, "OFFLINE (Unlock phone screen & select File Transfer/MTP)"
        elif pending_state == "unauthorized":
            return pending_serial, "UNAUTHORIZED (Accept 'Always allow from this computer' on phone)"
        
    return None, "DISCONNECTED"

def audit_mobile_apps():
    print("=" * 70)
    print("📱 AUDITING INSTALLED APPS ON OPPO A78 5G VIA ADB")
    print("=" * 70)
    
    serial, state = get_adb_device()
    print(f"[*] Device Serial: {serial} | State: {state}")
    
    if state != "device":
        print("\n[-] Phone is not in 'device' state.")
        return False

    # Fetch installed packages
    print("[*] Querying installed packages via Android Package Manager...")
    res = subprocess.run([ADB_EXE, "-s", serial, "shell", "pm", "list", "packages"], capture_output=True, text=True)
    installed_packages = res.stdout

    print("\n📦 Target Creative & Automation Apps Status:")
    for app_name, pkg in TARGET_APPS.items():
        if f"package:{pkg}" in installed_packages:
            print(f"  🟢 {app_name:<20} ({pkg}) -> INSTALLED & READY")
        else:
            print(f"  ⚪ {app_name:<20} ({pkg}) -> NOT INSTALLED")

    # Ensure DCIM folders exist on phone
    print("\n[*] Initializing Md Sadique Amin Media Directories on Phone...")
    subprocess.run([ADB_EXE, "-s", serial, "shell", "mkdir", "-p", "/sdcard/DCIM/Md Sadique Amin", "/sdcard/DCIM/Camera"], check=False)
    print("  🟢 /sdcard/DCIM/Md Sadique Amin/ & /sdcard/DCIM/Camera/ are verified on phone storage.")
    return True

def push_media_to_phone(local_path):
    serial, state = get_adb_device()
    if state != "device":
        print("[-] Cannot push media: Phone not authorized/connected.")
        return False
        
    filename = os.path.basename(local_path)
    camera_path = f"/sdcard/DCIM/Camera/{filename}"
    md_sadique_amin_path = f"/sdcard/DCIM/Md Sadique Amin/{filename}"
    
    print(f"[*] Transferring '{filename}' -> '{camera_path}' on OPPO A78 5G ({serial})...")
    res = subprocess.run([ADB_EXE, "-s", serial, "push", local_path, camera_path], capture_output=True, text=True)
    if res.returncode == 0:
        # Also copy to Md Sadique Amin folder
        subprocess.run([ADB_EXE, "-s", serial, "shell", f"cp '{camera_path}' '{md_sadique_amin_path}'"], check=False)
        print(f"[+] Successfully transferred media to phone gallery & Md Sadique Amin folder!")
        
        # Trigger media scanner so Android Gallery & YouTube Create show it immediately
        subprocess.run([
            ADB_EXE, "-s", serial, "shell", "am", "broadcast", 
            "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", 
            "-d", f"file://{camera_path}"
        ], check=False)
        subprocess.run([
            ADB_EXE, "-s", serial, "shell", "am", "broadcast", 
            "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", 
            "-d", f"file://{md_sadique_amin_path}"
        ], check=False)
        return True
    else:
        print(f"[-] Push failed: {res.stderr}")
        return False

if __name__ == "__main__":
    audit_mobile_apps()
