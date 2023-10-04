from dataclasses import dataclass
@dataclass
class APPLICATION:
	display: str
	name: str
	link: str

import json
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import aiohttp

import webbrowser
from urllib.parse import urljoin

from fuzzywuzzy import fuzz
from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm


from ftplib import FTP, error_perm, error_temp, error_proto
import os
import datetime

flags = [
	"initialize",		#0
	"script-run",		#1
	"",					#2
	"",					#3
	"",					#4
	"free-space-error",	#5
	"ftp-attempt",		#6
	"ftp-error",		#7
	"ftp-success",   	#8
	"",					#9
	"ftp-quit",			#10
	"file-notfound",	#11
	"file-sizediff",	#12
	"file-found",		#13
	"",					#14
	"file-limit",		#15
	"download-success",	#16
	"",					#17
	"",					#18
	"",					#19
	"",					#20
	"get-download",		#21
	"got-download",		#22
	"start-download",	#23
	"",					#24
	"",					#25
	"parse-fail",		#26
	"download-fail",	#27
	]

error = "UNCAUGHT ERROR"
log_file = "archive_log.csv"
script_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(script_path)
tcbatch_path = os.path.join(parent_path,"TCBatch")
archive_flag = os.path.join(tcbatch_path,"__archive__")

application_list = "application_list.json"

async def check_already_downloaded(filename: str) -> bool:
	"""RETURNS TRUE IF FILE ALREADY DOWNLOADED"""
	downloaded_files = os.listdir(tcbatch_path)
	for file in downloaded_files:
		if filename.lower() == file.lower():
			return True

	return False

def check_file_size(filename: str) -> bool:
	"""RETURNS TRUE IF FILE SIZES MATCH"""



async def get_page_html(url: str):
	"""Get page HTML, including content loaded via JavaScript."""
	browser = await launch()
	try:
		page = await browser.newPage()
		await page.goto(url)
		html = await page.content()
	finally:
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

async def download_from_web(app_name: str, url: str):
	"""Download a file from a URL."""
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				filename = url.split("/")[-1]
				if not await check_already_downloaded(filename):
					console_log(flags[23],f"DOWNLOADING: {app_name.upper()}")
					with open(os.path.join(tcbatch_path,filename), 'wb') as f:
						async for data in response.content.iter_any():
							f.write(data)
					console_log(flags[16],f"FINISHED DOWNLOAD: {app_name}")
				else:
					console_log(flags[13],f"{app_name.upper()} ALREADY IN GLINET")

	except Exception as e:
		console_log(flags[27],f"COULD NOT DOWNLOAD: {app_name}")


async def find_file_from_website(app: APPLICATION):
	url = app.link
	try:
		html = await get_page_html(url)
		download_link = parse_html_for_link(url, html)
		if download_link is not None:
			console_log(flags[22],f"GOT LINK FOR: {app.display}")
			await download_from_web(app.display, download_link)
			return True
		else:
			console_log(flags[26], f"NO LINK FOR: {app.display}")
			return None
		
	except Exception as e:
		console_log(flags[26], f"COULD NOT PARSE: {app.display}")
		return None

# async def get_download(download_list: list):
# 	TIMEOUT_DURATION = 5
# 	download_tasks = []
# 	archived_apps = []

# 	file_limit = 0

# 	for i, app, in enumerate(download_list):
# 		if file_limit < 1000:
# 			if app.link == "Archive":
# 				archived_apps.append(app)
# 			else:
# 				console_log(flags[21],f"GETTING FROM ONLINE: {app.display}")
# 				task = asyncio.wait_for(find_file_from_website(app), TIMEOUT_DURATION)
# 				download_tasks.append(task)
# 			file_limit += 1
# 		else:
# 			console_log(flags[15],"DEBUG FILE LIMIT REACHED - INTERNET")
# 			break

# 	# Execute all tasks concurrently
# 	results = []
# 	for task in download_tasks:
# 		try:
# 			result = await task
# 			results.append(result)
# 		except asyncio.TimeoutError:
# 			# If there's a timeout, append None to results (or any sentinel value you prefer)
# 			results.append(None)

# 	for result, app in zip(results, download_list):
# 		if result is None:
# 			archived_apps.append(app)

# 	return archived_apps

