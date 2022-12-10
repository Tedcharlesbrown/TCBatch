import os.path
import os
import subprocess
import platform
import subprocess
import msvcrt
import time
import ipaddress
import pyuac


APP_NAME = "TCB - Quick Setup"
DIVIDER = "----------"
PATH_BATCH_FOLDER = "batch_files"

APPLICATION_INSTALL_LIST = []
APPLICATION_FOLDER_PATH = 'applications/'

SUBNET_LIST = ["0.0.0.0", "128.0.0.0", "192.0.0.0", "224.0.0.0", "240.0.0.0", "248.0.0.0", "252.0.0.0", "254.0.0.0", "255.0.0.0", "255.128.0.0", "255.192.0.0", "255.224.0.0", "255.240.0.0", "255.248.0.0", "255.252.0.0", "255.254.0.0", "255.255.0.0", "255.255.128.0",
			   "255.255.192.0", "255.255.224.0", "255.255.240.0", "255.255.248.0", "255.255.252.0", "255.255.254.0", "255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240", "255.255.255.248", "255.255.255.252", "255.255.255.254", "255.255.255.255"]

SUBNET_MAP = {
	"a": "255.0.0.0",
	"b": "255.255.0.0",
	"c": "255.255.255.0",
}
# https://patorjk.com/software/taag/#p=display&h=0&v=0&f=Old%20Banner&t=TCBATCH
APP_NAME = """

  _____ ___ ___       _      _    
 |_   _/ __| _ ) __ _| |_ __| |_  
   | || (__| _ \/ _` |  _/ _| ' \ 
   |_| \___|___/\__,_|\__\__|_||_|
								  

"""

ASCII_COMPUTER_NAME = """

   ___ _  _   _   _  _  ___ ___ _  _  ___    ___ ___  __  __ ___ _   _ _____ ___ ___   _  _   _   __  __ ___ 
  / __| || | /_\ | \| |/ __|_ _| \| |/ __|  / __/ _ \|  \/  | _ \ | | |_   _| __| _ \ | \| | /_\ |  \/  | __|
 | (__| __ |/ _ \| .` | (_ || || .` | (_ | | (_| (_) | |\/| |  _/ |_| | | | | _||   / | .` |/ _ \| |\/| | _| 
  \___|_||_/_/ \_\_|\_|\___|___|_|\_|\___|  \___\___/|_|  |_|_|  \___/  |_| |___|_|_\ |_|\_/_/ \_\_|  |_|___|
																											  

"""

ASCII_IP_ADDRESS = """
   ___ _  _   _   _  _  ___ ___ _  _  ___   ___ ___     _   ___  ___  ___ ___ ___ ___ 
  / __| || | /_\ | \| |/ __|_ _| \| |/ __| |_ _| _ \   /_\ |   \|   \| _ \ __/ __/ __|
 | (__| __ |/ _ \| .` | (_ || || .` | (_ |  | ||  _/  / _ \| |) | |) |   / _|\__ \__ \\
  \___|_||_/_/ \_\_|\_|\___|___|_|\_|\___| |___|_|   /_/ \_\___/|___/|_|_\___|___/___/                                                                            
"""

