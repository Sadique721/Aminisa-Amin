import subprocess
import time

PROMPT = (
    "Cinematic 9:16 vertical video of Md Sadique Amin, 22-year-old elegant Indian female creator, "
    "fair wheatish skin, unblemished face with strictly zero moles, almond hazel-brown eyes, "
    "dark espresso wavy hair, wearing handcrafted cream-ivory Lucknowi Chikankari kurta with sheer dupatta, "
    "standing in modern South Mumbai art gallery courtyard with stone arches and sun-dappled plants, "
    "slow cinematic camera dolly-in, soft breeze moving hair, warm confident smile, 60fps photorealistic 4k"
)

# Convert prompt to ADB input text format (escape special characters and replace spaces with %s)
def send_text_to_device(text):
    # Split text into chunks so adb input text doesn't overflow buffer
    words = text.split(" ")
    chunk = []
    for word in words:
        clean_word = word.replace("'", "").replace('"', '').replace("&", "and")
        chunk.append(clean_word)
        if len(chunk) >= 5:
            cmd = ["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", f"input text {'%s'.join(chunk)}%s"]
            subprocess.run(cmd)
            chunk = []
            time.sleep(0.1)
    if chunk:
        cmd = ["C:\\platform-tools\\adb.exe", "-s", "WS9X6LLJXW7H7TFQ", "shell", f"input text {'%s'.join(chunk)}"]
        subprocess.run(cmd)

if __name__ == "__main__":
    print("[*] Sending Master Md Sadique Amin Prompt to YouTube Create AI Video Generator...")
    send_text_to_device(PROMPT)
    print("[+] Prompt typed successfully!")
