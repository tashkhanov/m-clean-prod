"""
Use a headless browser to intercept ReviewLab API calls and extract reviews data.
"""
import asyncio
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.async_api import async_playwright

all_requests = []
all_reviews = []

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Intercept all network requests
        async def handle_response(response):
            url = response.url
            if 'reviewlab' in url or 'review' in url.lower():
                print(f"ReviewLab request: {url}")
                try:
                    data = await response.json()
                    with open('scratch/reviewlab_response.json', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'url': url, 'data': data}, ensure_ascii=False) + '\n')
                    print(f"  -> JSON captured, {len(str(data))} chars")
                except:
                    try:
                        text = await response.text()
                        if len(text) > 50:
                            print(f"  -> Text response ({len(text)} chars): {text[:200]}")
                    except:
                        pass

        page.on('response', handle_response)
        
        print("Navigating...")
        await page.goto('https://m-clean.kz/otzyvy/', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(5000)
        
        # Try clicking load more buttons
        print("Trying to click load more buttons...")
        for attempt in range(5):
            found_btn = False
            btns = await page.locator("button, a").all()
            for btn in btns:
                try:
                    if await btn.is_visible(timeout=500):
                        text = (await btn.inner_text()).lower()
                        if any(w in text for w in ['ещё', 'еще', 'more', 'show', 'загрузить', 'показать']):
                            await btn.click()
                            print(f"  Clicked: '{text[:40]}'")
                            found_btn = True
                            await page.wait_for_timeout(2000)
                except:
                    pass
            if not found_btn:
                print(f"  No more buttons found on attempt {attempt+1}")
                break

        # Save the fully rendered page
        content = await page.content()
        with open('scratch/rendered_reviews.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Saved rendered_reviews.html")
        
        await browser.close()

asyncio.run(main())
