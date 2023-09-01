import os.path
import os
import time
import subprocess
import argparse
import sys
import shutil

import pyuac

import questionary

from questions import *
from constants import *
import constants

from src_computer_name.menu_computer_name import menu_change_computer_name
from src_network.menu_network import menu_change_network
from src_network.change_ip import reset_network_adapters
from src_software.menu_software import menu_manage_software
from src_optimize_windows.menu_optimize_windows import menu_optimize_windows
from src_restart.menu_restart import menu_restart_computer
from src_automations.menu_automations import menu_custom_automations


# ---------------------------------------------------------------------------- #

def utility_folder_init():
	if not os.path.exists(UTILITY_FOLDER_PATH):
		# print_error("CREATING TCBatch FOLDER IN C DRIVE")
		os.makedirs(UTILITY_FOLDER_PATH)
		# print_error("CREATING SETTINGS.JSON IN C DRIVE")
		save_settings()
	elif not os.path.exists(UTILITY_FOLDER_PATH + SETTINGS_FOLDER):
		# print_error("CREATING SETTINGS.JSON IN C DRIVE")
		save_settings()
	elif os.path.exists(UTILITY_FOLDER_PATH) and os.path.exists(UTILITY_FOLDER_PATH + SETTINGS_FOLDER):
		# print_error("READING SETTINGS.JSON IN C DRIVE")
		with open(UTILITY_FOLDER_PATH + SETTINGS_FOLDER, "r") as json_file:
			json_data = json.load(json_file)
			download_path = json_data["download path"]
			try:
				if os.access(download_path, os.W_OK):
					constants.DOWNLOAD_FOLDER_PATH = download_path
				else:
					# print_error("COULD NOT REACH DOWNLOAD FOLDER")
					save_settings()
			except Exception as e:
				print(e)
				save_settings()

	print(f"CURRENT DOWNLOAD FOLDER {constants.DOWNLOAD_FOLDER_PATH}")

	# ----------------- create a copy of the exe for command line prompts ---------------- #
	try:
		if getattr(sys, 'frozen', False):
			# Copy the .exe file to UTILITY_FOLDER_PATH
			current_exe_path = sys.executable  # Path of the running .exe file
			destination_path = os.path.join(UTILITY_FOLDER_PATH, os.path.basename(current_exe_path))
			
			# Copy the file only if it doesn't already exist in the destination
			if not os.path.exists(destination_path):
				shutil.copy(current_exe_path, destination_path)
	except:
		pass

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

def handle_starting_arguments():
	parser = argparse.ArgumentParser(description=f'TCBatch {APP_VERSION}')
	parser.add_argument('-hello', action='store_true', help='returns "world" for testing')
	parser.add_argument('-v', action='store_true', help='returns version')

	parser.add_argument('-ip-reset', action='store_true', help='resets all ip addresses sequentially starting at 192.168.8.100 - requires admin')
	

	args, unknown = parser.parse_known_args()
	# args = parser.parse_args()

	if args.hello:
		print("world.")
		return False
	
	if args.v:
		print(APP_VERSION)
		return False

	if args.ip_reset:
		reset_network_adapters()
		return False
	
	return True


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

def main():
	utility_folder_init()
	menu_main()


if __name__ == "__main__":
	if handle_starting_arguments(): 
		if not pyuac.isUserAdmin():
			print("RE-LAUNCHING AS ADMIN!")
			time.sleep(1)
			pyuac.runAsAdmin()
		else:        
			main()  # Already an admin here.

