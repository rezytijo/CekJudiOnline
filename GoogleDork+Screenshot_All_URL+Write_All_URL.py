import asyncio
from playwright.async_api import async_playwright
import re
from datetime import datetime

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        domain = input("Masukkan subdomain: ")
        query = f"site:{domain} intext:'Judi Slot'"
        search_url = f"https://www.google.com/search?q={query}"
        
        await page.goto(search_url)
        
        page_index = 1
        date_str = datetime.now().strftime("%d-%m-%Y")
        output_file = f"{date_str}_URL_Slot.txt"
        
        while True:
            await page.wait_for_timeout(10000)  # Tunggu 10 detik sebelum mengambil screenshot
            await page.screenshot(path=f'screenshot_{domain}_page_{page_index}.png', full_page=True)
            
            # Ambil semua URL di halaman hasil pencarian
            urls = await page.query_selector_all('a[href]')
            for i, url in enumerate(urls):
                href = await url.get_attribute('href')
                if href and domain in href and "google" not in href:
                    # Buka URL di tab baru
                    new_page = await context.new_page()
                    try:
                        await new_page.goto(href)
                        await new_page.wait_for_timeout(5000)  # Tunggu 5 detik sebelum mengambil screenshot
                        # Ambil screenshot dari halaman yang dikunjungi
                        sanitized_url = re.sub(r'[^\w\-_\.]', '_', href)  # Sanitasi nama file
                        await new_page.screenshot(path=f'{sanitized_url}.png', full_page=True)
                        # Tulis URL ke file teks
                        with open(output_file, 'a') as file:
                            file.write(f"{href}\n")
                    except Exception as e:
                        print(f"Gagal membuka {href}: {e}")
                    finally:
                        await new_page.close()
            
            next_button = await page.query_selector('a#pnnext')
            if not next_button:
                break
            await next_button.click()
            await page.wait_for_timeout(2000)  # Tunggu beberapa detik untuk memuat halaman berikutnya
            page_index += 1
        
        await browser.close()

asyncio.run(main())