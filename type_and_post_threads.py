import subprocess
import time

THREAD_TEXT = (
    "Hello everyone! Main hoon Md Sadique Amin. Welcome to my official Threads space! "
    "Here to share future tech, couture fashion elegance, and next-gen AI creativity. "
    "What trends are you exploring today? "
    "#Md Sadique Amin #AICreator #VirtualInfluencer"
)

def post_to_threads():
    print("[*] Typing first official thread into Threads app...")
    words = THREAD_TEXT.split(" ")
    chunk = []
    for word in words:
        clean = word.replace("'", "").replace('"', '').replace('&', 'and').replace('#', '\\#')
        chunk.append(clean)
        if len(chunk) >= 4:
            subprocess.run(["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", f"input text {'%s'.join(chunk)}%s"], check=False)
            chunk = []
            time.sleep(0.1)
    if chunk:
        subprocess.run(["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", f"input text {'%s'.join(chunk)}"], check=False)
        
    time.sleep(1)
    # Dismiss keyboard
    subprocess.run(["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", "input", "keyevent", "4"], check=False)
    time.sleep(1)
    
    # Dump UI to get exact Post button
    subprocess.run(["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", "uiautomator dump /sdcard/threads_post_ui.xml"], check=False)
    subprocess.run(["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "pull", "/sdcard/threads_post_ui.xml", "phone_threads_post_ui.xml"], check=False)

if __name__ == "__main__":
    post_to_threads()
