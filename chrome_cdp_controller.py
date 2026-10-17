"""
Md Sadique Amin Chrome CDP Live Controller
Connects to User's Active Chrome Browser via Port 9222 (Developer Debugging Mode)
Controls Facebook, Instagram, Threads, and YouTube directly within the user's active session.
"""

import time
import asyncio
from playwright.async_api import async_playwright

WEBSITE_URL = "https://www.instagram.com/md_sadique_amin.official/"
ADMIN_EMAIL = "mdsadiqueamin721721@gmail.com"
PORTRAIT_PATH = r"d:\current using file\1 social media automation handler file\md_sadique_amin-images\01_md_sadique_amin_clean_portrait_kurta.jpg"

async def automate_active_chrome():
    print("[*] Connecting to running Chrome on http://localhost:9222...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("[+] Successfully connected to Chrome via CDP!")
        except Exception as e:
            print(f"[-] Connection failed. Is Chrome running with --remote-debugging-port=9222? Error: {e}")
            return False

        context = browser.contexts[0]
        pages = context.pages
        print(f"[*] Found {len(pages)} open tabs in Chrome:")
        for idx, page in enumerate(pages):
            try:
                title = await page.title()
                url = page.url
                print(f"    Tab {idx+1}: {title} ({url})")
            except Exception:
                pass

        # 1. Automate Facebook Page Wizard if open
        fb_page = None
        for page in pages:
            if "facebook.com/pages/create" in page.url or "facebook.com" in page.url:
                fb_page = page
                break

        if fb_page:
            print("\n[*] Interacting with Facebook Page Creation Tab...")
            await fb_page.bring_to_front()
            await asyncio.sleep(1)

            # Try to fill Website field
            try:
                # Target Website input
                website_input = await fb_page.query_selector("input[aria-label*='Website' i], input[placeholder*='Website' i], label:has-text('Website') input")
                if not website_input:
                    # Generic input near 'Website'
                    website_input = await fb_page.query_selector("div:has-text('Website') ~ div input, input[type='text']")
                if website_input:
                    await website_input.fill(WEBSITE_URL)
                    print(f"[+] Filled Facebook Website: {WEBSITE_URL}")
            except Exception as e:
                print(f"[-] Could not fill Website: {e}")

            # Try to fill Email field
            try:
                email_input = await fb_page.query_selector("input[aria-label*='Email' i], input[type='email'], input[placeholder*='Email' i]")
                if email_input:
                    await email_input.fill(ADMIN_EMAIL)
                    print(f"[+] Filled Facebook Email: {ADMIN_EMAIL}")
            except Exception as e:
                print(f"[-] Could not fill Email: {e}")

            # Click Next button
            try:
                next_btn = await fb_page.query_selector("div[aria-label='Next' i][role='button'], button:has-text('Next')")
                if next_btn:
                    print("[+] Found 'Next' button on Facebook. Clicking...")
                    await next_btn.click()
                    await asyncio.sleep(2)
            except Exception as e:
                print(f"[-] Next button click note: {e}")

        # 2. Check YouTube Create Channel
        yt_page = None
        for page in pages:
            if "youtube.com/create_channel" in page.url:
                yt_page = page
                break

        if not yt_page:
            print("\n[*] Opening YouTube Create Channel in a new tab...")
            yt_page = await context.new_page()
            await yt_page.goto("https://www.youtube.com/create_channel")
            await asyncio.sleep(2)

        print("[*] Checking YouTube Create Channel page...")
        await yt_page.bring_to_front()
        try:
            create_btn = await yt_page.query_selector("button:has-text('Create channel'), ytd-button-renderer:has-text('Create channel')")
            if create_btn:
                print("[+] Found 'Create channel' button on YouTube! Clicking...")
                await create_btn.click()
                await asyncio.sleep(2)
                print("[+] Clicked 'Create channel' successfully!")
        except Exception as e:
            print(f"[-] YouTube interaction note: {e}")

        print("\n[+] Browser live interaction cycle complete!")
        return True

if __name__ == "__main__":
    asyncio.run(automate_active_chrome())
