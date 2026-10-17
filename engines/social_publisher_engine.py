# -*- coding: utf-8 -*-
"""
Md Sadique Amin Cross-Platform Social Publisher Engine
==============================================
Handles automated publishing from PC to connected OnePlus phone over ADB:
1. Pushes rendered video to /sdcard/DCIM/Camera/ (Camera roll)
2. Broadcasts MEDIA_SCANNER_SCAN_FILE so Android registers it in MediaStore
3. Resolves the MediaStore content:// URI for modern Android 14/15 scoped storage
4. Prepares caption on phone clipboard
5. Dispatches SEND Intent to Instagram Reels / YouTube Shorts / Facebook / Threads
"""

import os
import sys
import time
import subprocess
import re

ADB_DEFAULT = r"C:\platform-tools\adb.exe"

class SocialPublisherEngine:
    def __init__(self, adb_path=None):
        self.adb = adb_path or ADB_DEFAULT

    def get_connected_device(self):
        try:
            res = subprocess.run([self.adb, "devices"], stdout=subprocess.PIPE, text=True)
            for line in res.stdout.strip().splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 2 and parts[1] == "device":
                    return parts[0]
        except Exception:
            pass
        return None

    def push_video_to_phone(self, local_video_path, remote_filename="md_sadique_amin_reel.mp4"):
        serial = self.get_connected_device()
        if not serial:
            print("[-] No ADB device connected!")
            return None

        remote_path = f"/sdcard/DCIM/Camera/{remote_filename}"
        # Ensure DCIM/Camera directory exists
        subprocess.run([self.adb, "-s", serial, "shell", "mkdir", "-p", "/sdcard/DCIM/Camera"], check=False)

        print(f"[*] Pushing {os.path.basename(local_video_path)} to {remote_path}...")
        push_res = subprocess.run([self.adb, "-s", serial, "push", local_video_path, remote_path],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if push_res.returncode != 0:
            print(f"[-] Push failed: {push_res.stderr}")
            return None

        # Scan media
        scan_cmd = [
            self.adb, "-s", serial, "shell", "am", "broadcast",
            "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
            "-d", f"file://{remote_path}"
        ]
        subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(1.5)

        # Retrieve content URI from MediaStore
        content_uri = self._get_content_uri(serial, remote_path)
        print(f"[+] Pushed & Registered. Content URI: {content_uri or 'Gallery File Ready'}")
        return {
            "remote_path": remote_path,
            "content_uri": content_uri,
            "serial": serial
        }

    def _get_content_uri(self, serial, remote_path):
        cmd = [
            self.adb, "-s", serial, "shell", "content", "query",
            "--uri", "content://media/external/video/media",
            "--projection", "_id:_data"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        last_id = None
        for line in res.stdout.splitlines():
            if remote_path in line or os.path.basename(remote_path) in line:
                m = re.search(r"_id=(\d+)", line)
                if m:
                    last_id = m.group(1)
        if last_id:
            return f"content://media/external/video/media/{last_id}"
        return None

    def set_phone_clipboard(self, serial, text):
        """Sets text in phone clipboard using Termux API or fallback typing."""
        try:
            # Try termux-clipboard-set if Termux is installed
            cmd = [self.adb, "-s", serial, "shell", "su", "-c", f"termux-clipboard-set '{text}'"]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode != 0:
                # Fallback: write to /sdcard/caption.txt so user/daemon can read it
                with open("scratch_test/caption_temp.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                subprocess.run([self.adb, "-s", serial, "push", "scratch_test/caption_temp.txt", "/sdcard/Md Sadique Amin_Latest_Caption.txt"], check=False)
        except Exception as e:
            print(f"[-] Clipboard set error: {e}")

    def trigger_instagram_reel_composer(self, media_info, caption):
        serial = media_info["serial"]
        content_uri = media_info.get("content_uri")
        self.set_phone_clipboard(serial, caption)

        # Wake phone
        subprocess.run([self.adb, "-s", serial, "shell", "input", "keyevent", "224"], check=False)
        subprocess.run([self.adb, "-s", serial, "shell", "input", "keyevent", "82"], check=False)

        if content_uri:
            cmd = [
                self.adb, "-s", serial, "shell", "am", "start",
                "-a", "android.intent.action.SEND",
                "-t", "video/mp4",
                "--eu", "android.intent.extra.STREAM", content_uri,
                "--grant-read-uri-permission",
                "-p", "com.instagram.android"
            ]
        else:
            cmd = [
                self.adb, "-s", serial, "shell", "am", "start",
                "-n", "com.instagram.android/.activity.MainTabActivity"
            ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"[+] Instagram Composer launched on {serial}!")
        return res.returncode == 0

    def trigger_youtube_shorts_composer(self, media_info, title, description):
        serial = media_info["serial"]
        content_uri = media_info.get("content_uri")
        if content_uri:
            cmd = [
                self.adb, "-s", serial, "shell", "am", "start",
                "-a", "android.intent.action.SEND",
                "-t", "video/mp4",
                "--eu", "android.intent.extra.STREAM", content_uri,
                "--grant-read-uri-permission",
                "-p", "com.google.android.youtube"
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"[+] YouTube Shorts Composer launched on {serial}!")
            return True
        return False

publisher_engine = SocialPublisherEngine()
