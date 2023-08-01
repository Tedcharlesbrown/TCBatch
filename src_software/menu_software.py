from constants import *
from questions import *
from src_software.application_list import APPLICATION_DOWNLOAD_LIST
from .download_software import get_archive
from .download_software import get_download
from .install_software import install_applications

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
	for application in APPLICATION_DOWNLOAD_LIST:
		choices.append(application.display)

	apps = ask_checkbox(ASCII_DOWNLOAD,choices,False)

	archived_apps = asyncio.run(get_download(apps))
	get_archive(archived_apps)

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