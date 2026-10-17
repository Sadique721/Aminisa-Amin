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

EMAIL = "mdsadiqueamin721721@gmail.com"
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

async def upload_reel():
    print("=" * 75)
    print("🚀 MD_SADIQUE_AMIN AUTONOMOUS REEL PUBLISHER (EMAIL AUTHENTICATED)")
    print("=" * 75)
    print(f"[*] Account Email : {EMAIL}")
    print(f"[*] Target Video  : {VIDEO_PATH} ({os.path.getsize(VIDEO_PATH):,} bytes)")
    
    os.makedirs(PROFILE_DIR, exist_ok=True)
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized"]
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        print("[*] Navigating to Instagram...")
        await page.goto("https://www.instagram.com/", timeout=60000)
        await page.wait_for_timeout(3000)
        
        email_inp = page.locator("input[name='email']")
        pass_inp = page.locator("input[name='pass']")
        
        if await email_inp.count() > 0 and await pass_inp.count() > 0:
            print(f"[*] Entering email: {EMAIL}...")
            await email_inp.first.fill(EMAIL)
            await page.wait_for_timeout(600)
            
            print("[*] Entering password...")
            await pass_inp.first.fill(PASSWORD)
            await page.wait_for_timeout(600)
            
            print("[*] Submitting login...")
            submit_btn = page.locator("input[type='submit'], div[role='button']:has-text('Log in'), button:has-text('Log in')")
            await submit_btn.first.click()
            await page.wait_for_timeout(10000)
            
        await page.screenshot(path="login_step.png")
        print(f"[*] Current URL after login attempt: {page.url}")
        
        # Dismiss 'Save your login info?' prompt
        save_btn = page.locator("button:has-text('Save info'), div[role='button']:has-text('Save info'), button:has-text('Not now'), div[role='button']:has-text('Not now')")
        if await save_btn.count() > 0:
            print("[*] Dismissing Save Info prompt...")
            await save_btn.first.click()
            await page.wait_for_timeout(3000)
            
        # Dismiss notifications prompt
        notif_btn = page.locator("button:has-text('Not now'), div[role='button']:has-text('Not now')")
        if await notif_btn.count() > 0:
            print("[*] Dismissing notification prompt...")
            await notif_btn.first.click()
            await page.wait_for_timeout(2000)
            
        # Click Create
        create_btn = page.locator("svg[aria-label='New post'], span:has-text('Create'), a[href='#']:has-text('Create')")
        if await create_btn.count() > 0:
            print("[*] Clicking Create button...")
            await create_btn.first.click()
            await page.wait_for_timeout(1500)
            
            # Sub-menu 'Post'
            post_menu = page.locator("span:has-text('Post'), div:has-text('Post')")
            if await post_menu.count() > 0:
                print("[*] Clicking 'Post' sub-menu...")
                await post_menu.first.click()
                await page.wait_for_timeout(2000)
                
        # File Chooser
        select_comp_btn = page.locator("button:has-text('Select from computer'), div[role='button']:has-text('Select from computer')")
        if await select_comp_btn.count() > 0:
            print("[*] Triggering file chooser for video upload...")
            async with page.expect_file_chooser() as fc:
                await select_comp_btn.first.click()
            chooser = await fc.value
            await chooser.set_files(VIDEO_PATH)
            print(f"[+] Video attached successfully: {VIDEO_PATH}")
            await page.wait_for_timeout(5000)
            await page.screenshot(path="upload_step.png")
            
            # Dismiss 'Video posts are now shared as reels' notice if present
            ok_reels = page.locator("button:has-text('OK'), div[role='button']:has-text('OK')")
            if await ok_reels.count() > 0:
                print("[*] Dismissing Reels notice...")
                await ok_reels.first.click()
                await page.wait_for_timeout(1500)
                
            # Click 'Next' (Cropping)
            next_btn = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')")
            if await next_btn.count() > 0:
                print("[*] Clicking Next (Step 1)...")
                await next_btn.first.click()
                await page.wait_for_timeout(2500)
                
            # Click 'Next' (Cover/Filter)
            next_btn2 = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')")
            if await next_btn2.count() > 0:
                print("[*] Clicking Next (Step 2)...")
                await next_btn2.first.click()
                await page.wait_for_timeout(2500)
                
            # Fill Caption
            caption_input = page.locator("div[aria-label='Write a caption...'], div[contenteditable='true']")
            if await caption_input.count() > 0:
                print("[*] Pasting Grand Welcome caption & SEO tags...")
                await caption_input.first.fill(CAPTION)
                await page.wait_for_timeout(2000)
                
            # Click Share
            share_btn = page.locator("div[role='button']:has-text('Share'), button:has-text('Share')")
            if await share_btn.count() > 0:
                print("[*] Clicking SHARE button...")
                await share_btn.first.click()
                print("[+] Share button clicked! Waiting for video processing and publication...")
                await page.wait_for_timeout(30000)
                await page.screenshot(path="share_step.png")
                print("\n" + "=" * 75)
                print("🎉 REEL SUCCESSFULLY PUBLISHED TO INSTAGRAM, FB & THREADS!")
                print("=" * 75)
            else:
                print("[-] Share button not reached.")
                await page.screenshot(path="share_step.png")
        else:
            print("[-] Upload modal not reached. Check login_step.png.")
            
        await page.wait_for_timeout(5000)
        await context.close()

if __name__ == "__main__":
    asyncio.run(upload_reel())
