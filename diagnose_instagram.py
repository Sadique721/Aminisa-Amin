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

async def inspect_instagram_page():
    print("[*] Launching Chrome context to inspect Instagram DOM...")
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
        await page.wait_for_timeout(4000)
        
        print(f"[+] Loaded URL: {page.url}")
        print(f"[+] Page Title: {await page.title()}")
        
        # Save screenshot
        await page.screenshot(path="instagram_inspect.png")
        print("[+] Screenshot saved to instagram_inspect.png")
        
        # Get all inputs
        inputs = await page.eval_on_selector_all("input", "elements => elements.map(e => ({name: e.name, type: e.type, placeholder: e.placeholder, id: e.id, aria: e.getAttribute('aria-label')}))")
        print(f"[+] Found {len(inputs)} input elements: {inputs}")
        
        # Get all buttons
        buttons = await page.eval_on_selector_all("button, div[role='button'], a", "elements => elements.map(e => e.innerText.trim()).filter(t => t.length > 0 && t.length < 30)")
        print(f"[+] Found button/link texts (sample): {buttons[:20]}")
        
        # Save page HTML
        content = await page.content()
        with open("instagram_dom.html", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Saved HTML to instagram_dom.html ({len(content):,} chars)")
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(inspect_instagram_page())
