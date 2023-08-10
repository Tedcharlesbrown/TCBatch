import os.path
import os
import time
import subprocess

import pyuac

import questionary

from questions import *
from constants import *
import constants

from src_computer_name.menu_computer_name import menu_change_computer_name
from src_network.menu_network import menu_change_network
from src_software.menu_software import menu_manage_software
from src_optimize_windows.menu_optimize_windows import menu_optimize_windows
from src_restart.menu_restart import menu_restart_computer
from src_automations.menu_automations import menu_custom_automations


# ---------------------------------------------------------------------------- #

def folder_application_init():
	if not os.path.exists(UTILITY_FOLDER_PATH):
		os.makedirs(UTILITY_FOLDER_PATH)
		save_settings()
	else:
		with open(UTILITY_FOLDER_PATH + SETTINGS_FOLDER, "r") as json_file:
			json_data = json.load(json_file)
		
		constants.DOWNLOAD_FOLDER_PATH = json_data["download path"]

		if not os.path.exists(constants.DOWNLOAD_FOLDER_PATH):
			os.makedirs(constants.DOWNLOAD_FOLDER_PATH)

	print(f"CURRENT DOWNLOAD FOLDER {constants.DOWNLOAD_FOLDER_PATH}")

# ---------------------------------------------------------------------------- #
#                                   MAIN MENU                                  #
# ---------------------------------------------------------------------------- #

def menu_main():
	choices = [
		"Manage Windows Settings",					#0
		"Download / Install Software",					#1
		"Automations",						#2
		"Restart Computer"]					#3

	# WINDOWS BACKUP?

	match ask_select(APP_NAME,choices,True):
		case 0:
			menu_manage_windows()
		case 1:
			menu_manage_software()
		case 2:
			menu_custom_automations()
		case 3:
			menu_restart_computer()
	
	menu_main()

def menu_manage_windows():
	choices = [
		"Change Computer Name",
		"Change Network Settings",
		"Optimize Windows",
		"Create Startup Shortcut Folder"
	]

	choices.append("[return]")
	cancel = choices[-1]

	match ask_select(ASCII_MANAGE_WINDOWS,choices,True):
		case 0:
			menu_change_computer_name()
		case 1:
			menu_change_network()
		case 2:
			# print_hint("-----credit to Andy Babin-----")
			menu_optimize_windows()
		case 3:
			menu_startup_symlink()
		case cancel:
			return
		
	menu_manage_windows()

# ---------------------------------------------------------------------------- #
#                              SET STARTUP SYMLINK                             #
# ---------------------------------------------------------------------------- #

def menu_startup_symlink():
	questionary.print("CREATING STARTUP SYMLINK FOLDER", style="bold")

	winshell.CreateShortcut(
	Path=os.path.join(winshell.desktop(), "Startup_Shortcut.lnk"),
	Target=PATH_STARTUP_FOLDER,
	Icon=(PATH_STARTUP_FOLDER, 0),
	Description="Shortcut to Startup"
)

	time.sleep(1)

	# print_return()
	menu_manage_windows()


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

def main():
	folder_application_init()
	menu_main()


if __name__ == "__main__":
	if not pyuac.isUserAdmin():
		print("RE-LAUNCHING AS ADMIN!")
		time.sleep(1)
		pyuac.runAsAdmin()
	else:        
		main()  # Already an admin here.

