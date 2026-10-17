"""
YouTube Create Mobile Driver for Md Sadique Amin
=========================================
Controls YouTube Create app (com.google.android.apps.youtube.producer)
directly from Termux via local ADB bridge.

Implements the 2-Step Generation Workflow:
STEP 1: Generate Md Sadique Amin Image with Locked Face Biometrics + Dynamic Attire/Setting
STEP 2: Generate Video from Image using Command Prompt/Script
"""

import time
import os
from adb_bridge import bridge
from config import YT_CREATE_COORDS, PACKAGES

class YouTubeCreateDriver:
    def __init__(self):
        self.pkg = PACKAGES["youtube_create"]
        self.activity = ".application.MainActivity"

    def launch(self):
        """Wake phone and open YouTube Create."""
        bridge.wake_screen()
        time.sleep(1)
        out, err, code = bridge.launch_app(self.pkg, self.activity)
        time.sleep(3)
        return code == 0

    def step1_generate_image(self, image_prompt):
        """Step 1: Opens Generate image, enters prompt, submits generation."""
        print("[*] [YouTube Create] STEP 1: Starting Md Sadique Amin Image Generation...")
        self.launch()
        
        # Tap Generate Image button (537, 669)
        coord = YT_CREATE_COORDS["generate_image_btn"]
        bridge.tap(coord[0], coord[1])
        time.sleep(2)

        # Tap prompt input field (360, 500)
        inp = YT_CREATE_COORDS["prompt_input"]
        bridge.tap(inp[0], inp[1])
        time.sleep(1)

        # Type the biometrics-locked Image prompt
        print(f"[*] [YouTube Create] Typing Md Sadique Amin Image Prompt ({len(image_prompt)} chars)...")
        bridge.type_text(image_prompt)
        time.sleep(2)

        # Tap Generate submit button (643, 906)
        btn = YT_CREATE_COORDS["generate_submit_btn"]
        bridge.tap(btn[0], btn[1])
        print("[+] [YouTube Create] Image generation submitted!")
        
        # Wait for image options to render
        time.sleep(25)
        
        # Take verification screenshot of generated images
        shot_path = f"/sdcard/DCIM/Md Sadique Amin/yt_generated_image_{int(time.time())}.png"
        bridge.take_screenshot(shot_path)
        print(f"[+] Image step proof: {shot_path}")
        return shot_path

    def step2_generate_video_from_image(self, video_prompt):
        """Step 2: Animate / Generate video from image using command prompt."""
        print("[*] [YouTube Create] STEP 2: Creating Video from Generated Image...")
        
        # Select first generated image variant (usually upper-left grid coordinate)
        bridge.tap(200, 400)
        time.sleep(2)
        
        # If prompt for motion/animation appears, type video prompt
        if video_prompt:
            print(f"[*] [YouTube Create] Applying Video Prompt: {video_prompt[:60]}...")
            # Tap input if available or trigger video action
            bridge.tap(360, 500)
            time.sleep(1)
            bridge.type_text(video_prompt)
            time.sleep(1)
            # Submit video creation
            btn = YT_CREATE_COORDS["generate_submit_btn"]
            bridge.tap(btn[0], btn[1])
            
        print("[*] Waiting for video render...")
        time.sleep(30)
        
        vid_shot = f"/sdcard/DCIM/Md Sadique Amin/yt_generated_video_{int(time.time())}.png"
        bridge.take_screenshot(vid_shot)
        print(f"[+] Video step proof: {vid_shot}")
        
        # Return to home
        bridge.press_key(3)
        return vid_shot

    def run_full_two_step_cycle(self, image_prompt, video_prompt):
        """Executes full Step 1 (Image) followed by Step 2 (Video)."""
        img_proof = self.step1_generate_image(image_prompt)
        vid_proof = self.step2_generate_video_from_image(video_prompt)
        return {
            "image_proof": img_proof,
            "video_proof": vid_proof
        }

    def run_generation_cycle(self, prompt_text, mode="image"):
        """Backwards compatibility wrapper."""
        return self.step1_generate_image(prompt_text)

yt_driver = YouTubeCreateDriver()
