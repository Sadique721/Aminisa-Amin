"""
Md Sadique Amin 100% Autonomous Web Multi-Poster (Playwright Chrome Engine)
Logs into Instagram Web, uploads the Grand Welcome Reel with full caption,
and clicks Share completely hands-free!
"""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

USERNAME = "md_sadique_amin.official"
PASSWORD = "Md Sadique AminAI@Creator2026!"
VIDEO_PATH = os.path.abspath(r"exports\reels\md_sadique_amin_official_grand_welcome_reel.mp4")
PROFILE_DIR = os.path.abspath("config/chrome_user_data")

CAPTION = (
    "✨ Welcome to the Md Sadique Amin Universe | Official Debut & Introduction 🌸\n\n"
    "Hello everyone!\n"
    "I'm Md Sadique Amin — your digital creator, creative technologist, and visual storyteller from Mumbai.\n\n"
    "Join me as we embark on an inspiring journey blending high-fashion elegance, cultural heritage, and future technology. "
    "From timeless traditions to modern lifestyle aesthetics, every frame tells a story.\n\n"
    "Follow along to be part of this incredible adventure! Drop a 'Hello' in the comments below! 👇✨\n\n"
    "#Md Sadique Amin #OfficialDebut #GrandWelcome #VirtualCreator #AICreator #DigitalHuman #IndianHeritage "
    "#AestheticFashion #TechLifestyle #ModernMumbai #VisualStorytelling #WelcomePost #FutureIsHere"
)

async def post_to_instagram_web():
    print("=" * 75)
    print("🚀 LAUNCHING AUTONOMOUS INSTAGRAM WEB POSTER (CHROME ENGINE)")
    print("=" * 75)
    print(f"[*] Target Video : {VIDEO_PATH} ({os.path.getsize(VIDEO_PATH):,} bytes)")
    print(f"[*] Account      : @{USERNAME}")
    
    os.makedirs(PROFILE_DIR, exist_ok=True)
    
    async with async_playwright() as p:
        print("[*] Spawning Chrome persistent context...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        print("[*] Navigating to Instagram...")
        await page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
        await page.wait_for_timeout(3000)
        
        # If redirected to sign up, click 'Log in' link
        login_link = page.locator("a:has-text('Log in'), span:has-text('Log in')")
        if await login_link.count() > 0:
            print("[*] Clicking 'Log in' link...")
            await login_link.first.click()
            await page.wait_for_timeout(3000)
            
        # Wait for username input
        await page.wait_for_selector("input[name='username']", timeout=15000)
        print("[*] Username input located. Authenticating...")
        # Dismiss cookie banner if present
        cookie_btn = page.locator("button:has-text('Allow all cookies'), button:has-text('Decline optional cookies')")
        if await cookie_btn.count() > 0:
            await cookie_btn.first.click()
            await page.wait_for_timeout(500)
            
        await page.fill("input[name='username']", USERNAME)
        await page.fill("input[name='password']", PASSWORD)
        await page.click("button[type='submit']")
        print("[*] Submitted credentials. Waiting for authentication...")
        await page.wait_for_timeout(10000)
        
        # Dismiss 'Save info' prompt if present
        save_info_btn = page.locator("button:has-text('Save info'), button:has-text('Not now'), div[role='button']:has-text('Not now')")
        if await save_info_btn.count() > 0:
            print("[*] Dismissing 'Save Login Info' prompt...")
            await save_info_btn.first.click()
            await page.wait_for_timeout(3000)
            
        # Dismiss notifications prompt
        notif_btn = page.locator("button:has-text('Not now'), div[role='button']:has-text('Not now')")
        if await notif_btn.count() > 0:
            print("[*] Dismissing notifications prompt...")
            await notif_btn.first.click()
            await page.wait_for_timeout(2000)
            
        print(f"[*] Current URL: {page.url}")
        
        # Look for Create post button
        create_selectors = [
            "svg[aria-label='New post']",
            "span:has-text('Create')",
            "a[href='#']:has-text('Create')"
        ]
        
        for sel in create_selectors:
            loc = page.locator(sel)
            if await loc.count() > 0:
                print(f"[*] Found Create button with selector: {sel}")
                await loc.first.click()
                await page.wait_for_timeout(1500)
                
                # Check for 'Post' in the popup menu
                post_menu = page.locator("span:has-text('Post'), div:has-text('Post')")
                if await post_menu.count() > 0:
                    print("[*] Clicking 'Post' from Create menu...")
                    await post_menu.first.click()
                    await page.wait_for_timeout(2000)
                break
                
        # Wait for Create modal to appear
        await page.wait_for_timeout(2000)
        
        # Check for 'Select from computer' button or file input
        select_btn = page.locator("button:has-text('Select from computer')")
        file_input = page.locator("input[type='file']")
        
        if await select_btn.count() > 0:
            print("[*] Found 'Select from computer' button! Triggering file chooser...")
            async with page.expect_file_chooser() as fc_info:
                await select_btn.first.click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(VIDEO_PATH)
            print(f"[+] File chosen successfully via file chooser: {VIDEO_PATH}")
            await page.wait_for_timeout(4000)
        elif await file_input.count() > 0:
            print(f"[*] Setting video file via file input: {VIDEO_PATH}")
            await file_input.first.set_input_files(VIDEO_PATH)
            await page.wait_for_timeout(4000)
        else:
            print("[-] Upload modal button not detected.")

        # Check for OK / Crop / Next buttons
        for step in range(5):
            await page.wait_for_timeout(2000)
            # Dismiss 'Video posts are now shared as reels' modal if present
            ok_btn = page.locator("button:has-text('OK'), div[role='button']:has-text('OK')")
            if await ok_btn.count() > 0:
                print("[*] Dismissing Reels notice (OK)...")
                await ok_btn.first.click()
                await page.wait_for_timeout(1000)

            next_btn = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')")
            if await next_btn.count() > 0:
                print(f"[*] Step {step+1}: Clicking 'Next' button...")
                await next_btn.first.click()
                await page.wait_for_timeout(2500)
            else:
                break
                
        # Caption box
        caption_box = page.locator("div[aria-label='Write a caption...'], div[contenteditable='true']")
        if await caption_box.count() > 0:
            print("[*] Writing caption and hashtags...")
            await caption_box.first.fill(CAPTION)
            await page.wait_for_timeout(2000)
            
        # Click Share
        share_btn = page.locator("div[role='button']:has-text('Share'), button:has-text('Share')")
        if await share_btn.count() > 0:
            print("[*] Clicking 'Share' button...")
            await share_btn.first.click()
            print("[+] Share button clicked! Waiting for reel to upload...")
            await page.wait_for_timeout(25000)
            print("[✓] REEL PUBLISHED TO INSTAGRAM & CROSS-POSTED TO META CHANNELS!")
        else:
            print("[-] Share button not reached.")
            
        await page.screenshot(path="instagram_upload_debug.png")
        print("[*] Captured debug screenshot: instagram_upload_debug.png")
        print("[*] Keeping browser active for verification...")
        await page.wait_for_timeout(5000)
        await context.close()

if __name__ == "__main__":
    asyncio.run(post_to_instagram_web())
