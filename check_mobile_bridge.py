import os
import sys
import subprocess
import socket

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def check_usb_devices():
    print("=" * 60)
    print("🔌 1. CHECKING USB HARDWARE STATUS (OPPO A78 5G)")
    print("=" * 60)
    
    ps_script = """
    $devices = Get-PnpDevice -PresentOnly | Where-Object { 
        $_.InstanceId -like "*VID_22D9*" -or $_.FriendlyName -like "*OPPO*" -or $_.FriendlyName -like "*ADB*" 
    } | Select-Object Status, Class, FriendlyName, InstanceId
    
    if ($devices) {
        $devices | Format-Table -AutoSize | Out-String
    } else {
        "NO_DEVICE_FOUND"
    }
    """
    try:
        proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True, timeout=10)
        output = proc.stdout.strip()
        if "NO_DEVICE_FOUND" in output or not output:
            print("[-] USB Status: OPPO A78 5G is currently NOT detected on USB.")
            print("    💡 Solution: Connect phone to laptop via USB cable, pull down notification bar, and select 'File Transfer' / 'MTP'.")
            return False, None
        else:
            print("[+] USB Status: OPPO Device Detected!")
            print(output)
            return True, output
    except Exception as e:
        print(f"[!] Error checking USB: {e}")
        return False, None

def check_wifi_network():
    print("\n" + "=" * 60)
    print("📶 2. CHECKING LOCAL WI-FI NETWORK STATUS")
    print("=" * 60)
    
    ps_wifi = """
    Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "*Wi-Fi*", "*Wireless*" -ErrorAction SilentlyContinue | 
        Select-Object IPAddress, InterfaceAlias, PrefixOrigin | 
        Format-Table -AutoSize | Out-String
    """
    try:
        proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_wifi], capture_output=True, text=True, timeout=10)
        output = proc.stdout.strip()
        if output:
            print("[+] Laptop Local Wi-Fi IP:")
            print(output)
            return True
        else:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            print(f"[+] Hostname: {hostname} | Detected IP: {ip}")
            return True
    except Exception as e:
        print(f"[!] Error checking Wi-Fi: {e}")
        return False

def check_adb_ports():
    print("\n" + "=" * 60)
    print("🔍 3. CHECKING ADB SERVICE & WIRELESS PORT 5555")
    print("=" * 60)
    
    ps_ports = """
    Get-NetTCPConnection -State Listen -LocalPort 5555, 8022 -ErrorAction SilentlyContinue | 
        Select-Object LocalAddress, LocalPort, State | 
        Format-Table -AutoSize | Out-String
    """
    try:
        proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_ports], capture_output=True, text=True, timeout=10)
        output = proc.stdout.strip()
        if output:
            print("[+] Active Mobile Bridge Listeners:")
            print(output)
        else:
            print("[-] No active listeners on port 5555 (Wireless ADB) or 8022 (Termux SSH) right now.")
    except Exception as e:
        print(f"[!] Error checking ports: {e}")

if __name__ == "__main__":
    check_usb_devices()
    check_wifi_network()
    check_adb_ports()
