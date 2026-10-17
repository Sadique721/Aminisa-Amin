"""
Md Sadique Amin Multi-Platform Phone ADB Social Uploader
Automates the official Instagram App on OPPO A78 5G via ADB with:
1. Selection of latest rendered reel
2. AI Label auto-toggled ON
3. Threads auto-share toggle ON
4. Facebook Page auto-share toggle ON
5. 1-Shot Simultaneous Cross-Publishing to Instagram, Facebook, and Threads!
"""

import sys
import time
import subprocess
from mobile_app_controller import get_adb_device, ADB_EXE

def publish_latest_reel_multi_platform(caption_text):
    serial, state = get_adb_device()
    if state != "device":
        print(f"[-] ADB device not ready: {state}")
        return False
        
    print(f"[*] Automating official Instagram App on {serial} for Multi-Platform Publish...")
    
    # 1. Bring Instagram Profile to foreground
    subprocess.run([ADB_EXE, "-s", serial, "shell", "am", "start", "-n", "com.instagram.android/.activity.MainTabActivity"], check=False)
    time.sleep(2)
    
    # 2. Tap profile tab (bottom right)
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "648", "1500"], check=False)
    time.sleep(2)
    
    # 3. Tap '+' (Create new) at top left
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "40", "111"], check=False)
    time.sleep(2)
    
    # 4. Tap 'Reel' from creation sheet
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "360", "939"], check=False)
    time.sleep(3)
    
    # 5. Handle draft prompt or select latest video
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "360", "950"], check=False)
    time.sleep(3)
    
    # 6. Tap 'Next' in Reel editor
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "641", "1502"], check=False)
    time.sleep(3)
    
    # 7. Dismiss download dialog if shown
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "360", "1397"], check=False)
    time.sleep(1)
    
    # 8. Focus caption field
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "360", "728"], check=False)
    time.sleep(1)
    
    # 9. Type caption (split chunks)
    words = caption_text.split(" ")
    chunk = []
    for word in words:
        clean = word.replace("'", "").replace('"', '').replace('&', 'and').replace('#', '\\#')
        chunk.append(clean)
        if len(chunk) >= 4:
            cmd = [ADB_EXE, "-s", serial, "shell", f"input text {'%s'.join(chunk)}%s"]
            subprocess.run(cmd, check=False)
            chunk = []
            time.sleep(0.1)
    if chunk:
        cmd = [ADB_EXE, "-s", serial, "shell", f"input text {'%s'.join(chunk)}"]
        subprocess.run(cmd, check=False)
        
    time.sleep(1)
    # Dismiss keyboard
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "keyevent", "4"], check=False)
    time.sleep(1)
    
    # 10. Enable AI Label toggle switch
    print("[*] Activating AI Content Label toggle...")
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "650", "1305"], check=False)
    time.sleep(1)
    
    # 11. Enable Cross-Posting Toggles for Threads & Facebook
    print("[*] Enabling Cross-Posting to Threads & Facebook Page...")
    # Threads toggle (X=640, Y=1040)
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "640", "1040"], check=False)
    time.sleep(1)
    # Facebook toggle (X=640, Y=1140)
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "640", "1140"], check=False)
    time.sleep(1)
    
    # 12. Tap Next / Share button
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "533", "1465"], check=False)
    time.sleep(2)
    
    # 13. Final Share confirmation
    subprocess.run([ADB_EXE, "-s", serial, "shell", "input", "tap", "360", "1390"], check=False)
    time.sleep(4)
    
    print("[+] Simultaneous multi-platform publish (Instagram + Threads + Facebook) executed!")
    return True

# Backwards compatibility alias for orchestrator
publish_latest_reel_on_instagram = publish_latest_reel_multi_platform

if __name__ == "__main__":
    test_caption = "Hello everyone! Main hoon Md Sadique Amin. Future tech & AI updates! #Md Sadique Amin #AICreator"
    publish_latest_reel_multi_platform(test_caption)
