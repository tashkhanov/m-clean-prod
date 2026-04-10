import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to https://m-clean.kz/otzyvy/...")
        await page.goto('https://m-clean.kz/otzyvy/', wait_until='networkidle')
        
        # Wait a bit for widgets to load
        await page.wait_for_timeout(3000)
        
        print("Clicking 'Ещё отзывы' buttons if they exist...")
        # ReviewLab buttons often have classes like .rl-btn, .rl-load-more, etc.
        # Or we can just find any button containing "Ещё" or "Показать"
        
        while True:
            # Find all buttons that might be load more
            buttons = await page.locator("button, a, div[role='button']").all()
            clicked_any = False
            for btn in buttons:
                try:
                    if await btn.is_visible():
                        text = await btn.inner_text()
                        if 'ещё' in text.lower() or 'еще' in text.lower() or 'показать' in text.lower():
                            await btn.click()
                            print(f"Clicked button with text: {text}")
                            clicked_any = True
                            await page.wait_for_timeout(2000)
                except:
                    pass
            
            if not clicked_any:
                break
                
        print("Extracting HTML...")
        html = await page.content()
        with open('scratch/scraped_reviews.html', 'w', encoding='utf-8') as f:
            f.write(html)
            
        print("Saved to scratch/scraped_reviews.html")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
