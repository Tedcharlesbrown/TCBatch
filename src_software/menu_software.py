from questions import *
# from src_software.application_list import APPLICATION_DOWNLOAD_LIST
from src_software.application_list import get_download_list
from src_software.download_software import get_archive
from src_software.download_software import get_download
from src_software.install_software import install_applications
from constants import *

import asyncio
import time


def menu_manage_software():
	choices = [
		"Download Software",
		"Install Software"
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
		case cancel:
			return



# ---------------------------------------------------------------------------- #
#                               DOWNLOAD SOFTWARE                              #
# ---------------------------------------------------------------------------- #

def menu_download_software():
	choices = []
	APPLICATION_DOWNLOAD_LIST = get_download_list()
	
	for application in APPLICATION_DOWNLOAD_LIST:
		choices.append(application.display)

	apps = ask_checkbox(ASCII_DOWNLOAD,choices,False)

	archived_apps = asyncio.run(get_download(apps,APPLICATION_DOWNLOAD_LIST))
	get_archive(archived_apps,APPLICATION_DOWNLOAD_LIST)

	print_return()
	return

# ---------------------------------------------------------------------------- #
#                               INSTALL SOFTWARE                               #
# ---------------------------------------------------------------------------- #

def menu_install_software():
	application_install_list = os.listdir(UTILITY_FOLDER_PATH)

	application_install_list = [file for file in application_install_list if file.endswith(".exe") or file.endswith(".msi")]


	if len(application_install_list) == 0:
		print_error("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!")
		time.sleep(1)
	else:
		install_applications(ask_checkbox(ASCII_SOFTWARE, application_install_list,False))

	print_return()
	return