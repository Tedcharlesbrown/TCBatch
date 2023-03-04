
import os.path
import os
import subprocess
import platform
import subprocess
import time
import threading

import pyuac

import re

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
from application_list import BLOATWARE_APPLICATION_LIST
from download_software import get_download

from install_software import install_applications

from optimize_windows import remove_bloatware_apps

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
			print_return()
			menu_main()


def menu_change_ip_address():
	choices = list_network_adapters(False)
	choices.append("[cancel]")
	interface = ask_select(ASCII_IP_ADDRESS,choices,False)

	if interface == "[cancel]":
		print_return()
		menu_main()

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
	# https://www.quirkyvirtualization.net/2017/12/29/automating-intel-network-adapter-vlan-configuration/
	questionary.print(ASCII_VLAN, style="bold")
	questionary.print("LOOKING FOR VLANS", style="bold")

	choices = list_network_adapters()
	if os.path.exists(PATH_INTEL_PROSET):
		ps_script = r"""Import-Module -Name 'C:\Program Files\Intel\Wired Networking\IntelNetCmdlets\IntelNetCmdlets'
		Get-IntelNetAdapter"""

		result = subprocess.run(['powershell', '-ExecutionPolicy', 'Unrestricted', '-Command', ps_script], capture_output=True, text=True)
		
		# print(result)

		if result.returncode != 0:
			print(result.stderr)
			exit(1)

		# Extract the adapter names using regular expressions
		adapter_result = re.findall(r'\d+:\d+:\d+:\d+\s+(.*)\s+\d+\.\d+\s+Gbps', result.stdout)

		parent_name = []
		connection_name = []
		choices = []

		# Print the adapter names
		for adapter in adapter_result:
			adapter = adapter.split("  ") 
			# print(adapter)
			for name in adapter:
				if len(name) > 1: #ignore spaces
					if name[0] == " ": #connection name
						connection_name.append(name.strip())
					else:
						parent_name.append(name.strip())
					# adapter_list.append(name)

		for i, name in enumerate(parent_name):
			if i >= len(connection_name):
				print(f"Adapter already using VLAN: {parent_name[i]}")
				choices.append(parent_name[i])
			else:
				print(f"Found compatable adapter: {connection_name[i]} : {parent_name[i]}")
				choices.append(connection_name[i])
		# print(parent_name)

		parent_name = ask_select("VLANS: ",choices,False)
		vlan_id = ask_text("VLAN ID:")
		vlan_name = ask_text("VLAN NAME:")

		input()

		ps_script = fr"""Import-Module -Name 'C:\Program Files\Intel\Wired Networking\IntelNetCmdlets\IntelNetCmdlets'
		Add-IntelNetVLAN -ParentName '{parent_name}' -VlanID {vlan_id}
		Set-IntelNetVLAN -ParentName '{parent_name}' -VLANID {vlan_id} -NewVLANName {vlan_name}
		"""

		result = subprocess.run(['powershell', '-ExecutionPolicy', 'Unrestricted', '-Command', ps_script], capture_output=True, text=True)

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
	"Remove Bloatware Applications",
	"Turn Off Windows Features",
	"Change Wallpaper",
	"Power Settings",
	"Firewall Settings",
	]
	choices.append("[cancel]")
	cancel = choices[-1]
	
	match ask_select(ASCII_OPTIMIZE_WINDOWS,choices,True):
		case 0:
			menu_remove_bloatware()
		case 1:
			print_error("WARNING, EDITING WINDOWS REGISTRY, PROCEED WITH CAUTION")
			time.sleep(1)
		case 2:
			print_error("WARNING, EDITING WINDOWS REGISTRY, PROCEED WITH CAUTION")
			time.sleep(1)
			menu_change_background()
		case cancel:
			pass

	print_return()
	menu_main()

# ------------------------ REMOVE WINDOWS APPLICATIONS ----------------------- #
def menu_remove_bloatware():
	choices = []
	for application in BLOATWARE_APPLICATION_LIST:
		choices.append(application.display)
	
	remove_bloatware_apps(ask_checkbox(ASCII_DOWNLOAD,choices,True))

	print_return()
	menu_main()

# ------------------------- CHANGE WINDOWS BACKGROUND ------------------------ #
def menu_change_background():
	choices = ["Clear Wallpaper","Set Color"]
	colors = ["Red","Orange","Yellow","Green","Blue","Purple","Pink","[cancel]"]
	choices.append("[cancel]")
	cancel = choices[-1]

	try:
		match ask_select("CHANGE WALLPAPER",choices,True):
			case 0:
					subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v WallPaper /t REG_SZ /d " " /f"""])
			case 1:
					match ask_select("SET BACKGROUND COLOR",colors,True):
						case 0:
							subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Colors" /v Background /t REG_SZ /d "100 0 0" /f"""])
						case 1:
							subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Colors" /v Background /t REG_SZ /d "100 50 0" /f"""])
						case 2:
							subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Colors" /v Background /t REG_SZ /d "100 100 0" /f"""])
						case 3:
							subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Colors" /v Background /t REG_SZ /d "0 100 0" /f"""])
						case 4:
							subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Colors" /v Background /t REG_SZ /d "0 0 100" /f"""])
						case 5:
							subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Colors" /v Background /t REG_SZ /d "50 0 100" /f"""])
						case 6:
							subprocess.call(["powershell.exe", fr"""reg add "HKEY_CURRENT_USER\Control Panel\Colors" /v Background /t REG_SZ /d "100 0 75" /f"""])
						case 6:
							print_return()
							menu_main()
			case cancel:
				pass

		
		print_error("WALLPAPER CHANGED, RESTART COMPUTER")

	except:
		print_error("COULD NOT CHANGE WALLPAPER")

			
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

