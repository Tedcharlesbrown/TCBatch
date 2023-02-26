
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


import winshell

from classes import MENU
from menu_change_name import *
from menu_change_ip import *

from menu_download_software import *

from menu_install_software import *
from menu_symlink import *
from menu_restart import *

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

def menu():
	m_main = MENU("MAIN MENU", APP_NAME)
	m_name = MENU_name("Change Computer Name", ASCII_COMPUTER_NAME)
	m_ip = MENU_ip("Change IP Addresses", ASCII_IP_ADDRESS)
	m_download = MENU_download("Download Software", ASCII_DOWNLOAD)
	m_software = MENU_software("Install Software", ASCII_SOFTWARE)
	m_symlink = MENU_symlink("Create Symlink Folder", ASCII_SYMLINK)
	m_restart = MENU_restart("Restart Computer", ASCII_RESTART)

	m_main.add_option(m_name)
	m_main.add_option(m_ip)
	m_main.add_option(m_download)
	m_main.add_option(m_software)
	m_main.add_option(m_symlink)
	m_main.add_option(m_restart)

	m_main.enter()

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

def main():
	# folder_application_init()
	# menu()


if __name__ == "__main__":
	if not pyuac.isUserAdmin():
		print("RE-LAUNCHING AS ADMIN!")
		time.sleep(1)
		pyuac.runAsAdmin()
	else:        
		main()  # Already an admin here.

