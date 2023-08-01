from constants import *
from questions import *
from .setup_grafana import check_and_download_grafana
from .setup_grafana import install_grafana_host
from .setup_grafana import install_grafana_client

import asyncio
from src_software.download_software import get_download
from src_software.install_software import install_msi


def menu_custom_automations():
	choices = [
		"Setup Grafana and Prometheus",		#0
		"Setup VNC Server"]		#1					
	choices.append("[return]")
	cancel = choices[-1]

	match ask_select("CUSTOM AUTOMATIONS",choices,True):
		case 0:
			menu_setup_grafana()
		case 1:
			menu_install_vnc()
		case cancel:
			return
		
	return

# ---------------------------------------------------------------------------- #
#                                 SETUP GRAFANA                                #
# ---------------------------------------------------------------------------- #

def menu_setup_grafana():
	choices = [
		"Setup Host",			#0
		"Setup Client"]			#1					
	choices.append("[return]")
	cancel = choices[-1]

	match ask_select("SETUP GRAFANA",choices,True):
		case 0:
			check_and_download_grafana()
			print(DIVIDER)
			menu_setup_grafana_host()
		case 1:
			install_grafana_client()
		case cancel:
			menu_custom_automations()

	print_return()
	return


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


def menu_install_vnc():
	path_for_vnc = UTILITY_FOLDER_PATH
	vnc_found = False

	for file in os.listdir(UTILITY_FOLDER_PATH):
		file = file.lower()
		if file.startswith("tightvnc"):
			path_for_vnc += file
			vnc_found = True
			break

	if not vnc_found:
		asyncio.run(get_download(['Tight VNC']))

	first_password = ask_text("SET PASSWORD")
	confirm_password = ask_text("CONFIRM PASSWORD")

	if confirm_password != first_password:
		print_error("PASSWORDS DO NOT MATCH")
		return
	else:
		try:
			install_msi(path_for_vnc,f"/quiet /norestart SET_ALLOWLOOPBACK=1 VALUE_OF_ALLOWLOOPBACK=1 SET_USEVNCAUTHENTICATION=1 VALUE_OF_USEVNCAUTHENTICATION=1 SET_PASSWORD=1 VALUE_OF_PASSWORD={confirm_password} SET_VIEWONLYPASSWORD=1 VALUE_OF_VIEWONLYPASSWORD={confirm_password} SET_USECONTROLAUTHENTICATION=1 VALUE_OF_USECONTROLAUTHENTICATION=1 SET_CONTROLPASSWORD=1 VALUE_OF_CONTROLPASSWORD={confirm_password}")
		except:
			pass
		print("INSTALLED VNC")
	return