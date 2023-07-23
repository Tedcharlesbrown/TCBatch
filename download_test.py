import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import aiohttp
from tqdm import tqdm

async def get_page_html(url: str):
    """Get page HTML, including content loaded via JavaScript."""
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    html = await page.content()
    await browser.close()
    return html

def parse_html_for_link(url: str, html: str):
    """Parse HTML to find download links."""
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', href=True):
        # Create absolute URL if necessary
        absolute_link = urljoin(url, link['href'])
        if ".exe" in absolute_link or ".msi" in absolute_link:
            return absolute_link
    return None

async def download_from_web(url: str):
    """Download a file from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            filename = url.split("/")[-1]
            total_size = int(response.headers.get('Content-Length', 0))

            with open(filename, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=f'Downloading {filename}') as pbar:
                    async for data in response.content.iter_any():
                        f.write(data)
                        pbar.update(len(data))

    print("Download complete")

async def download_file_from_website(url: str):
    html = await get_page_html(url)
    download_link = parse_html_for_link(url, html)
    if download_link is not None:
        await download_from_web(download_link)
    else:
        print(f"No download link found on {url}")

# Run the download function with the webpage URL
# 


# asyncio.run(download_file_from_website("https://www.lightjams.com/artnetominator/"))
# asyncio.run(download_file_from_website("https://learn.microsoft.com/en-us/sysinternals/downloads/bginfo"))
# asyncio.run(download_file_from_website("https://www.bulkrenameutility.co.uk/Download.php"))
# asyncio.run(download_file_from_website("https://www.opengear.tv/frame-and-control/control-system/download/"))
# asyncio.run(download_file_from_website("http://decimator.com/DOWNLOADS/DOWNLOADS.html"))
# asyncio.run(download_file_from_website("https://freefilesync.org/download.php"))
# asyncio.run(download_file_from_website("https://central.github.com/deployments/desktop/desktop/latest/win32"))
# asyncio.run(download_file_from_website("http://www.midiox.com/zip/midioxse.exe"))
# asyncio.run(download_file_from_website("https://www.myffmpeg.com/download.html"))
# asyncio.run(download_file_from_website("https://obsproject.com/download"))
# asyncio.run(download_file_from_website("https://builds.parsec.app/package/parsec-windows.exe"))
# asyncio.run(download_file_from_website("https://hexler.net/protokol#windows"))
# asyncio.run(download_file_from_website("https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"))
# asyncio.run(download_file_from_website("https://www.python.org/downloads/"))
# asyncio.run(download_file_from_website("https://www.realvnc.com/en/connect/download/viewer/windows/"))
# asyncio.run(download_file_from_website("https://www.reaper.fm/download.php"))
# asyncio.run(download_file_from_website("https://rufus.ie/en/"))
# asyncio.run(download_file_from_website("https://www.sublimetext.com/download_thanks?target=win-x64"))
# asyncio.run(download_file_from_website("https://pkgs.tailscale.com/stable/"))
# asyncio.run(download_file_from_website("https://www.tightvnc.com/download.php"))
# asyncio.run(download_file_from_website("https://www.vmix.com/software/download.aspx"))
# asyncio.run(download_file_from_website("https://www.wireshark.org/download.html"))
# asyncio.run(download_file_from_website("https://pixera.one/en/support/downloads"))


