
import os.path
import os
import subprocess
import platform
import subprocess
import msvcrt
import time
import ipaddress
import threading

import pyuac

import questionary
from questionary import Style
from questionary import Validator, ValidationError, prompt

from questions import ask_select
from questions import ask_checkbox
from questions import ask_text
from questions import custom_style


import winshell

from classes import MENU
from menu_change_name import *

from change_ip import list_network_adapters
from change_ip import set_network_adapter

from application_list import APPLICATION_DOWNLOAD_LIST
from download_software import get_download

from install_software import install_applications

from constants import *


# ---------------------------------------------------------------------------- #

def folder_application_init():
	if not os.path.exists(APPLICATION_FOLDER_PATH):
		os.makedirs(APPLICATION_FOLDER_PATH)
		print(DIVIDER)
		print("APPLICATION INSTALL FOLDER NOT FOUND - CREATING ONE")
		print(DIVIDER)

# ---------------------------------------------------------------------------- #
#                                   MAIN MENU                                  #
# ---------------------------------------------------------------------------- #

def menu_main():
	choices = ["Change Computer Name", "Change IP Addresses", "Download Software", "Install Software", "Create Startup Symlink Folder", "Restart Computer"]

	match ask_select(APP_NAME,choices,True):
		case 0:
			menu_change_computer_name()
		case 1:
			menu_change_ip_address()
		case 2:
			menu_download_software()
		case 3:
			menu_install_software()
		case 4:
			menu_startup_symlink()
		case 5:
			menu_restart_computer()


def menu_change_computer_name():
	user_input = questionary.text(
	f"{ASCII_COMPUTER_NAME}\nCURRENT COMPUTER NAME = " + "'" + platform.node() + "'",
	instruction="\ntype new name and press <enter>, or press <enter> to cancel\n",
	qmark="",
	style=custom_style
	).ask()

	if user_input == "":
			# print("GOING BACK TO MAIN MENU")
			questionary.print(DIVIDER, style="bold")	
			menu_main()
	else:
		if questionary.confirm(f"\nCHANGE NAME TO {user_input}?",qmark="",style=custom_style).ask():
			print()
			questionary.print(DIVIDER, style="bold")
			questionary.print("CHANGING NAME TO: " + user_input, style="bold")
			# subprocess.call(['powershell.exe', "Rename-Computer -NewName " + user_input])
			questionary.print(DIVIDER, style="bold")
			menu_main()
		else:
			print()
			questionary.print(DIVIDER, style="bold")	
			menu_main()

def menu_change_ip_address():

	interface = ask_select(ASCII_IP_ADDRESS,list_network_adapters(),False)

	return_string = []
	primary_dns = ""
	secondary_dns = ""
	ip_adddress = ask_text("IP ADDRESS:")
	if ip_adddress:
		return_string.append(ip_adddress)
		subnet = ask_text("SUBNET:")

		if subnet:
			return_string.append(subnet)
			gateway = ask_text("GATEWAY:")

			if gateway:
				return_string.append(gateway)
				primary_dns = ask_text("PRIMARY DNS:")

				if primary_dns:
					secondary_dns = ask_text("SECONDARY DNS:")

		set_network_adapter(interface, return_string, primary_dns, secondary_dns)

	menu_main()


def menu_download_software():
	choices = []
	for application in APPLICATION_DOWNLOAD_LIST:
		choices.append(application.display)
	
	get_download(ask_checkbox(ASCII_DOWNLOAD,choices,False))

	menu_main()

def menu_install_software():
	application_install_list = os.listdir(APPLICATION_FOLDER_PATH)
	if len(application_install_list) == 0:
		print("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!")
	else:
		install_applications(ask_checkbox(ASCII_SOFTWARE, application_install_list,False))

	menu_main()

def menu_startup_symlink():
	print(DIVIDER)
	print(ASCII_SYMLINK)
	print(DIVIDER)
	print("CREATING STARTUP SYMLINK FOLDER")
	time.sleep(2)
	try:
		os.symlink(PATH_STARTUP_FOLDER,"Startup_Symlink")
	except:
		print("COULD NOT CREATE STARTUP FOLDER, CHECK IF ALREADY EXISTS?")
		time.sleep(1)

	menu_main()

def menu_restart_computer():
	global cancel_restart_flag
	print("RESTARTING COMPUTER IN 5 SECONDS, PRESS 'ENTER' TO CANCEL")
	
	# Create a flag variable to cancel the thread
	cancel_restart_flag = False
	
	# Start a new thread to restart the computer
	t = threading.Thread(target=restart_computer)
	t.start()

	# Wait for user input
	user_input = input()
	if user_input == "":
		# Cancel the restart
		cancel_restart_flag = True
		print("RESTART CANCELLED")
		print(DIVIDER)
		time.sleep(1)

	else:
		# Restart the computer
		t.join()
	

def restart_computer():
	global cancel_restart_flag
	timeout = 5
	time.sleep(1)
	while timeout > 0:
		# Check the flag and exit if necessary
		if cancel_restart_flag:
			return
		print(timeout)
		timeout -= 1
		time.sleep(1)
	
	# Restart the computer
	print("RESTARTING")
	# os.system("shutdown /r")




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

