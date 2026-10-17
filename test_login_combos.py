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

PAIRS_TO_TEST = [
    ("mdsadiqueamin721721@gmail.com", "Md Sadique AminAI@Creator2026!"),
    ("mdsadiqueamin721721@gmail.com", "Md Sadique AminCreator@2026"),
    ("md_sadique_amin.official", "Md Sadique AminCreator@2026")
]

async def test_combos():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        for user, pwd in PAIRS_TO_TEST:
            print(f"[*] Testing: {user} / {pwd[:4]}*** ...")
            await page.goto("https://www.instagram.com/", timeout=60000)
            await page.wait_for_timeout(2000)
            
            email_inp = page.locator("input[name='email']")
            pass_inp = page.locator("input[name='pass']")
            
            if await email_inp.count() > 0:
                await email_inp.first.fill(user)
                await pass_inp.first.fill(pwd)
                submit_btn = page.locator("input[type='submit'], div[role='button']:has-text('Log in'), button:has-text('Log in')")
                await submit_btn.first.click()
                await page.wait_for_timeout(5000)
                
                # Check URL
                print(f"    -> Current URL: {page.url}")
                if "login" not in page.url:
                    error_el = page.locator("div[role='alert'], #slfErrorAlert, p:has-text('incorrect')")
                    if await error_el.count() == 0:
                        print(f"[✓] LOGIN SUCCESSFUL WITH: {user} / {pwd}")
                        await page.screenshot(path="login_success.png")
                        await context.close()
                        return True
            await page.wait_for_timeout(1000)
            
        print("[-] None of the tested email/password combinations passed automatically.")
        await context.close()
        return False

if __name__ == "__main__":
    asyncio.run(test_combos())
