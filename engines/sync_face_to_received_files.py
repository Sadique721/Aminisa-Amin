# -*- coding: utf-8 -*-
"""
Sync Latest Aminsa Face Master to Received Files (PC & Mobile)
=============================================================
1. Copies the enhanced 4K Aminsa Face Master to all PC 'Received Files' locations:
   - Workspace: Received Files/
   - Windows Documents: Documents/Received Files/
   - Windows Downloads: Downloads/Received Files/
   - Windows Pictures: Pictures/Received Files/
2. Pushes directly to connected Phone (OnePlus / OPPO WS9X6LLJXW7H7TFQ) via ADB:
   - /sdcard/Download/aminsa_face_master_4k.jpg
   - /sdcard/DCIM/Aminsa/aminsa_face_master_4k.jpg
   - /sdcard/DCIM/Camera/aminsa_face_master_4k.jpg
   - Broadcasts Android MediaScanner so it instantly appears in Phone Gallery.
"""

import os
import sys
import shutil
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_JPG = os.path.join(PROJECT_ROOT, "character", "aminsa_face_master_4k.jpg")
SRC_PNG = os.path.join(PROJECT_ROOT, "character", "aminsa_face_master_4k.png")
ADB_EXE = r"C:\platform-tools\adb.exe"
DEVICE_SERIAL = "WS9X6LLJXW7H7TFQ"

USER_HOME = os.path.expanduser("~")

PC_DESTS = [
    os.path.join(PROJECT_ROOT, "Received Files"),
    os.path.join(USER_HOME, "Documents", "Received Files"),
    os.path.join(USER_HOME, "Downloads", "Received Files"),
    os.path.join(USER_HOME, "Pictures", "Received Files"),
    os.path.join(USER_HOME, "Downloads")
]

def sync_pc():
    print("=" * 65)
    print("📂 SYNCING AMINSA 4K FACE MASTER TO PC RECEIVED FILES")
    print("=" * 65)
    for folder in PC_DESTS:
        try:
            os.makedirs(folder, exist_ok=True)
            dst_jpg = os.path.join(folder, "aminsa_face_master_4k.jpg")
            dst_png = os.path.join(folder, "aminsa_face_master_4k.png")
            shutil.copy2(SRC_JPG, dst_jpg)
            shutil.copy2(SRC_PNG, dst_png)
            print(f"[✔] Successfully copied to PC: {folder}")
        except Exception as e:
            print(f"[-] Notice on {folder}: {e}")

def sync_phone():
    print("\n" + "=" * 65)
    print("📱 SYNCING AMINSA 4K FACE MASTER TO MOBILE PHONE (ADB)")
    print("=" * 65)
    if not os.path.exists(ADB_EXE):
        print("[-] adb.exe not found at C:\\platform-tools\\adb.exe")
        return

    try:
        res = subprocess.run([ADB_EXE, "devices"], capture_output=True, text=True, timeout=5)
        if DEVICE_SERIAL not in res.stdout and "device" not in res.stdout:
            print("[-] Phone not detected or unauthorized in ADB.")
            return

        phone_targets = [
            "/sdcard/Download/aminsa_face_master_4k.jpg",
            "/sdcard/DCIM/Aminsa/aminsa_face_master_4k.jpg",
            "/sdcard/DCIM/Camera/aminsa_face_master_4k.jpg"
        ]

        for target in phone_targets:
            parent = os.path.dirname(target)
            subprocess.run([ADB_EXE, "-s", DEVICE_SERIAL, "shell", f"mkdir -p '{parent}'"], timeout=10)
            subprocess.run([ADB_EXE, "-s", DEVICE_SERIAL, "push", SRC_JPG, target], timeout=20)
            # Notify Android Media Gallery to index photo immediately
            subprocess.run([
                ADB_EXE, "-s", DEVICE_SERIAL, "shell",
                f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{target}"
            ], timeout=10)
            print(f"[✔] Successfully pushed to Phone: {target}")

    except Exception as e:
        print(f"[-] Phone sync error: {e}")

if __name__ == "__main__":
    sync_pc()
    sync_phone()
