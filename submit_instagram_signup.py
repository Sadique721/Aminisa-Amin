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

PROFILE_DIR = os.path.abspath("config/chrome_user_data")
EMAIL = "mdsadiqueamin721721@gmail.com"
PASSWORD = "Md Sadique AminAI@Creator2026!"
FULL_NAME = "Md Sadique Amin Amin"
USERNAME = "md_sadique_amin.official"

async def fill_and_submit_signup():
    print("[*] Launching Chrome to complete Instagram signup...")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 950})
        
        print("[*] Loading https://www.instagram.com/accounts/emailsignup/ ...")
        await page.goto("https://www.instagram.com/accounts/emailsignup/", timeout=60000)
        await page.wait_for_timeout(3000)
        
        inputs = page.locator("input")
        input_count = await inputs.count()
        print(f"[+] Found {input_count} input elements on signup form.")
        
        if input_count >= 4:
            # 1. Mobile number or email (index 0)
            print("[*] Filling Mobile number or email...")
            await inputs.nth(0).fill(EMAIL)
            await page.wait_for_timeout(500)
            
            # 2. Password (index 1)
            print("[*] Filling Password...")
            await inputs.nth(1).fill(PASSWORD)
            await page.wait_for_timeout(500)
            
            # 3. Birthday
            selects = page.locator("select")
            if await selects.count() >= 3:
                print("[*] Selecting Birthday: August 15, 2002...")
                # Month: index 0
                await selects.nth(0).select_option(index=7)  # August (0-indexed or value 8)
                await page.wait_for_timeout(300)
                # Day: index 1
                await selects.nth(1).select_option(value="15")
                await page.wait_for_timeout(300)
                # Year: index 2
                await selects.nth(2).select_option(value="2002")
                await page.wait_for_timeout(500)
                
            # 4. Full name (index 2)
            print("[*] Filling Full name...")
            await inputs.nth(2).fill(FULL_NAME)
            await page.wait_for_timeout(500)
            
            # 5. Username (index 3)
            print("[*] Filling Username...")
            await inputs.nth(3).fill(USERNAME)
            await page.wait_for_timeout(2000)
            
            await page.screenshot(path="signup_filled_ready.png")
            print("[+] Screenshot saved to signup_filled_ready.png")
            
            # 6. Click Submit
            submit_btn = page.locator("button:has-text('Submit'), div[role='button']:has-text('Submit'), input[type='submit']")
            if await submit_btn.count() > 0:
                print("[*] Clicking Submit button...")
                await submit_btn.first.click()
                print("[*] Clicked Submit! Waiting for verification code screen or redirect...")
                await page.wait_for_timeout(8000)
                
                print(f"[+] Post-Submit URL: {page.url}")
                await page.screenshot(path="signup_after_submit.png")
                print("[+] Saved screenshot to signup_after_submit.png")
                
                body_text = await page.inner_text("body")
                lines = [l.strip() for l in body_text.split("\n") if l.strip() and len(l.strip()) < 80]
                print("\n[+] SCREEN TEXT SUMMARY AFTER SUBMIT:")
                for line in lines[:15]:
                    print(f"    - {line}")
            else:
                print("[-] Submit button not found.")
        else:
            print("[-] Less than 4 inputs found.")
            
        await context.close()

if __name__ == "__main__":
    asyncio.run(fill_and_submit_signup())
