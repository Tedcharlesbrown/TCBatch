import os.path
import os
import subprocess
import platform
import subprocess
import msvcrt
import time
import ipaddress


APP_NAME = "TCB - Quick Setup"
DIVIDER = "----------"
PATH_BATCH_FOLDER = "batch_files"

SUBNET_LIST = ["0.0.0.0", "128.0.0.0", "192.0.0.0", "224.0.0.0", "240.0.0.0", "248.0.0.0", "252.0.0.0", "254.0.0.0", "255.0.0.0", "255.128.0.0", "255.192.0.0", "255.224.0.0", "255.240.0.0", "255.248.0.0", "255.252.0.0", "255.254.0.0", "255.255.0.0", "255.255.128.0",
			   "255.255.192.0", "255.255.224.0", "255.255.240.0", "255.255.248.0", "255.255.252.0", "255.255.254.0", "255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240", "255.255.255.248", "255.255.255.252", "255.255.255.254", "255.255.255.255"]

SUBNET_MAP = {
	"a": "255.0.0.0",
	"b": "255.255.0.0",
	"c": "255.255.255.0",
}

# NETWORK INTERFACES ------------------------------------------------------------------------------


def get_network_adapters():
	# Create an empty list to store the interface names
	interfaces = []

	# Run the "ipconfig" command and save the output
	output = subprocess.check_output("ipconfig")

	# Decode the output from bytes to a string
	output = output.decode("utf-8")

	# Split the output into a list of lines
	for line in output.split("\n"):

		# Check if the line contains the word "adapter"
		if "adapter" in line:

			# Split the line on the word "adapter" and extract the adapter name
			adapter = line.split("adapter ")
			adapter = adapter[1].split(":")

			# Add the adapter name to the list of interfaces
			interfaces.append(adapter[0])

	# Return the list of interfaces
	return interfaces


def default_subnet(ip_input: str):
	# split the IP address by the period character and take the first item in the resulting list
	octet_one = int(ip_input.split('.')[0])
	# if the first octet is less than or equal to 127
	if octet_one <= 127:
		# return the subnet mask 255.0.0.0
		return "255.0.0.0"

	# if the first octet is between 128 and 191
	elif octet_one >= 128 and octet_one <= 191:
		# return the subnet mask 255.255.0.0
		return "255.255.0.0"

	# if the first octet is greater than or equal to 192
	elif octet_one >= 192:
		# return the subnet mask 255.255.255.0
		return "255.255.255.0"


# def parse_subnet(subnet_input: str):
#     subnet = ""
#     if subnet_input.lower() == "a":
#         subnet = "255.0.0.0"
#     elif subnet_input.lower() == "b":
#         subnet = "255.255.0.0"
#     elif subnet_input.lower() == "c":
#         subnet = "255.255.255.0"
#     elif int(subnet_input) <= 33:
#         subnet = SUBNET_LIST[int(subnet_input)]
#     else:
#         subnet = subnet_input
#     return subnet


def parse_subnet(subnet_input: str):

	# convert the input to lowercase to make it case-insensitive
	subnet_input = subnet_input.lower()

	# try to convert the input to an integer if it cannot be converted, the ValueError exception will be raised
	try:
		subnet_index = int(subnet_input)
	except ValueError:
		subnet_index = None

	# if the input is in the subnet map, return the corresponding subnet mask
	if subnet_input in SUBNET_MAP:
		return SUBNET_MAP[subnet_input]

	# if the input can be converted to an integer and is less than or equal to 33,
	# return the subnet mask at the specified index in the SUBNET_LIST array
	elif subnet_index is not None and subnet_index <= 33:
		return SUBNET_LIST[subnet_index]

	# if the input does not match any of the above conditions,
	# return the input subnet mask
	else:
		return subnet_input


def parse_gateway(addresses: list):
	# split the first address by the period character and store the resulting list
	ip = addresses[0].split('.')
	gateway = addresses[2]
	if len(gateway) <= 12:
		if '.' not in gateway:
			gateway = f"{ip[0]}.{ip[1]}.{ip[2]}.{gateway}"
		else:
			gateway = gateway.split('.')
			if len(gateway) == 2:
				gateway = f"{ip[0]}.{ip[1]}.{ip[2]}.{gateway[1].replace('.','')}"
			elif len(gateway) == 3:
				gateway = f"{ip[0]}.{ip[1]}.{gateway[1].replace('.','')}.{gateway[2].replace('.','')}"
			elif len(gateway) == 4:
				gateway = f"{ip[0]}.{gateway[1].replace('.','')}.{gateway[2].replace('.','')}.{gateway[3].replace('.','')}"
	return gateway


