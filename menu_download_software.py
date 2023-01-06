

import requests

from bs4 import BeautifulSoup

import threading
import ftplib
import msvcrt
from urllib.parse import urlparse
import json

from classes import MENU

from constants import *
from application_list import *

import importlib

VERBOSE = True

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

				get_download(self.options_list[number], archive)

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

	ftp.login("_FTP_", "tedcharlesbrown_ftp")

	files = ftp.nlst()

	versions = 0
	m_versions = MENU_version("Download Versions", "MULTIPLE VERSIONS FOUND, WHICH VERSION TO DOWNLOAD")

	for file in files:
		if file.lower().replace("-", "").find(file_to_search.lower().replace("-", "")[:-4]) != -1:
			file_to_download = file
			file_found = True
			m_versions.add_option(file)
			versions += 1

	if file_found:
		if versions > 1:
			m_versions.enter()
			file_to_download = m_versions.wait_for_input()

		# Get the size of the file on the server
		download_size = ftp.size(file_to_download)

		# Create a flag to track whether the download has been interrupted
		interrupted = False

		# Create a thread to listen for the Enter key press
		def listen_for_interrupt():
			nonlocal interrupted
			# Wait for the user to press the Enter key
			key = msvcrt.getch()
			if key == b'\r':  # b'\r' represents the Enter key
				# Set the interrupted flag to True
				interrupted = True

		# Start the interrupt listener thread
		interrupt_listener = threading.Thread(target=listen_for_interrupt)
		interrupt_listener.start()

		try:
			# Open the local file in binary write mode
			with open(APPLICATION_FOLDER_PATH + file_to_download, 'wb') as f:
				# initialize a variable to store the number of bytes downloaded so far
				downloaded = 0
				# initialize a variable to store the last progress that was printed
				last_progress = -1

				print(DIVIDER)

				# Download the file
				def callback(data):
					# update the number of bytes downloaded
					nonlocal downloaded
					nonlocal last_progress

					# Check for interrupt
					if interrupted:
						raise KeyboardInterrupt

					downloaded += len(data)
					# write the data to the file
					f.write(data)
					# check if the total size is known
					if download_size > 0:
						# calculate the download progress as a percentage
						progress = int(downloaded / download_size * 100)
						# only print the progress if it is a multiple of 25 and if it is different from the last progress that was printed
						if progress % 25 == 0 and progress != last_progress:
							print(f'Download progress: {(downloaded / 1e+6):.2f} Megabytes of {(download_size / 1e+6):.2f}, [ {progress}% ]')
							last_progress = progress

				ftp.retrbinary(f'RETR {file_to_download}', callback)

		except KeyboardInterrupt:
			# code to handle the keyboard interrupt goes here
			print('Keyboard interrupt detected, stopping download...')

	else:
		print("NOT IN ARCHIVE")

	print(DIVIDER)

	try:
		ftp.quit()
	except:
		pass


def parse_html_for_link(app: APPLICATION):

	# IF DIRECT LINK GIVEN, USE LINK
	if type(app) == str:
		url = app
	# ELSE, APP GIVEN, USE APP LINK
	else:
		url = app.link

	if ".exe" in url or ".msi" in url:
		# IF URL IS DIRECT LINK
		if VERBOSE:
			print("PARSING LINK AS DIRECT")
		download_link = url
	else:
		# PARSE URL FOR BASE
		parsed_url = urlparse(url)
		base_url = '{}://{}'.format(parsed_url.scheme, parsed_url.netloc)
		if VERBOSE:
			print(f"FOUND BASE URL: {base_url}")

		# send a request to the website
		response = requests.get(url).text

		# parse the HTML content
		soup = BeautifulSoup(response, 'html.parser')

		# Find the download link

		download_link = soup.find('a', href=lambda x: x and (x.endswith('.exe') or x.endswith('.msi')))

		if download_link is None:
			if VERBOSE:
				print("NO EXE OR MSI FOUND")
			find_download_button(soup)
		else:
			download_link = download_link['href']
			if VERBOSE:
				print(f"EXE OR MSI FOUND: {download_link}")
			if download_link.find("http") == -1:
				if VERBOSE:
					print("NO HTTP FOUND, ADDING BASE URL")
				download_link = f"{base_url}/{download_link}"
			else:
				find_download_button(soup)

	return download_link

def find_download_button(soup):
	# Find the download button using its ID
	download_button = soup.find(id="download-alt-win") # VSCODE
	# Find the URL to download the file from
	download_link = download_button['href']


	# script_element = soup.find(id="download-details")
	# download_details_json = script_element.innerHTML
	# download_details = json.loads(download_details_json)
	# download_link = download_details["windows"]["downloadLink"]

	# print(download_link)
	return download_link

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

def download_from_web(url, app):

	# return

	response = requests.get(url, stream=True)

	if response.headers.get("Content-Disposition") and response.headers.get("Content-Disposition").startswith("filename="):
		content_disposition = response.headers.get("Content-Disposition").replace("\"", "")
		name = content_disposition[content_disposition.find("filename=") + 9:]
	elif ".exe" in response.url or ".msi" in response.url:
		index_start = response.url.rfind("/")
		name = response.url[index_start:]

	# Create a flag to track whether the download has been interrupted
	interrupted = False

	# Create a thread to listen for the Enter key press
	def listen_for_interrupt():
		nonlocal interrupted
		# Wait for the user to press the Enter key
		key = msvcrt.getch()
		if key == b'\r':  # b'\r' represents the Enter key
			# Set the interrupted flag to True
			interrupted = True

	# Start the interrupt listener thread
	interrupt_listener = threading.Thread(target=listen_for_interrupt)
	interrupt_listener.start()

	try:
		if response.status_code == 200:
			# get the total size of the file
			total_size = int(response.headers.get('content-length', 0))
			# initialize a variable to store the number of bytes downloaded so far
			downloaded = 0
			# initialize a variable to store the last progress that was printed
			last_progress = -1

			print(DIVIDER)

			with open(APPLICATION_FOLDER_PATH + name, 'wb') as f:
				for data in response.iter_content(chunk_size=4096):
					# Check for interrupt
					if interrupted:
						raise KeyboardInterrupt
					# update the number of bytes downloaded
					downloaded += len(data)
					# write the data to the file
					f.write(data)
					# check if the total size is known
					if total_size > 0:
						# calculate the download progress as a percentage
						progress = int(downloaded / total_size * 100)
						# only print the progress if it is a multiple of 25 and if it is different from the last progress that was printed
						if progress % 25 == 0 and progress != last_progress:
							print(f'Download progress: {(downloaded / 1e+6):.2f} Megabytes of {(total_size / 1e+6):.2f}, [ {progress}% ]')
							last_progress = progress

		else:
			print("Error downloading file:", response.status_code)
			download_from_archive(app.name)

	except KeyboardInterrupt:
		   # code to handle the keyboard interrupt goes here
		print('Keyboard interrupt detected, stopping download...')

	print(DIVIDER)


def get_download(app: APPLICATION, archive: bool):
	print(DIVIDER)
	print(f"DOWNLOADING: {app.display}")

	if archive == False and app.link:
		try:
			download_from_web(parse_html_for_link(app), app)
		except:
			download_from_archive(app.name)
	else:
		download_from_archive(app.name)


# ---------------------------------------------------------------------------- #
#                                 BOTTOM IMPORT                                #
# ---------------------------------------------------------------------------- #
main = importlib.import_module('main')
