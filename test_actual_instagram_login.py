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
USERNAME = "md_sadique_amin.official"
PASSWORD = "Md Sadique AminAI@Creator2026!"

async def do_login():
    print("[*] Launching Chrome context...")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=True,
            args=["--start-maximized"]
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        print("[*] Navigating to https://www.instagram.com/ ...")
        await page.goto("https://www.instagram.com/", timeout=60000)
        await page.wait_for_timeout(3000)
        
        # Check for email and pass inputs
        email_inp = page.locator("input[name='email']")
        pass_inp = page.locator("input[name='pass']")
        
        if await email_inp.count() > 0 and await pass_inp.count() > 0:
            print("[*] Found login fields: input[name='email'] and input[name='pass']")
            print(f"[*] Filling username: {USERNAME}...")
            await email_inp.first.fill(USERNAME)
            await page.wait_for_timeout(500)
            
            print("[*] Filling password...")
            await pass_inp.first.fill(PASSWORD)
            await page.wait_for_timeout(500)
            
            print("[*] Submitting login form...")
            # Click Log in button
            submit_btn = page.locator("input[type='submit'], div[role='button']:has-text('Log in'), button:has-text('Log in')")
            await submit_btn.first.click()
            
            print("[*] Form submitted! Waiting for response...")
            await page.wait_for_timeout(10000)
            
            print(f"[+] Post-login URL: {page.url}")
            print(f"[+] Post-login Title: {await page.title()}")
            await page.screenshot(path="post_login_result.png")
            print("[+] Saved post-login screenshot to post_login_result.png")
            
            # Check for error text if any
            error_el = page.locator("div[role='alert'], #slfErrorAlert, p:has-text('incorrect')")
            if await error_el.count() > 0:
                print(f"[-] Login alert message: {await error_el.first.inner_text()}")
        else:
            print("[+] Already logged in or different view!")
            await page.screenshot(path="post_login_result.png")
            
        await context.close()

if __name__ == "__main__":
    asyncio.run(do_login())
