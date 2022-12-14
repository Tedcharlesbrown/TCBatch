import subprocess


from classes import MENU
from constants import *

import importlib

# ---------------------------------------------------------------------------- #
#                                  IP ADDRESS                                  #
# ---------------------------------------------------------------------------- #

class MENU_ip(MENU):
	def enter(self):
		print(DIVIDER)
		# print("CHANGING IP ADDRESSES")
		print(ASCII_IP_ADDRESS)
		print(DIVIDER)
		print("TYPE THE NUMBER OF THE INTERFACE YOU WOULD LIKE TO CHANGE, OR PRESS 'ENTER' TO CANCEL")
		network_adapters = self.get_network_adapters()
		for i, interface in enumerate(network_adapters):
			print(str(i) + ": " + "\"" + interface + "\"")
		print(DIVIDER)

		user_input = input()
		selected_network_adapter = ""

		if user_input == "":
			print("GOING BACK TO MAIN MENU")
			print(DIVIDER)
			main.menu()
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
				main.menu()
			else:
				addresses = user_input.split("/")
				# if user_input == "":
				# 	print("GOING BACK")
				# 	menu_main()
				# else:
				self.change_network_adapters(selected_network_adapter, addresses)

	def get_network_adapters(self):
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

	def default_subnet(self,ip_input: str):
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


	def parse_subnet(self,subnet_input: str):

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


	def parse_gateway(self,addresses: list):
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


	def parse_dns(self, dns_input: str, is_primary: bool):
		dns = ""
		if len(dns_input) == 0:
			if is_primary:
				dns = "1.1.1.1"
			else:
				dns = "8.8.8.8"
		else:
			dns = dns_input

		return dns


	def change_network_adapters(self, interface: str, addresses: list):
		cmd = ""

		if addresses[0].lower() == "dhcp":
			cmd = "netsh interface ip set address \"" + interface + "\" dhcp"

		elif len(addresses) == 1:
			cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + self.default_subnet(addresses[0])

		elif len(addresses) == 2:
			cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + self.parse_subnet(addresses[1])

		elif len(addresses) == 3:
			cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + self.parse_subnet(addresses[1]) + " " + self.parse_gateway(addresses)

		elif len(addresses) == 4:
			cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + self.parse_subnet(addresses[1]) + " " + self.parse_gateway(addresses)
			cmd += "\r"
			cmd += "netsh interface ip set dns \"" + interface + "\" static " + self.parse_dns(addresses[3], True)

		elif len(addresses) == 5:
			cmd = "netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + self.parse_subnet(addresses[1]) + " " + self.parse_gateway(addresses)
			cmd += "\r"
			cmd += "netsh interface ip set dns \"" + interface + "\" static " + self.parse_dns(addresses[3], True)
			cmd += "\r"
			cmd += "netsh interface ip add dns \"" + interface + "\" " + self.parse_dns(addresses[3], False) + " index=2"

		subprocess.call(["powershell.exe", cmd])
		main.menu()

# ---------------------------------------------------------------------------- #
#                                 BOTTOM IMPORT                                #
# ---------------------------------------------------------------------------- #
main = importlib.import_module('main')