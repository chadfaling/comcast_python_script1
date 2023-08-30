import asyncio
from pyppeteer import launch

async def scrape():
    browser = await launch(headless=True)
    page = await browser.newPage()
    
    await page.goto('https://palermo.viper.comcast.net/#ccvs/f0d16f89-d587-4d85-ad70-f0ffbe831452')
    
    # Wait for a few seconds to let the page load (you can adjust this duration)
    await asyncio.sleep(20)
    
    # Query elements by their class names
    elements = await page.querySelectorAll('form-grid')
    
    # Iterate over each element and extract data
    for element in elements:
        # Using page.evaluate to read the element properties
        element_content = await page.evaluate('(element) => element.textContent', element)
        print(f'Element content: {element_content.strip()}')

    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape())

