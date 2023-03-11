

import requests

from bs4 import BeautifulSoup

import ftplib
from tqdm import tqdm
import webbrowser
from urllib.parse import urlparse

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


def parse_html_for_link(app: APPLICATION, verbose: bool):

	
	if type(app) == str:
		link = app
	else:
		link = app.link

	if ".exe" in link or ".msi" in link:
		download_link = link
	else:
		# find the index of the character immediately after the "://" substring
		index_start = link.find("://") + 3
		# find the index of the first "/" character that appears after index_start
		index_end = link.find("/",index_start)
		# extract the base URL of the website from the download_url string
		base_url = link[:index_end]
		
		# send a request to the website
		response = requests.get(link)

		# parse the HTML content
		soup = BeautifulSoup(response.text, 'html.parser')

		# convert the parsed HTML content to a string and encode it as UTF-8
		html = str(soup.prettify().encode('utf-8'))
		
		# find the index of the character immediately after the ".exe" substring
		index_end = -1
		if html.find(".exe") != -1:
			index_end = html.find(".exe") + 4
		elif html.find(".msi") != -1:
			index_end = html.find(".msi") + 4

		# extract the download link from the html string
		download_link = html[:index_end]

		# find the index of the character immediately after the "http" substring
		index_start = download_link.rfind("http")

		if index_start == -1 or index_start < download_link.rfind(" "):
			if verbose:
				print("DIRECT LINK NOT GIVEN, USING BASE")
			index_start = download_link.rfind("href=") + 6
			# extract the download name from the html string
			download_name = html[index_start:index_end]
			# if download_name does not begin with a '/' add one
			if download_name[0] != "/":
				download_name = "/" + download_name
			# concatenate the base URL and the download name to create the full download link
			download_link = base_url + download_name
			
			# print(index_start,download_name)
		else:
			# extract the download name from the html string
			download_link = html[index_start:index_end]
	try:
		# is_valid_url(download_link)
		if download_link.find(" ") == -1:
			if verbose:
				print(f"DOWNLOADING FROM: {download_link}")
			return download_link
		else:
			print("COULD NOT PARSE DOWNLOAD LINK")
			return False
	except:
		return False


# def get_github(filename: str, owner: str, repo: str):
#     # define the URL of the GitHub releases page
#     url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

#     # send a request to the GitHub API to get the latest release
#     response = requests.get(url)

#     # check the status code of the response
#     if response.status_code == 200:
#         # parse the JSON data
#         data = json.loads(response.text)
#         # get the URL of the .exe file
#         exe_url = data['assets'][0]['browser_download_url']

#         get_download(filename,exe_url)

def download_from_web(response, app):
	if isinstance(app, str):
		name = app
	else:
		name = app.name

	if response.headers.get("Content-Disposition"):
		content_disposition = response.headers.get("Content-Disposition")
		content_disposition = content_disposition.replace("\"", "")
		index_start = content_disposition.find("filename=") + 9
		name = content_disposition[index_start:]
	elif ".exe" in response.url or ".msi" in response.url:
		index_start = response.url.rfind("/")
		name = response.url[index_start:]

	if response.status_code == 200:
		total_size = int(response.headers.get('content-length', 0))
		downloaded = 0

		print(DIVIDER)

		with open(UTILITY_FOLDER_PATH + name, 'wb') as f:
			for data in tqdm(response.iter_content(chunk_size=4096),
							 total=total_size // 4096 + 1,
							 unit='B', unit_scale=True, desc=f'Downloading {name}'):
				downloaded += len(data)
				f.write(data)

		print("Download complete")
	else:
		print("Error downloading file:", response.status_code)
		download_from_archive(app.name)

	print(DIVIDER)

def get_download(app_list: list):
	if len(app_list) == 0:
		print_error("NO OPTIONS SELECTED, SELECT OPTIONS WITH <space>")
	for i, app in enumerate(APPLICATION_DOWNLOAD_LIST):
		for selected in app_list:
			if selected in app.display:
				app = APPLICATION_DOWNLOAD_LIST[i]

				if i != len(APPLICATION_DOWNLOAD_LIST) - 1:
					print(f"DOWNLOADING: {app.display}")

					if app.link == "False":
						pass
					elif parse_html_for_link(app, False):
						# print("ATTEMPTING TO GET FROM INTERNET")
						response = requests.get(parse_html_for_link(app, True), stream=True)
						download_from_web(response, app)
						return
					download_from_archive(app.name)

				else:
					print("PASSWORD: TCB ADDRESS (numbers only)")
					webbrowser.open("http://gofile.me/70auI/6qt31duqE", new=0, autoraise=True)

		
def custom_download(link: str):
	if parse_html_for_link(link, False):
		response = requests.get(parse_html_for_link(link, True), stream=True)
		download_from_web(response, "custom.exe")
	else:
		print("COULD NOT FETCH DOWNLOAD")