import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        domain = input("Masukkan subdomain: ")
        query = f"site:*{domain} Judi Slot"
        search_url = f"https://www.google.com/search?q={query}"
        
        await page.goto(search_url)
        
        page_index = 1
        while True:
            await page.screenshot(path=f'screenshot_{domain[1:]}_page_{page_index}.png', full_page=True)
            next_button = await page.query_selector('a#pnnext')
            if not next_button:
                break
            await next_button.click()
            await page.wait_for_timeout(2000)  # Tunggu beberapa detik untuk memuat halaman berikutnya
            page_index += 1
        
        await browser.close()

asyncio.run(main())