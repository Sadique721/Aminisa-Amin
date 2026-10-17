import socket
import concurrent.futures

IPS = [
    f"192.168.1.{i}" for i in [3, 4, 12, 18, 19, 20, 24, 26, 27, 29, 30, 33, 34, 35, 40, 42, 44, 45, 47, 64, 76, 107]
]
PORTS = [8022, 5555, 8080]

def check(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.6)
    try:
        if s.connect_ex((ip, port)) == 0:
            return ip, port
    except Exception:
        pass
    finally:
        s.close()
    return None

def scan():
    print("[*] Scanning local network for Mobile Termux (8022) / ADB (5555)...")
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(check, ip, port) for ip in IPS for port in PORTS]
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            if res:
                print(f"[+] FOUND OPEN SERVICE: {res[0]}:{res[1]}")
                found.append(res)
    if not found:
        print("[-] No open Termux SSH (8022) or ADB (5555) detected on local IPs.")
    return found

if __name__ == "__main__":
    scan()
