import os.path
import os
import subprocess
import platform
import subprocess
import time
import threading
import asyncio

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
from download_software import get_archive

from install_software import install_applications

from setup_grafana import check_and_download_grafana
from setup_grafana import install_grafana_host
from setup_grafana import install_grafana_client

from optimize_windows import remove_bloatware_apps
from optimize_windows import set_windows_features

from background_wallpaper import set_color_background
from background_wallpaper import set_tcb_background

from constants import *


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
			subprocess.call(['powershell.exe', "Rename-Computer -NewName " + user_input])


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
	choices = list_network_adapters(False)
	choices.append("[cancel]")
	interface = ask_select(ASCII_NETWORK_NAME,choices,False)

	if interface == "[cancel]":
		print_return()
		menu_main()

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

	if os.path.exists(PATH_INTEL_PROSET):
		vlan_adapters = list_network_adapters(True)
		# print(choices)
		if len(vlan_adapters) > 0:
			choices = []

			for adapter in vlan_adapters:
				choices.append(f"{adapter[0]} : {adapter[1]}")

			parent_name = vlan_adapters[ask_select("VLAN ADAPTER: ",choices,True)][1]
			vlan_id = ask_text("VLAN ID:")
			vlan_name = ask_text("VLAN NAME:")

			ps_script = fr"""Import-Module -Name 'C:\Program Files\Intel\Wired Networking\IntelNetCmdlets\IntelNetCmdlets'
			Add-IntelNetVLAN -ParentName '{parent_name}' -VlanID {vlan_id}
			Set-IntelNetVLAN -ParentName '{parent_name}' -VLANID {vlan_id} -NewVLANName '{vlan_name}'
			"""

			result = subprocess.run(['powershell', '-ExecutionPolicy', 'Unrestricted', '-Command', ps_script], capture_output=True, text=True)

		else:
			print_error("NO INTEL VLANS FOUND")
			time.sleep(1)
			print_return()
			menu_main()
	else:
		print_error("INTEL PROSET NOT FOUND")
		time.sleep(1)
		print_return()
		menu_main()
				
			# input()

# ---------------------------------------------------------------------------- #
#                                 SETUP GRAFANA                                #
# ---------------------------------------------------------------------------- #

def menu_setup_grafana():
	choices = [
		"Setup Host",			#0
		"Setup Client"]			#1					
	choices.append("[cancel]")
	cancel = choices[-1]

	match ask_select("SETUP GRAFANA",choices,True):
		case 0:
			check_and_download_grafana()
			print(DIVIDER)
			menu_setup_grafana_host()
		case 1:
			install_grafana_client()
		case cancel:
			print_return()
			menu_main()

	print_return()
	menu_main()


def menu_setup_grafana_host():
	targets = 0
	names = []
	ips = []
	
	while True:
		name = ask_text(f"{targets}: TARGET NAME:")
		if not name:
			break
		names.append(name)
		ip = ask_text(f"{targets}: {name} IP:")
		ips.append(ip)

		targets+= 1


	install_grafana_host(names, ips)


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
	menu_main()

# ---------------------------------------------------------------------------- #
#                               INSTALL SOFTWARE                               #
# ---------------------------------------------------------------------------- #

def menu_install_software():
	print(application_install_list)
	# for file in application_install_list:
	# 	if file.endswith(".bmp") or "GrafanaSetup" in file:
	# 		application_install_list.remove(file)

	application_install_list = [file for file in application_install_list if not file.endswith(".bmp") and "GrafanaSetup" not in file]


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
	"Set Windows Features",
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
			menu_set_windows_features()
		case 2:
			menu_change_background()
		case 3:
			pass
		case 4:
			pass
		case cancel:
			pass

	print_return()
	menu_main()

# ------------------------ REMOVE WINDOWS APPLICATIONS ----------------------- #
def menu_remove_bloatware():

	remove_bloatware_apps()

	print_return()
	menu_main()

# -------------------------- CHANGE WINDOWS SETTINGS ------------------------- #
def menu_set_windows_features():

	set_windows_features()

	print_return()
	menu_main()

# ------------------------- CHANGE WINDOWS BACKGROUND ------------------------ #
def menu_change_background():
	choices = ["Clear Wallpaper","Set Color", "Set TCB"]
	colors = ["Red","Orange","Yellow","Green","Blue","Purple","Pink","[cancel]"]
	choices.append("[cancel]")
	cancel = choices[-1]

	try:
		match ask_select("CHANGE WALLPAPER",choices,True):
			case 0:
				set_color_background(0,0,0)
			case 1:
					match ask_select("SET BACKGROUND COLOR",colors,True):
						case 0:
							set_color_background(100,0,0)
						case 1:
							set_color_background(100,50,0)
						case 2:
							set_color_background(100,100,0)
						case 3:
							set_color_background(0,100,0)
						case 4:
							set_color_background(0,0,100)
						case 5:
							set_color_background(50,0,100)
						case 6:
							set_color_background(100,0,75)
						case 6:
							print_return()
							menu_main()
			case 2:
				set_tcb_background()
					
			case cancel:
				pass

	except:
		print_error("COULD NOT CHANGE WALLPAPER")

			
	print_return()
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

