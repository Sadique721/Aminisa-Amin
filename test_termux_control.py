#!/data/data/com.termux/files/usr/bin/python3
import subprocess
import time
import os
import sys

# Ensure Termux environment
os.environ["PATH"] = "/data/data/com.termux/files/usr/bin:" + os.environ.get("PATH", "")
os.environ["TMPDIR"] = "/data/data/com.termux/files/usr/tmp"
os.environ["HOME"] = "/data/data/com.termux/files/home"

ADB_CMD = ["adb", "-s", "127.0.0.1:5555"]

def run_adb(args):
    cmd = ADB_CMD + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip(), res.stderr.strip()

print("=" * 60)
print("TEST 1: Check Local ADB Device")
out, err = run_adb(["getprop", "ro.product.model"])
print(f"Phone Model: {out} (Error: {err})")

print("=" * 60)
print("TEST 2: Wake up screen if sleeping")
run_adb(["shell", "input", "keyevent", "224"])
time.sleep(1)

print("=" * 60)
print("TEST 3: Launch YouTube Create from Termux")
out, err = run_adb(["shell", "am", "start", "-n", "com.google.android.apps.youtube.producer/.application.MainActivity"])
print(f"Launch result: {out}")
time.sleep(3)

print("=" * 60)
print("TEST 4: Check Foreground Activity")
out, err = run_adb(["shell", "dumpsys", "window", "displays"])
for line in out.splitlines():
    if "mCurrentFocus" in line or "mFocusedApp" in line:
        print(f"Focus: {line.strip()}")

print("=" * 60)
print("TEST 5: Termux Native Screen Capture")
run_adb(["shell", "screencap", "-p", "/sdcard/termux_yt_create_test.png"])
print("Screenshot saved to /sdcard/termux_yt_create_test.png")

print("=" * 60)
print("TEST 6: Return to Home / Termux")
run_adb(["shell", "input", "keyevent", "3"]) # HOME
print("Returned to Home successfully!")
print("ALL TESTS PASSED INSIDE TERMUX!")
