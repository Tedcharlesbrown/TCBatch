from constants import *
from questions import *
from src_network.change_ip import *

import subprocess
import time

def menu_change_network():
	choices = [
		"Change IP Addresses",
		"Change Adapter Names",
		"Add VLANS"]
	
	choices.append("[return]")
	cancel = choices[-1]
	
	match ask_select(ASCII_NETWORK_SETTINGS,choices,True):
		case 0:
			menu_change_ip_address()
			menu_change_network()
		case 1:
			menu_change_adapter_name()
			menu_change_network()
		case 2:
			menu_add_vlans()
			menu_change_network()
		case cancel:
			print_return()
			return


def menu_change_ip_address():
	choices = list_network_adapters(False)
	choices.append("[return]")
	interface = ask_select(ASCII_IP_ADDRESS,choices,False)

	if interface == "[return]":
		print_return()
		return

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
	return

def menu_change_adapter_name():
	choices = list_network_adapters(False)
	choices.append("[return]")
	interface = ask_select(ASCII_NETWORK_NAME,choices,False)

	if interface == "[return]":
		print_return()
		return

	user_input = ask_name(f"CURRENT ADAPTER NAME = '{interface}'")

	if user_input == "":
			pass
	else:
		if questionary.confirm(f"CHANGE NAME TO {user_input}?",qmark="",style=custom_style).ask():
			questionary.print("CHANGING NAME TO: " + user_input, style="bold")
			cmd = f'netsh interface set interface name="{interface}" newname="{user_input}"'
			subprocess.call(cmd, shell=True)

	print_return()
	return

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
			return
	else:
		print_error("INTEL PROSET NOT FOUND")
		time.sleep(1)
		print_return()
		return
				
			# input()