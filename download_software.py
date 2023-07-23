

import requests
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import aiohttp

import ftplib
from tqdm import tqdm
import webbrowser
from urllib.parse import urlparse
from urllib.parse import urljoin

from constants import *
from application_list import *

from questions import ask_select
from questions import print_error


def download_from_archive(file_to_search: str):
	print("DOWNLOADING FROM ARCHIVE")
	file_found = False

	try:
		ftp = ftplib.FTP("tedcharlesbrown.synology.me")
	except:
		ftp = ftplib.FTP("192.168.1.100")

	ftp.login("_FTP_", "tedcharlesbrown_ftp")
	# ftp.cwd("/Application_Installers")

	files = ftp.nlst()

	versions = []
	
	# m_versions = MENU_version("Download Versions", "MULTIPLE VERSIONS FOUND, WHICH VERSION TO DOWNLOAD")

	for file in files:
		if file.lower().replace("-", "").find(file_to_search.lower().replace("-", "")[:-4]) != -1:
			file_to_download = file
			file_found = True
			versions.append(file)

	if file_found:
		if len(versions) > 1:
			versions.reverse()
			file_to_download = ask_select("MULTIPLE VERSIONS FOUND",versions,False)

		# Download the file
		with open(UTILITY_FOLDER_PATH + file_to_download, 'wb') as f:
			print(f"FOUND {file_to_download} FROM ARCHIVE, PLEASE WAIT")
			file_size = ftp.size(file_to_download)
			progress = tqdm(total=file_size, unit='B', unit_scale=True)
			def progress_callback(data):
				progress.update(len(data))
				f.write(data)
			ftp.retrbinary(f'RETR {file_to_download}', progress_callback)
			progress.close()
			print("DOWNLOAD COMPLETE")

	else:
		print("NOT IN ARCHIVE")

	print(DIVIDER)
	ftp.quit()

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

            with open(UTILITY_FOLDER_PATH + filename, 'wb') as f:
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


def get_download(app_list: list):
	if len(app_list) == 0:
		print_error("NO OPTIONS SELECTED, SELECT OPTIONS WITH <space>")

	print(len(app_list))

	for i, app in enumerate(APPLICATION_DOWNLOAD_LIST):
		for selected in app_list:
			if selected in app.display:
				print(selected)
				app = APPLICATION_DOWNLOAD_LIST[i]

				if i != len(APPLICATION_DOWNLOAD_LIST) - 1:
					print(f"DOWNLOADING: {app.display}")

					if app.link == "Archive":
						download_from_archive(app.name)
					else:
						asyncio.run(download_file_from_website((app.link)))

				else:
					print("PASSWORD: TCB ADDRESS (numbers only)")
					webbrowser.open("http://gofile.me/70auI/6qt31duqE", new=0, autoraise=True)

		
def custom_download(link: str):
	if parse_html_for_link(link, False):
		response = requests.get(parse_html_for_link(link, True), stream=True)
		download_from_web(response, "custom.exe")
	else:
		print("COULD NOT FETCH DOWNLOAD")