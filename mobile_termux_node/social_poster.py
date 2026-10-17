"""
Social Poster Driver for Md Sadique Amin Mobile
======================================
Prepares and initiates cross-platform posting for Instagram, Threads, and YouTube
directly on the phone using Android Intents and local ADB clipboard automation.
"""

import time
import subprocess
from adb_bridge import bridge
from config import PACKAGES

class SocialPoster:
    def copy_to_clipboard(self, text):
        """Sets clipboard in Termux so paste works anywhere."""
        try:
            p = subprocess.Popen(["termux-clipboard-set"], stdin=subprocess.PIPE)
            p.communicate(input=text.encode("utf-8"))
        except Exception as e:
            print(f"[-] Clipboard set error: {e}")

    def share_to_instagram(self, media_path, caption):
        """Prepares Instagram post / Reel."""
        print("[*] Preparing Instagram share...")
        self.copy_to_clipboard(caption)
        # Launch Instagram Reel / Share intent
        bridge.cmd(["shell", "am", "start", "-a", "android.intent.action.SEND",
                    "-t", "video/mp4",
                    "--eu", "android.intent.extra.STREAM", f"file://{media_path}",
                    "-p", PACKAGES["instagram"]])
        time.sleep(3)
        print("[+] Instagram share intent triggered (Caption copied to clipboard)!")

    def share_to_threads(self, caption):
        """Prepares Threads post."""
        print("[*] Preparing Threads post...")
        self.copy_to_clipboard(caption)
        bridge.cmd(["shell", "am", "start", "-a", "android.intent.action.SEND",
                    "-t", "text/plain",
                    "--es", "android.intent.extra.TEXT", caption,
                    "-p", PACKAGES["threads"]])
        time.sleep(3)
        print("[+] Threads share intent triggered!")

    def share_to_facebook(self, media_path, caption):
        """Prepares Facebook post / Reel."""
        print("[*] Preparing Facebook share...")
        self.copy_to_clipboard(caption)
        bridge.cmd(["shell", "am", "start", "-a", "android.intent.action.SEND",
                    "-t", "video/mp4",
                    "--eu", "android.intent.extra.STREAM", f"file://{media_path}",
                    "-p", PACKAGES["facebook"]])
        time.sleep(3)
        print("[+] Facebook share intent triggered!")

    def share_to_youtube(self, media_path, title):
        """Prepares YouTube Shorts upload."""
        print("[*] Preparing YouTube Shorts upload...")
        bridge.cmd(["shell", "am", "start", "-a", "android.intent.action.SEND",
                    "-t", "video/*",
                    "--eu", "android.intent.extra.STREAM", f"file://{media_path}",
                    "-p", PACKAGES["youtube"]])
        time.sleep(3)
        print("[+] YouTube upload intent triggered!")

    def post_to_all_individual_platforms(self, media_path, caption, title=None):
        """
        Sequentially posts to Instagram, Facebook, Threads, and YouTube
        as individual standalone app automations.
        """
        print("=" * 60)
        print("🚀 [INDIVIDUAL APP AUTOMATION] Cross-Platform Broadcast")
        print("=" * 60)
        
        # 1. Instagram
        self.share_to_instagram(media_path, caption)
        time.sleep(5)
        
        # 2. Facebook
        self.share_to_facebook(media_path, caption)
        time.sleep(5)
        
        # 3. Threads
        self.share_to_threads(caption)
        time.sleep(5)
        
        # 4. YouTube Shorts
        if title:
            self.share_to_youtube(media_path, title)
        
        print("[✓] All individual platform triggers dispatched successfully!")

social_poster = SocialPoster()

