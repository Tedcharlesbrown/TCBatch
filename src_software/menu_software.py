from constants import *
from questions import *
from src_software.application_list import APPLICATION_DOWNLOAD_LIST
from .download_software import get_archive
from .download_software import get_download
from .install_software import install_applications

import asyncio
import time

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
	# for file in application_install_list:
	# 	if file.endswith(".bmp") or "GrafanaSetup" in file:
	# 		application_install_list.remove(file)
	
	application_install_list = ""
	application_install_list = [file for file in application_install_list if not file.endswith(".bmp") and "GrafanaSetup" not in file]


	if len(application_install_list) == 0:
		# questionary.print("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!", style="fg:#C00000 bold")
		print_error("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!")
		time.sleep(1)
	else:
		install_applications(ask_checkbox(ASCII_SOFTWARE, application_install_list,False))

	print_return()
	return