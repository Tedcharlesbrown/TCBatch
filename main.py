
import os.path
import os
import subprocess
import platform
import subprocess
import time
import threading

import pyuac

import questionary

from questions import ask_select
from questions import ask_checkbox
from questions import ask_text
from questions import ask_name
from questions import print_error
from questions import print_return
from questions import print_hint
from questions import custom_style

from change_ip import list_network_adapters
from change_ip import set_network_adapter

from application_list import APPLICATION_DOWNLOAD_LIST
from application_list import MICROSOFT_APPLICATION_LIST
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
	# choices = [
	# "Change Computer Name", 
	# "Change Network Settings",
	# "Download Software",
	# "Install Software",
	# "Create Startup Symlink Folder",
	# "Restart Computer"]

	# # WINDOWS BACKUP?

	# match ask_select(APP_NAME,choices,True):
	# 	case 0:
	# 		menu_change_computer_name()
	# 	case 1:
	# 		menu_change_network()
	# 	case 2:
	# 		menu_download_software()
	# 	case 3:
	# 		menu_install_software()
	# 	case 4:
	# 		menu_startup_symlink()
	# 	case 5:
	# 		menu_restart_computer()

	choices = [
		"Change Computer Name", 
		"Change Network Settings",
		"Download Software",
		"Install Software",
		"Optimize Windows",
		"Create Startup Symlink Folder",
		"Restart Computer"]

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
			print_hint("-----credit to Andy Babin-----")
			menu_optimize_windows()
		case 5:
			menu_startup_symlink()
		case 6:
			menu_restart_computer()


# ---------------------------------------------------------------------------- #
#                             CHANGE COMPUTER NAME                             #
# ---------------------------------------------------------------------------- #

def menu_change_computer_name():
	user_input = ask_name(f"{ASCII_COMPUTER_NAME}\nCURRENT COMPUTER NAME = '{platform.node()}'")

	if user_input == "":
		pass
	else:
		if questionary.confirm(f"CHANGE NAME TO {user_input}?",qmark="",style=custom_style).ask():
			questionary.print("CHANGING NAME TO: " + user_input, style="bold")
			# subprocess.call(['powershell.exe', "Rename-Computer -NewName " + user_input])

	print_return()
	menu_main()

# ---------------------------------------------------------------------------- #
#                                CHANGE NETWORK                                #
# ---------------------------------------------------------------------------- #

def menu_change_network():
	choices = [
		"Change IP Addresses",
		"Change Adapter Names",
		"Add VLANS"]
	
	choices.append("[cancel]")
	cancel = choices[-1]
	match ask_select(ASCII_NETWORK_SETTINGS,choices,True):
		case 0:
			menu_change_ip_address()
		case 1:
			menu_change_adapter_name()
		case 2:
			menu_add_vlans()
		case cancel:
			menu_main()


def menu_change_ip_address():
	choices = list_network_adapters()
	interface = ask_select(ASCII_IP_ADDRESS,choices,False)

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

	print_return()
	menu_main()

def menu_change_adapter_name():
	choices = list_network_adapters()
	interface = ask_select(ASCII_NETWORK_NAME,choices,False)

	user_input = ask_name(f"CURRENT ADAPTER NAME = '{interface}'")

	if user_input == "":
			pass
	else:
		if questionary.confirm(f"CHANGE NAME TO {user_input}?",qmark="",style=custom_style).ask():
			questionary.print("CHANGING NAME TO: " + user_input, style="bold")
			cmd = f'netsh interface set interface name="{interface}" newname="{user_input}"'
			subprocess.call(cmd, shell=True)

	print_return()
	menu_main()

