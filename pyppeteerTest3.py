import asyncio
from pyppeteer import launch

async def scrape():
    browser = await launch(headless=True)
    page = await browser.newPage()
    
    await page.goto('https://palermo.viper.comcast.net/#ccvs/f0d16f89-d587-4d85-ad70-f0ffbe831452')
    
    # Wait for a few seconds to let the page load (you can adjust this duration)
    await asyncio.sleep(20)

    # Search for labels with the text "Name"
    labels = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('label')).filter(
            label => label.textContent.includes('Name')
        ).map(label => label.outerHTML)
    }''')

    # Print the result
    print(labels)
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape())

