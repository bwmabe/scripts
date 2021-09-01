import asyncio
import aiohttp
import sys
import os
from bs4 import BeautifulSoup


class Image():
    def __init__(self, tld, link, filename):
        self.filename = filename
        self.link = f"{tld}{link[1:]}"


async def get_images(thread_link, tld, output_directory=None):
    images = list()
    async with aiohttp.ClientSession() as session:
        async with session.get(thread_link) as thread:
            soup = BeautifulSoup(await thread.text(), 'html.parser')
            for a in soup.find_all('a', class_="originalNameLink"):
                images.append(Image(tld, a['href'], a['download']))
        for image in images:
            async with session.get(image.link) as image_response:
                if output_directory is not None:
                    try:
                        os.mkdir(output_directory)
                    except FileExistsError:
                        pass
                    except Exception as err:
                        print(f"mkdir: {err}")
                    filename = f"{output_directory}/{image.filename}"
                else:
                    filename = image.filename
                with open(filename, 'wb') as img_out:
                    print(f"Downloading '{filename}' from {image.link}...")
                    img_out.write(await image_response.read())


async def main(argv):
    if argv[1] == "help" or argv[1] == "-h":
        print("usage: lynxchan_media_downloader [thread_link] [directory]")
        print("specifying an output directory is optional")
        print("downloads all media from a thread on a site running the")
        print("'lynxchan' image board software")
        exit(0)
    thread_link = argv[1]
    tld = f"https://{thread_link.split('/')[2]}/"
    output_directory = None
    if len(argv) >= 3:
        output_directory = argv[2]
    await get_images(thread_link, tld, output_directory)


asyncio.run(main(sys.argv))
