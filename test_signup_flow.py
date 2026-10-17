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

async def test_signup_status():
    print("[*] Launching Chrome context to test signup/registration state...")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        print("[*] Navigating to https://www.instagram.com/accounts/emailsignup/ ...")
        await page.goto("https://www.instagram.com/accounts/emailsignup/", timeout=60000)
        await page.wait_for_timeout(3000)
        
        # Check inputs on signup page
        inputs = await page.eval_on_selector_all("input", "elements => elements.map(e => e.name)")
        print(f"[+] Found input names on signup page: {inputs}")
        
        # Fill email
        email_field = page.locator("input[name='emailOrPhone'], input[name='email']")
        if await email_field.count() > 0:
            await email_field.first.fill(EMAIL)
            print("[+] Filled email: " + EMAIL)
            
        # Fill password
        pass_field = page.locator("input[name='password'], input[name='pass']")
        if await pass_field.count() > 0:
            await pass_field.first.fill(PASSWORD)
            print("[+] Filled password")
            
        # Fill Full Name
        name_field = page.locator("input[name='fullName']")
        if await name_field.count() > 0:
            await name_field.first.fill(FULL_NAME)
            print("[+] Filled full name: " + FULL_NAME)
            
        # Fill Username
        user_field = page.locator("input[name='username']")
        if await user_field.count() > 0:
            await user_field.first.fill(USERNAME)
            print("[+] Filled username: " + USERNAME)
            await page.wait_for_timeout(2000)
            
        await page.screenshot(path="signup_filled_state.png")
        print("[+] Screenshot saved to signup_filled_state.png")
        
        # Check if username or email shows error or checkmark
        alerts = await page.eval_on_selector_all("span[aria-label], div[role='alert'], p", "elements => elements.map(e => e.innerText.trim()).filter(t => t.length > 0 && t.length < 100)")
        print(f"[+] Page notices: {alerts[:10]}")
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(test_signup_status())
