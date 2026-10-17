import subprocess
import time

CAPTION = (
    "Hello everyone! Main hoon Md Sadique Amin. Welcome to the official Md Sadique Amin universe! "
    "Blending Indian heritage, couture elegance, and next-gen AI creativity. "
    "Drop your thoughts below! "
    "#Md Sadique Amin #AICreator #VirtualInfluencer #GrandWelcome #IndianHeritage #FashionTech"
)

def type_caption():
    print("[*] Typing Grand Debut caption and trending hashtags into Instagram...")
    words = CAPTION.split(" ")
    chunk = []
    for word in words:
        # replace special characters
        clean = word.replace("'", "").replace('"', '').replace('&', 'and')
        chunk.append(clean)
        if len(chunk) >= 4:
            cmd = ["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", f"input text {'%s'.join(chunk)}%s"]
            subprocess.run(cmd)
            chunk = []
            time.sleep(0.1)
    if chunk:
        cmd = ["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", f"input text {'%s'.join(chunk)}"]
        subprocess.run(cmd)
    print("[+] Caption typed successfully!")

if __name__ == "__main__":
    type_caption()
