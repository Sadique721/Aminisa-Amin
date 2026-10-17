"""
ADB Bridge for Md Sadique Amin Mobile (Termux Native)
============================================
Communicates with localhost ADB daemon on port 5555 inside Termux.
Enables full screen touch, text input, app launch, and UI dump.
"""

import subprocess
import time
import os
from config import ADB_TARGET, PACKAGES

# Termux environment setup
os.environ["PATH"] = "/data/data/com.termux/files/usr/bin:" + os.environ.get("PATH", "")
os.environ["TMPDIR"] = "/data/data/com.termux/files/usr/tmp"
os.environ["HOME"] = "/data/data/com.termux/files/home"

ADB_BIN = "/data/data/com.termux/files/usr/bin/adb"

class AdbBridge:
    def __init__(self, target=ADB_TARGET):
        self.target = target
        self.adb = ADB_BIN if os.path.exists(ADB_BIN) else "adb"

    def cmd(self, args, timeout=15):
        """Execute an ADB command against the target device."""
        full_cmd = [self.adb, "-s", self.target] + args
        try:
            res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
            return res.stdout.strip(), res.stderr.strip(), res.returncode
        except Exception as e:
            return "", str(e), -1

    def ensure_connected(self):
        """Ensure connection to localhost ADB."""
        # 1. Connect
        subprocess.run([self.adb, "connect", self.target], capture_output=True, timeout=10)
        # 2. Check via shell getprop (not bare adb getprop which is invalid)
        out, err, code = self.cmd(["shell", "getprop", "ro.product.model"])
        if code == 0 and out:
            return True, out
        
        # Try reconnecting once (kill-server + reconnect)
        subprocess.run([self.adb, "kill-server"], capture_output=True, timeout=5)
        time.sleep(1)
        subprocess.run([self.adb, "start-server"], capture_output=True, timeout=10)
        subprocess.run([self.adb, "connect", self.target], capture_output=True, timeout=10)
        out, err, code = self.cmd(["shell", "getprop", "ro.product.model"])
        return code == 0, out or err

    def wake_screen(self):
        """Wake up the screen and unlock if simple swipe."""
        # KEYCODE_WAKEUP = 224
        self.cmd(["shell", "input", "keyevent", "224"])
        time.sleep(0.5)
        # KEYCODE_MENU = 82 (often dismisses keyguard)
        self.cmd(["shell", "input", "keyevent", "82"])

    def launch_app(self, package_key_or_name, activity=None):
        """Launch app by package key from PACKAGES or raw package name."""
        pkg = PACKAGES.get(package_key_or_name, package_key_or_name)
        if activity:
            cmp_str = f"{pkg}/{activity}"
            return self.cmd(["shell", "am", "start", "-n", cmp_str])
        else:
            return self.cmd(["shell", "monkey", "-p", pkg, "-c", "android.intent.category.LAUNCHER", "1"])

    def tap(self, x, y):
        """Tap coordinate."""
        return self.cmd(["shell", "input", "tap", str(x), str(y)])

    def type_text(self, text):
        """Types text safely handling spaces."""
        chunks = text.split(" ")
        for i, chunk in enumerate(chunks):
            if chunk:
                # Escape special characters for input text
                escaped = chunk.replace("&", "\\&").replace("'", "\\'").replace('"', '\\"').replace("(", "\\(").replace(")", "\\)")
                self.cmd(["shell", "input", "text", escaped])
            if i < len(chunks) - 1:
                # Type space via keycode 62
                self.cmd(["shell", "input", "keyevent", "62"])

    def press_key(self, keycode):
        """Send keyevent (e.g. 3=HOME, 4=BACK, 66=ENTER)."""
        return self.cmd(["shell", "input", "keyevent", str(keycode)])

    def dump_ui(self, output_path="/sdcard/current_ui.xml"):
        """Dump UI hierarchy XML."""
        self.cmd(["shell", "uiautomator", "dump", output_path])
        return output_path

    def take_screenshot(self, output_path="/sdcard/current_screen.png"):
        """Capture screen."""
        self.cmd(["shell", "screencap", "-p", output_path])
        return output_path

    def notify(self, title, message):
        """Send native Android notification via termux-notification."""
        try:
            subprocess.run(["termux-notification", "--title", title, "--content", message], check=False)
        except Exception:
            pass

    def acquire_wake_lock(self):
        """Acquires Termux wake lock so CPU doesn't sleep."""
        try:
            subprocess.run(["termux-wake-lock"], check=False)
        except Exception:
            pass

    def release_wake_lock(self):
        """Releases Termux wake lock."""
        try:
            subprocess.run(["termux-wake-unlock"], check=False)
        except Exception:
            pass

bridge = AdbBridge()
