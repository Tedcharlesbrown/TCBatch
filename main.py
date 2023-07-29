import os.path
import os
import time

import pyuac

import questionary

from questions import *
from constants import *

from src_computer_name.menu_computer_name import menu_change_computer_name
from src_network.menu_network import menu_change_network
from src_software.menu_software import menu_download_software
from src_software.menu_software import menu_install_software
from src_optimize_windows.menu_optimize_windows import menu_optimize_windows
from src_restart.menu_restart import menu_restart_computer
from src_grafana.menu_grafana import menu_setup_grafana


# ---------------------------------------------------------------------------- #

def folder_application_init():
	if not os.path.exists(UTILITY_FOLDER_PATH):
		os.makedirs(UTILITY_FOLDER_PATH)
		print(DIVIDER)
		print("APPLICATION INSTALL FOLDER NOT FOUND - CREATING ONE")
		print(DIVIDER)

# ---------------------------------------------------------------------------- #
#                                   MAIN MENU                                  #
# ---------------------------------------------------------------------------- #

def menu_main():
	choices = [
		"Change Computer Name",				#0
		"Change Network Settings",			#1
		"Download Software",				#2
		"Install Software",					#3
		"Setup Grafana",					#4
		"Optimize Windows",					#5
		"Create Startup Shortcut Folder",	#6
		"Restart Computer"]					#7

	# WINDOWS BACKUP?

	match ask_select(APP_NAME,choices,True):
		case 0:
			menu_change_computer_name()
		case 1:
			menu_change_network()
		case 2:
			menu_download_software()
		case 3:
			menu_install_software()
		case 4:
			menu_setup_grafana()
		case 5:
			# print_hint("-----credit to Andy Babin-----")
			menu_optimize_windows()
		case 6:
			menu_startup_symlink()
		case 7:
			menu_restart_computer()
	
	menu_main()



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

	print_return()
	menu_main()






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