async def get_download(download_list: list):
    TIMEOUT_DURATION = 5
    download_tasks = []
    archived_apps = []

    file_limit = 0

    for i, app in enumerate(download_list):
        if file_limit < 1000:
            if app.link == "Archive":
                archived_apps.append(app)
            else:
                # console_log(flags[21],f"GETTING FROM ONLINE: {app.display}")
                task = asyncio.wait_for(find_file_from_website(app), TIMEOUT_DURATION)
                download_tasks.append(task)
            file_limit += 1
        else:
            console_log(flags[15],"DEBUG FILE LIMIT REACHED - INTERNET")
            break

    # Execute all tasks concurrently
    results = []
    for task, app in zip(download_tasks, download_list):
        try:
            result = await task
            results.append(result)
            if result is None:  # If the download failed (based on your sentinel value)
                archived_apps.append(app)
        except asyncio.TimeoutError:
            # If there's a timeout, append None to results (or any sentinel value you prefer)
            results.append(None)
            archived_apps.append(app)  # Add app to archived list if there's a timeout

    return archived_apps

# ---------------------------------------------------------------------------- #
#                                    ARCHIVE                                   #
# ---------------------------------------------------------------------------- #

def download_from_archive(ftp, file):
	"""download from FTP server"""
	try:
		with open(f"{tcbatch_path}/{file}", 'wb') as local_file:
			ftp.retrbinary('RETR ' + file, local_file.write)
		console_log(flags[16],f"DOWNLOADED {file}")
	except (error_perm, error_temp, error_proto, EOFError, IOError, FileNotFoundError, PermissionError, MemoryError, TypeError, Exception) as e:
		if isinstance(e, Exception):  # All exceptions derive from the base Exception class.
			console_log(flags[7], str(e).upper())
		else:
			console_log(error, "UNCAUGHT ERROR")


def search_archive(init: bool):
	"""connect to FTP server and compare files"""
	console_log(flags[6],"CONNECTING TO FTP")
	try:
		ftp = FTP("tedcharlesbrown.synology.me")
		# ftp = FTP("192.168.1.100")
		ftp.login("_FTP_", "tedcharlesbrown_ftp")
		console_log(flags[8],"FTP CONNECTION SUCCESS")

	except (error_perm, error_temp, error_proto, EOFError, IOError, FileNotFoundError, PermissionError, MemoryError, TypeError, Exception) as e:
		if isinstance(e, Exception):  # All exceptions derive from the base Exception class.
			console_log(flags[7], str(e).upper())
		else:
			console_log(error, "UNCAUGHT ERROR")

	files_in_archive = ftp.nlst()
	files_downloaded = os.listdir(tcbatch_path)

	file_limit = 0

	if init:
		if application_list in files_in_archive:
			download_from_archive(ftp,application_list)
	else:
		for file in files_in_archive:
			if file != "__hidden__" and file != application_list:
				if file_limit < 10000:
					if not asyncio.run(check_already_downloaded(file)):
						console_log(flags[11],f"{file.upper()} NOT IN GLINET")
						download_from_archive(ftp,file)
					elif ftp.size(file) != os.path.getsize(os.path.join(tcbatch_path,file)):
						console_log(flags[12],f"{file.upper()} SIZE MISMATCH")
						download_from_archive(ftp,file)
					else:
						console_log(flags[13],f"{file.upper()} IN GLINET, SKIPPING")
					file_limit += 1
				else:
					console_log(flags[15],"DEBUG FILE LIMIT REACHED- ARCHIVE")
					break

	ftp.quit()
	console_log(flags[10],f"FTP CLOSED")

# ---------------------------------------------------------------------------- #
#                                  CONSOLE LOG                                 #
# ---------------------------------------------------------------------------- #

def console_log(flag: str, log: str):
	"""prints to the console and appends the log file"""
	date = datetime.datetime.now()
	print(date, flag, log)
	with open(os.path.join(script_path,log_file),'a') as file:
		file.write(f"\n{date},{flag},{log}")


if not os.path.exists(log_file):
	with open(os.path.join(script_path,log_file),'w') as file:
		file.write(f"[TIME],[FLAG],[LOG]\n{datetime.datetime.now()},{flags[0]},LOG CREATED")

if not os.path.exists(tcbatch_path):
	os.mkdir(tcbatch_path)

if not os.path.exists(archive_flag):
	with open(archive_flag,'w') as file:
		file.write("")
	

console_log(flags[1],"-----RUNNING SCRIPT-----")

# GET APPLICATION DOWNLOAD LIST
search_archive(True)

#PARSE LIST FROM APPLICATION DOWNLOAD LIST
download_list = []
with open(os.path.join(tcbatch_path,application_list), "r") as json_file:
	json_data = json.load(json_file)

for item in json_data:
	app = APPLICATION(item["display"], item["name"], item["link"])
	download_list.append(app)

apps = asyncio.run(get_download(download_list))
search_archive(False)