
import os.path
import os
import subprocess
import platform
import subprocess
import msvcrt
import time
import ipaddress

import pyuac

import questionary
from questionary import Style
from questionary import Validator, ValidationError, prompt


import winshell

from classes import MENU
from menu_change_name import *
from change_ip import list_network_adapters
from change_ip import set_network_adapter

from menu_download_software import *

from menu_install_software import *
from menu_symlink import *
from menu_restart import *

from constants import *

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    # ('answer', 'fg:#f44336 bold'),      # submitted answer text behind the question
    ('answer', 'fg:#039300 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    # ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('highlighted', 'fg:#7000A9 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
	
def ask_select(message: str, choices: list, return_index: bool):

	answer = questionary.select(
    f"{message}\n",
    qmark="",
    instruction=" ",
    style=custom_style,
    choices=choices,
	).ask()

	if return_index:
		for i, choice in enumerate(choices):
			if answer == choice:
				return(i)
	else:
		return answer

def ask_text(message: str):
	return questionary.text(message,qmark="",style=custom_style).ask()


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
	choices = ["Change Computer Name", "Change IP Addresses", "Download Software", "Install Software", "Create Symlink Folder", "Restart Computer"]

	match ask_select(APP_NAME,choices,True):
		case 0:
			menu_change_computer_name()
		case 1:
			menu_change_ip_address()
		case 2:
			menu_download_software()


def menu_change_computer_name():
	user_input = questionary.text(
	f"{ASCII_COMPUTER_NAME}\nTYPE NEW NAME AND PRESS 'ENTER', OR PRESS 'ENTER' TO CANCEL\nCURRENT COMPUTER NAME = " + "'" + platform.node() + "'\n\n",
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
	pass

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

