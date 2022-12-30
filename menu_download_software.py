

import requests

from bs4 import BeautifulSoup

import ftplib
import threading
import os
from urllib.parse import urlparse

from classes import MENU

from constants import *
from application_list import *

import importlib

# ---------------------------------------------------------------------------- #
#                                   DOWNLOAD                                   #
# ---------------------------------------------------------------------------- #

class MENU_download(MENU):
	def enter(self):
		print(self.greeting)
		print(DIVIDER)
		for app in APPLICATION_DOWNLOAD_LIST:
			self.options_list.append(app)
		self.list_options()

	def list_options(self):
		for i, option in enumerate(self.options_list):
			i += 1
			print(f"{int(i)}: {option.display}")
		print(DIVIDER)
		self.wait_for_input()

	def wait_for_input(self):
		intial_user_input = input()
		user_input = intial_user_input
		

		if user_input == "":
			pass
		else:
			user_input = intial_user_input.split(",")
			for number in user_input:
				archive = False
				# CHECK TO SEE IF '/' IS INCLUDED TO DOWNLOAD DIRECT FROM ARCHIVE
				if "/" in number:
					archive = True
					number = number[:-1]
					
				if number.isdigit():
					number = int(number) - 1

				get_download(self.options_list[number],archive)

		main.menu()


# ---------------------------------------------------------------------------- #
#                               VERSION DOWNLOAD                               #
# ---------------------------------------------------------------------------- #
class MENU_version(MENU):
	def list_options(self):
		self.options_list.reverse()
		for i, option in enumerate(self.options_list):
			i += 1
			print(f"{int(i)}: {option}")
		print(DIVIDER)
		# self.wait_for_input()

	def wait_for_input(self):
		user_input = input()
		if user_input == "":
			pass
		else:
			user_input = int(user_input) - 1
			
			choice = self.options_list[user_input]

			print(choice)
			return choice

		print("GOING BACK TO MAIN MENU")
		print(DIVIDER)
		main.menu()

def download_from_archive(file_to_search: str):
	print("DOWNLOADING FROM ARCHIVE")
	file_found = False

	try:
		ftp = ftplib.FTP("tedcharlesbrown.synology.me")
	except:
		ftp = ftplib.FTP("192.168.1.100")

	ftp.login("_FTP_","tedcharlesbrown_ftp")
	# ftp.cwd("/Application_Installers")

	files = ftp.nlst()

	versions = 0
	m_versions = MENU_version("Download Versions", "MULTIPLE VERSIONS FOUND, WHICH VERSION TO DOWNLOAD")

	for file in files:
		if file.lower().replace("-","").find(file_to_search.lower().replace("-","")[:-4]) != -1:
			file_to_download = file
			file_found = True
			m_versions.add_option(file)
			versions += 1

	if file_found:
		if versions > 1:
			m_versions.enter()
			file_to_download = m_versions.wait_for_input()
		# Download the file
		with open(APPLICATION_FOLDER_PATH + file_to_download, 'wb') as f:
			print(f"FOUND {file_to_download} FROM ARCHIVE, PLEASE WAIT")
			ftp.retrbinary(f'RETR {file_to_download}', f.write) 
			print("DOWNLOAD COMPLETE")
		
	else:
		print("NOT IN ARCHIVE")

	print(DIVIDER)
	ftp.quit()

def parse_html_for_link(app: APPLICATION, verbose: bool):

	# print("TEST")
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

	if type(app) == str:
		name = app
	else:
		name = app.name
	
	if response.headers.get("Content-Disposition"):
		# Get the value of the Content-Disposition header
		content_disposition = response.headers.get("Content-Disposition")
		# Split the value by ";" to get a list of key-value pairs
		content_disposition = content_disposition.replace("\"","")
		index_start = content_disposition.find("filename=") + 9
		name = content_disposition[index_start:]
	elif ".exe" in response.url or ".msi" in response.url:
		index_start = response.url.rfind("/")
		name = response.url[index_start:]


	if response.status_code == 200:
		# get the total size of the file
		total_size = int(response.headers.get('content-length', 0))
		# initialize a variable to store the number of bytes downloaded so far
		downloaded = 0
		# initialize a variable to store the last progress that was printed
		last_progress = -1
		
		print(DIVIDER)

		with open(APPLICATION_FOLDER_PATH + name,'wb') as f:
			for data in response.iter_content(chunk_size=4096):
				# update the number of bytes downloaded
				downloaded += len(data)
				# write the data to the file
				f.write(data)
				# check if the total size is known
				if total_size > 0:
					# calculate the download progress as a percentage
					progress = int(downloaded / total_size * 100)
					# only print the progress if it is a multiple of 10 and if it is different from the last progress that was printed
					if progress % 25 == 0 and progress != last_progress:
						print(f'Download progress: {(downloaded / 1e+6):.2f} Megabytes of {(total_size / 1e+6):.2f}, [ {progress}% ]')
						last_progress = progress
	
	else:
		print("Error downloading file:", response.status_code)
		download_from_archive(app.name)

	print(DIVIDER)

def get_download(app: APPLICATION, archive: bool):
	print(f"DOWNLOADING: {app.display}")

	if app.link == "False" or archive:
		pass
	elif parse_html_for_link(app, False):
		# print("ATTEMPTING TO GET FROM INTERNET")
		response = requests.get(parse_html_for_link(app, True), stream=True)
		download_from_web(response, app)
		return
	download_from_archive(app.name)
		
def custom_download(link: str):
	if parse_html_for_link(link, False):
		response = requests.get(parse_html_for_link(link, True), stream=True)
		download_from_web(response, "custom.exe")
	else:
		print("COULD NOT FETCH DOWNLOAD")


# ---------------------------------------------------------------------------- #
#                                 BOTTOM IMPORT                                #
# ---------------------------------------------------------------------------- #
main = importlib.import_module('main')

