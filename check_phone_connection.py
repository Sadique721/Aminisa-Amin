import subprocess
import os
import sys

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

adb_exe = r"C:\platform-tools\adb.exe"

print("=" * 60)
print("📱 CHECKING ADB DEVICE CONNECTION TO OPPO A78 5G")
print("=" * 60)

res = subprocess.run([adb_exe, "devices", "-l"], capture_output=True, text=True)
print(res.stdout)

# Check USB devices via PowerShell
ps = "Get-PnpDevice -PresentOnly | Where-Object { $_.FriendlyName -like '*OPPO*' -or $_.FriendlyName -like '*Android*' -or $_.FriendlyName -like '*Phone*' -or $_.InstanceId -like '*VID_22D9*' } | Select-Object Status, FriendlyName, InstanceId | Out-String"
res_usb = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True)
print("USB Hardware Scan:")
if res_usb.stdout.strip():
    print(res_usb.stdout)
else:
    print("[-] No USB hardware match found. Phone might be connected via Wi-Fi or unplugged.")