def parse_dns(dns_input: str, is_primary: bool):
	dns = ""
	if len(dns_input) == 0:
		if is_primary:
			dns = "1.1.1.1"
		else:
			dns = "8.8.8.8"
	else:
		dns = dns_input

	return dns


def change_network_adapters(interface: str, addresses: list):
	cmd = ""

	if addresses[0].lower() == "dhcp":
		cmd = "netsh interface ip set address \"" + interface + "\" source=dhcp"

	if len(addresses) == 1:
		cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + default_subnet(addresses[0])

	elif len(addresses) == 2:
		cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1])

	elif len(addresses) == 3:
		cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1]) + " " + parse_gateway(addresses)

	elif len(addresses) == 4:
		cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1]) + " " + parse_gateway(addresses)
		cmd += "\r"
		cmd += "netsh interface ip set dns \"" + interface + "\" static " + parse_dns(addresses[3], True)

	elif len(addresses) == 5:
		cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1]) + " " + parse_gateway(addresses)
		cmd += "\r"
		cmd += "netsh interface ip set dns \"" + interface + "\" static " + parse_dns(addresses[3], True)
		cmd += "\r"
		cmd += "netsh interface ip add dns \"" + interface + "\" " + parse_dns(addresses[3], False) + " index=2"

	subprocess.call(["powershell.exe", cmd])


# COMPUTER NAME ------------------------------------------------------------------------------

def change_computer_name(computer_name: str):

	subprocess.call(['powershell.exe', "Rename-Computer -NewName " + computer_name])

# APPLICATION INSTALL------------------------------------------------------------------------


def application_init():
	application_folder_path = 'applications'
	if not os.path.exists(application_folder_path):
		os.makedirs(application_folder_path)
	else:
		application_install_list = os.listdir(application_folder_path)
		print(application_install_list)
		# subprocess.run(["applications/"+application_install_list[0], ""])
		# subprocess.run(["applications/"+application_install_list[1], ""])


# msiexec.exe /i "C:\Users\Rkdns\Desktop\TCB_BatchInstall\applications\SpotifySetup.exe"


def menu_main():
	print("1: Change computer name")
	print("2: Change IP Addresses")
	print("3: Install Software")
	print(DIVIDER)

	user_input = input()

	if user_input == "1":
		menu_change_computer_name()
	elif user_input == "2":
		menu_change_network()
	elif user_input == "3":
		print("SOFTWARE INSTALL: NOT IMPLEMENTED YET")
		print(DIVIDER)
		menu_main()


def menu_change_computer_name():
	print(DIVIDER)
	print("CHANGING COMPUTER NAME")
	print(DIVIDER)
	time.sleep(1)
	print("TYPE NEW NAME AND PRESS 'ENTER', OR PRESS 'ENTER' TO CANCEL")
	print("CURRENT COMPUTER NAME = " + "'" + platform.node() + "'")
	print(DIVIDER)

	user_input = input()

	if user_input == "":
		print("GOING BACK TO MAIN MENU")
		print(DIVIDER)
		menu_main()
	else:
		print(DIVIDER)
		print("CHANGING NAME TO: " + user_input)
		change_computer_name(user_input)
		time.sleep(1)
		print("NAME WILL UPDATE ON RESTART")
		print(DIVIDER)
		time.sleep(1)
		menu_main()


def menu_change_network():
	print(DIVIDER)
	print("CHANGING IP ADDRESSES")
	print("TYPE THE NUMBER OF THE INTERFACE YOU WOULD LIKE TO CHANGE, OR PRESS 'ENTER' TO CANCEL")
	network_adapters = get_network_adapters()
	for i, interface in enumerate(network_adapters):
		print(str(i) + ": " + "\"" + interface + "\"")
	print(DIVIDER)

	user_input = input()
	selected_network_adapter = ""

	if user_input == "":
		print("GOING BACK TO MAIN MENU")
		print(DIVIDER)
		menu_main()
	elif user_input.isdigit():
		print(DIVIDER)
		selected_network_adapter = network_adapters[int(user_input)]
		print("EDITING ADAPTER: " + selected_network_adapter)
		print("USE FOLLOWING SYNTAX TO CHANGE NETWORK ADAPTER")
		print("\"IP ADDRESS/SUBNET/GATEWAY/PRIMARY DNS/SECONDARY DNS\"")
		# print("\"192.168.1.11/255.255.255.0/192.168.1.1\"")
		print(DIVIDER)
		user_input = input()
		if user_input == "":
			print("GOING BACK")
			menu_change_network()
		else:
			addresses = user_input.split("/")
			if user_input == "":
				print("GOING BACK")
				menu_change_network()
			else:
				change_network_adapters(selected_network_adapter, addresses)


print(APP_NAME)
print("Press number then 'ENTER' to make selection")
print(DIVIDER)
menu_main()
