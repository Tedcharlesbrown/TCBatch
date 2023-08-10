import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import aiohttp

import ftplib
from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm
import webbrowser
from urllib.parse import urljoin

from constants import *
import constants

from questions import ask_select
from questions import print_error

from fuzzywuzzy import fuzz

def check_already_downloaded(app_list: list) -> list:
	downloaded_files = os.listdir(constants.DOWNLOAD_FOLDER_PATH)
	return_list = []

	for app in app_list:
		app_found = False
		for file in downloaded_files:
			check_app = app.lower()  # Assuming app is the name you want to compare
			check_file = file.lower()[:len(file)-4] #slice the exstension
			check_file = file.lower()[:len(check_app)] #slice anything past the length of the stored file name
			check_fuzz = fuzz.ratio(check_file, check_app)
			# print(check_file, check_app, check_fuzz)
			
			# If a match is found, break out of the inner loop
			if check_fuzz > 75:
				app_found = True
				print(f"{app.upper()} ALREADY DOWNLOADED")
				break
		
		# If app wasn't found in downloaded_files, add it to the return_list
		if not app_found:
			return_list.append(app)

	return return_list  # returning the list of apps that were not found


def download_from_archive(file_to_search: str, verbose: bool):
	if verbose:
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

		if not verbose: #IF GETTING APPLICATION LIST
			path = UTILITY_FOLDER_PATH
		else:
			path = constants.DOWNLOAD_FOLDER_PATH

		# Download the file
		with open(path + file_to_download, 'wb') as f:
			if verbose: 
				print(f"FOUND {file_to_download} FROM ARCHIVE, PLEASE WAIT")
			file_size = ftp.size(file_to_download)
			progress = tqdm(total=file_size, unit='B', unit_scale=True)
			def progress_callback(data):
				progress.update(len(data))
				f.write(data)
			ftp.retrbinary(f'RETR {file_to_download}', progress_callback)
			progress.close()
			if verbose:
				print("DOWNLOAD COMPLETE")

	else:
		print("NOT IN ARCHIVE")

	if verbose:
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
			progress = async_tqdm(total=total_size, unit='B', unit_scale=True, desc=f'DOWNLOADING {filename}')

			with open(constants.DOWNLOAD_FOLDER_PATH + filename, 'wb') as f:
				async for data in response.content.iter_any():
					f.write(data)
					progress.update(len(data))

			progress.close()

	# print("Download complete")

async def find_file_from_website(url: str):
	try:
		html = await get_page_html(url)
		download_link = parse_html_for_link(url, html)
		if download_link is not None:
			await download_from_web(download_link)
			return True
		else:
			print(f"No download link found on {url}")
			return None
		
	except:
		print(f"Could not parse {url}")
		return None


# async def get_download(app_list: list):
# 	if len(app_list) == 0:
# 		print_error("NO OPTIONS SELECTED, SELECT OPTIONS WITH <space>")
		
# 	download_tasks = []
# 	archived_apps = []

# 	for i, app in enumerate(constants.APPLICATION_DOWNLOAD_LIST):
# 		for selected in app_list:
# 			if selected in app.display:
# 				app = constants.APPLICATION_DOWNLOAD_LIST[i]

# 				if i != len(constants.APPLICATION_DOWNLOAD_LIST) - 1:

# 					if app.link == "Archive":
# 						archived_apps.append(app.display)
# 						app_list.remove(selected)
# 					else:
# 						# print(f"DOWNLOADING: {app.display}")
# 						download_tasks.append(find_file_from_website(app.link))
# 				else:
# 					print("PASSWORD: TCB ADDRESS (numbers only)")
# 					webbrowser.open("http://gofile.me/70auI/6qt31duqE", new=0, autoraise=True)

# 	# execute all tasks concurrently
# 	results = (await asyncio.gather(*download_tasks, return_exceptions=True))
# 	for result, app in zip(results, app_list):
# 		if result is None:
# 			# print(app_list)
# 			# print(results)
# 			# print(f"ADDING TO ARCHIVE {app}")
# 			archived_apps.append(app)
# 	return archived_apps

# ------------------------------ TIMEOUT VERSION ----------------------------- #
async def get_download(app_list: list):
    if len(app_list) == 0:
        print_error("NO OPTIONS SELECTED, SELECT OPTIONS WITH <space>")

    download_tasks = []
    archived_apps = []

    for i, app in enumerate(constants.APPLICATION_DOWNLOAD_LIST):
        for selected in app_list:
            if selected in app.display:
                app = constants.APPLICATION_DOWNLOAD_LIST[i]

                if i != len(constants.APPLICATION_DOWNLOAD_LIST) - 1:

                    if app.link == "Archive":
                        archived_apps.append(app.display)
                        app_list.remove(selected)
                    else:
                        # Define a timeout duration (e.g., 10 seconds)
                        TIMEOUT_DURATION = 5

                        # Wrap the download task with a timeout
                        task = asyncio.wait_for(find_file_from_website(app.link), TIMEOUT_DURATION)
                        download_tasks.append(task)

                else:
                    print("PASSWORD: TCB ADDRESS (numbers only)")
                    webbrowser.open("http://gofile.me/70auI/6qt31duqE", new=0, autoraise=True)

    # Execute all tasks concurrently
    results = []
    for task in download_tasks:
        try:
            result = await task
            results.append(result)
        except asyncio.TimeoutError:
            # If there's a timeout, append None to results (or any sentinel value you prefer)
            results.append(None)

    for result, app in zip(results, app_list):
        if result is None:
            archived_apps.append(app)

    return archived_apps


def get_archive(app_list: list):
	if len(app_list) > 0:
		for i, app in enumerate(constants.APPLICATION_DOWNLOAD_LIST):
			for selected in app_list:
				if selected in app.display:
					# print(selected)
					app = constants.APPLICATION_DOWNLOAD_LIST[i]

					if i != len(constants.APPLICATION_DOWNLOAD_LIST) - 1:

						# if app.link == "Archive":
						print(f"DOWNLOADING: {app.display}")
						download_from_archive(app.name, True)