def menu_add_vlans():
	questionary.print(ASCII_VLAN, style="bold")
	questionary.print("LOOKING FOR VLANS", style="bold")

	choices = list_network_adapters()
	if os.path.exists(PATH_INTEL_PROSET):
		ps_script = r"""Import-Module -Name 'C:\Program Files\Intel\Wired Networking\IntelNetCmdlets\IntelNetCmdlets'
		Get-IntelNetAdapter"""
		# Get-IntelNetAdapter | ConvertTo-Csv -NoTypeInformation -Delimiter ';'"""

		result = subprocess.run(['powershell', '-ExecutionPolicy', 'Unrestricted', '-Command', ps_script], capture_output=True, text=True)

		if result.returncode != 0:
			print(result.stderr)
			exit(1)

		print(result)
		input()
		# result = str(result).split(";")

		# valid_adapters = []

		# for choice in choices:
		# 	if any(choice in res for res in result):
		# 		valid_adapters.append(choice)
		
		# ask_select("FOUND INTEL CAPABLE VLANS",valid_adapters,False)
		# 4. Type: Add-IntelNetVLAN
		# 5. copy and paste an adapter name for parent (in this case the 1G adapter)
		# 6. press enter when prompted for another parent name (this skips adding another)
		# 7. for VLAN ID, one at a time enter 0 followed by enter, 10 followed by enter, 30, 40, 70 (each followed by enter)
		# 8. press enter once step 7 is complete
		# 9. Windows will take a moment and then all of the virtual NICs will appear as new adapters
		# 10. Set IPs according to Google sheet and label as: A - 0 Control, A - 10 d3Net, A - 30 Automation, A - 40 Artnet, A - 70 Projection

		# """
		# Add-IntelNetVLAN
		# Add-IntelNetVLAN -InterfaceName "Ethernet" -VlanID 10 -VirtualAdapterName "VLAN10"
		# Add-IntelNetVLAN -InterfaceName "Ethernet" -VlanID 20 -VirtualAdapterName "VLAN20"
		# Add-IntelNetVLAN -InterfaceName "Ethernet" -VlanID 30 -VirtualAdapterName "VLAN30"
		# """
	else:
		print_error("NO INTEL VLANS FOUND")
		time.sleep(1)
		menu_main()
			
		# input()


# ---------------------------------------------------------------------------- #
#                               DOWNLOAD SOFTWARE                              #
# ---------------------------------------------------------------------------- #

def menu_download_software():
	choices = []
	for application in APPLICATION_DOWNLOAD_LIST:
		choices.append(application.display)
	
	get_download(ask_checkbox(ASCII_DOWNLOAD,choices,False))

	print_return()
	menu_main()

# ---------------------------------------------------------------------------- #
#                               INSTALL SOFTWARE                               #
# ---------------------------------------------------------------------------- #

def menu_install_software():
	application_install_list = os.listdir(APPLICATION_FOLDER_PATH)
	if len(application_install_list) == 0:
		# questionary.print("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!", style="fg:#C00000 bold")
		print_error("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!")
		time.sleep(1)
	else:
		install_applications(ask_checkbox(ASCII_SOFTWARE, application_install_list,False))

	print_return()
	menu_main()

# ---------------------------------------------------------------------------- #
#                               OPTIMIZE WINDOWS                               #
# ---------------------------------------------------------------------------- #

def menu_optimize_windows():
	choices = [
	"Remove Windows Applications",
	"Turn Off Windows Features",
	"Change Wallpaper",
	"Power Settings",
	"Firewall Settings",
	]
	choices.append("[cancel]")
	cancel = choices[-1]
	
	match ask_select(ASCII_OPTIMIZE_WINDOWS,choices,True):
		case 0:
			menu_remove_windows_apps()
		case 1:
			print_error("WARNING, EDITING WINDOWS REGISTRY, PROCEED WITH CAUTION")
			time.sleep(1)
		case 2:
			pass
		case cancel:
			pass

	menu_main()

# ------------------------ REMOVE WINDOWS APPLICATIONS ----------------------- #
def menu_remove_windows_apps():
	choices = []
	for application in MICROSOFT_APPLICATION_LIST:
		choices.append(application[10:])
	
	ask_checkbox(ASCII_DOWNLOAD,choices,False)

	print_return()
	menu_main()

# ---------------------------------------------------------------------------- #
#                              SET STARTUP SYMLINK                             #
# ---------------------------------------------------------------------------- #

def menu_startup_symlink():
	questionary.print("CREATING STARTUP SYMLINK FOLDER", style="bold")
	try:
		os.symlink(PATH_STARTUP_FOLDER,"Startup_Symlink")
	except:
		time.sleep(1)
		questionary.print("COULD NOT CREATE STARTUP FOLDER, CHECK IF ALREADY EXISTS?", style="fg:#C00000 bold")
	time.sleep(1)

	print_return()
	menu_main()

# ---------------------------------------------------------------------------- #
#                               RESTART COMPUTER                               #
# ---------------------------------------------------------------------------- #

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
		menu_main()

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
	os.system("shutdown /r")




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