ASCII_SOFTWARE = """
  ___ _  _ ___ _____ _   _    _    ___ _  _  ___   ___  ___  ___ _______      ___   ___ ___ 
 |_ _| \| / __|_   _/_\ | |  | |  |_ _| \| |/ __| / __|/ _ \| __|_   _\ \    / /_\ | _ \ __|
  | || .` \__ \ | |/ _ \| |__| |__ | || .` | (_ | \__ \ (_) | _|  | |  \ \/\/ / _ \|   / _| 
 |___|_|\_|___/ |_/_/ \_\____|____|___|_|\_|\___| |___/\___/|_|   |_|   \_/\_/_/ \_\_|_\___|
																							
"""

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

	# store the third address as the gateway
	gateway = addresses[2]

	# if the length of the gateway address is less than or equal to 12
	if len(gateway) <= 12:
		# if the gateway address does not contain a period,
		# build the gateway address using the first three octets of the first address
		if '.' not in gateway:
			gateway = f"{ip[0]}.{ip[1]}.{ip[2]}.{gateway}"

		# if the gateway address contains one or more periods,
		# split the gateway address by the period character and store the resulting list
		else:
			gateway = gateway.split('.')

			# if the gateway address has two octets,
			# build the gateway address using the first three octets of the first address and the second octet of the gateway address
			if len(gateway) == 2:
				gateway = f"{ip[0]}.{ip[1]}.{ip[2]}.{gateway[1].replace('.','')}"

			# if the gateway address has three octets,
			# build the gateway address using the first and second octets of the first address and the second and third octets of the gateway address
			elif len(gateway) == 3:
				gateway = f"{ip[0]}.{ip[1]}.{gateway[1].replace('.','')}.{gateway[2].replace('.','')}"

			# if the gateway address has four octets,
			# build the gateway address using the first octet of the first address and the second, third, and fourth octets of the gateway address
			elif len(gateway) == 4:
				gateway = f"{ip[0]}.{gateway[1].replace('.','')}.{gateway[2].replace('.','')}.{gateway[3].replace('.','')}"

	# return the gateway address
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
		cmd = "netsh interface ip set address \"" + interface + "\" dhcp"

	elif len(addresses) == 1:
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
	menu_main()


# COMPUTER NAME ------------------------------------------------------------------------------

def change_computer_name(computer_name: str):

	subprocess.call(['powershell.exe', "Rename-Computer -NewName " + computer_name])

# APPLICATION INSTALL------------------------------------------------------------------------


def folder_application_init():
	if not os.path.exists(APPLICATION_FOLDER_PATH):
		os.makedirs(APPLICATION_FOLDER_PATH)
		print(DIVIDER)
		print("APPLICATION INSTALL FOLDER NOT FOUND - CREATING ONE")
		print(DIVIDER)

def install_applications(user_input: str, apps: list):
	user_input = user_input.split(",")
	for n in user_input:
		if n.isdigit():
			n = int(n)
			if n <= len(apps):
				subprocess.call([APPLICATION_FOLDER_PATH + apps[n]])
				time.sleep(1)
			else:
				print("INPUT IS NOT VALID")
		else:
			print("INPUT IS NOT VALID")
	menu_install_software(False)

def menu_main():
	print(APP_NAME)
	print("Press number then 'ENTER' to make selection")
	print(DIVIDER)
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
		menu_install_software(True)


def menu_change_computer_name():
	print(DIVIDER)
	# print("CHANGING COMPUTER NAME")
	print(ASCII_COMPUTER_NAME)
	print(DIVIDER)
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
		print("NAME WILL UPDATE ON RESTART")
		print(DIVIDER)
		menu_main()


def menu_change_network():
	print(DIVIDER)
	# print("CHANGING IP ADDRESSES")
	print(ASCII_IP_ADDRESS)
	print(DIVIDER)
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


def menu_install_software(ascii: bool):
	application_install_list = os.listdir(APPLICATION_FOLDER_PATH)
	if ascii:
		print(ASCII_SOFTWARE)
	print(DIVIDER)
	if len(application_install_list) == 0:
		print("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!")
		time.sleep(1)
		print(DIVIDER)
		menu_main()
	else:
		print("TYPE THE NUMBER OF THE SOFTWARE YOU WOULD LIKE TO INSTAll, OR PRESS 'ENTER' TO CANCEL")
		for i, app in enumerate(application_install_list):
			print(str(i) + ": " + "\"" + app + "\"")
		print(DIVIDER)

		# print(APPLICATION_INSTALL_LIST)
		user_input = input()
		if user_input == "":
			print("GOING BACK TO MAIN MENU")
			print(DIVIDER)
			menu_main()
		else:
			install_applications(user_input, application_install_list)

# -------------------------------------------------------------------------------

def main():
	folder_application_init()
	menu_main()
# if isAdmin():

# else:
# 	print(DIVIDER)
# 	print("PLEASE RE-RUN SCRIPT AS ADMIN!")
# 	time.sleep(2)

if __name__ == "__main__":
	if not pyuac.isUserAdmin():
		print("RE-LAUNCHING AS ADMIN!")
		time.sleep(1)
		pyuac.runAsAdmin()
	else:        
		main()  # Already an admin here.