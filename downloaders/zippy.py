import asyncio
import aiohttp
import urllib

from bs4 import BeautifulSoup

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Used to run Firefox geckodriver headlessly
options = Options()
options.add_argument("--headless")

zippy_links = """
put a zippyshare link on each line
"""


async def fetch_link(link, queue):
    link_prefix = '/'.join(link.split('/')[:3])
    with Firefox(options=options) as driver:
        print(f' --- Starting browser for {link}')
        driver.get(link)
        anchors = WebDriverWait(driver, 5).until(
                lambda page:
                page.find_elements_by_css_selector("a"))
        for anchor in anchors:
            if anchor.get_attribute('id') == "dlbutton":
                l = anchor.get_attribute('href')
                await queue.put(l)
        print(f' --- Closing browser for {link}')


async def download_file(link):
    filename = urllib.parse.unquote(link.split('/')[-1])
    print(f' --- Started Downloading: {filename}')
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            with open(filename, 'wb') as payload:
                payload.write(await response.read())
    print(f' --- Finished Downloading: {filename}')


async def main(links):
    download_queue = asyncio.Queue()
    fetch_workers = []
    download_workers = []
    print("Retriving download link(s) from landing page(s)...")
    for link in links:
        process = asyncio.create_task(fetch_link(link, download_queue))
        fetch_workers.append(process)
    await asyncio.gather(*fetch_workers)
    print("Done!")
    print("Downloading file(s)...")
    while not download_queue.empty():
        current_link = await download_queue.get()
        dl_worker = asyncio.create_task(download_file(current_link))
        await asyncio.gather(dl_worker)
    print("Done!")


asyncio.run(main(zippy_links.split()))
