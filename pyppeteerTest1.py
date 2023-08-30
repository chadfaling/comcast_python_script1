import asyncio
from pyppeteer import launch

async def scrape():
    browser = await launch(headless=True)
    page = await browser.newPage()
    
    await page.goto('https://palermo.viper.comcast.net/#ccvs/f0d16f89-d587-4d85-ad70-f0ffbe831452')
    
    # Optional: You may want to wait for some element to be loaded to ensure the webpage is ready.
    # await page.waitForSelector('some_selector')

    # wait for pre-determined time, 10 seconds
    #await page.waitForTimeout(10000)
    await asyncio.sleep(10)

    
    # Get the HTML content
    content = await page.content()
    print(content)
    
    # TODO: Identify which elements you want to scrape.
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape())

