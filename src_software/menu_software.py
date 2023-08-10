from questions import *
from src_software.application_list import get_download_list
from src_software.download_software import check_already_downloaded
from src_software.download_software import get_archive
from src_software.download_software import get_download
from src_software.install_software import install_applications

from constants import *
import constants

import asyncio
import time
import os


def menu_manage_software():
	choices = [
		"Download Software",
		"Install Software",
		"Change Software Folder"
	]

	choices.append("[return]")
	cancel = choices[-1]

	match ask_select("MANAGE SOFTWARE",choices,True):
		case 0:
			menu_download_software()
			menu_manage_software()
		case 1:
			menu_install_software()
			menu_manage_software()
		case 2:
			menu_change_folder_location()
			menu_manage_software()
		case cancel:
			return



# ---------------------------------------------------------------------------- #
#                               DOWNLOAD SOFTWARE                              #
# ---------------------------------------------------------------------------- #

def menu_download_software():
	choices = []
	get_download_list()
	
	for application in constants.APPLICATION_DOWNLOAD_LIST:
		choices.append(application.display)

	apps = ask_checkbox(ASCII_DOWNLOAD,choices,False)

	apps = check_already_downloaded(apps)
	apps = asyncio.run(get_download(apps))
	get_archive(apps)

	print_return()
	return

# ---------------------------------------------------------------------------- #
#                               INSTALL SOFTWARE                               #
# ---------------------------------------------------------------------------- #


def menu_install_software():
	application_install_list = os.listdir(constants.DOWNLOAD_FOLDER_PATH)

	application_install_list = [file for file in application_install_list if file.endswith(".exe") or file.endswith(".msi")]


	if len(application_install_list) == 0:
		print_error("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!")
		time.sleep(1)
	else:
		install_applications(ask_checkbox(ASCII_SOFTWARE, application_install_list,False))

	print_return()
	return

# ---------------------------------------------------------------------------- #
#                            CHANGE FOLDER LOCATION                            #
# ---------------------------------------------------------------------------- #

from src_software.change_folder_location import get_mounted_drives
from src_software.change_folder_location import get_shared_folders

def menu_change_folder_location():
	choices = [
		"Local Drive",
		"Network Shared Drive",
	]

	choices.append("[return]")
	cancel = choices[-1]

	match ask_select("CHANGE FOLDER",choices,True):
		case 0:
			choices = get_mounted_drives()
			choices.append("[return]")
			cancel = choices[-1]
			new_path = ask_select("LOCAL DRIVE",choices,False)
			constants.DOWNLOAD_FOLDER_PATH = new_path + "TCBatch/"
		case 1:
			user_input = ask_text("IP ADDRESS:")
			if user_input:
				choices = get_shared_folders(user_input)

				if choices is None:
					print("Failed to get shared folders.")
					return

				choices.append("[return]")
				cancel = choices[-1]
				new_path = ask_select("NETWORK DRIVE", choices, False)
				constants.DOWNLOAD_FOLDER_PATH = f"//{user_input}/{new_path}/TCBatch/"
			
		case cancel:
			return
	
	save_settings()
	try:
		os.makedirs(constants.DOWNLOAD_FOLDER_PATH)
	except:
		pass
	
	return
