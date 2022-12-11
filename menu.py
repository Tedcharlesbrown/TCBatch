
from constants import *
from main import *


# ------------------------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------------------------

def menu_main():

	# Menu_main = Menu("MAIN MENU", APP_NAME)
	# Menu_name = Menu("Change Computer Name", ASCII_COMPUTER_NAME)
	# Menu_ip = Menu("Change IP Addresses", ASCII_IP_ADDRESS)
	# Menu_software = Menu("Install Software", ASCII_SOFTWARE)

	# Menu_main.add_option(Menu_name)
	# Menu_main.add_option(Menu_ip)
	# Menu_main.add_option(Menu_software)

	# # Menu_name.add_option()

	# Menu_main.enter()
	# # Menu_name.enter()

	print(APP_NAME)
	print("Press number then 'ENTER' to make selection")
	print(DIVIDER)
	print("1: Change computer name")
	print("2: Change IP Addresses")
	print("3: Install Software")
	print("4: Create Startup Symlink")
	print(DIVIDER)

	user_input = input()

	if user_input == "1":
		menu_change_computer_name()
	elif user_input == "2":
		menu_change_network()
	elif user_input == "3":
		menu_install_software(True)
	elif user_input == "4":
		menu_set_startup()

# ------------------------------------------------------------------------------
# COMPUTER NAME
# ------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------
# APPLICATION INSTALL
# ------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------
# NETWORK INTERFACES 
# ------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------
# STARTUP
# ------------------------------------------------------------------------------

def menu_set_startup():
	print(DIVIDER)
	print("CREATING STARTUP SYMLINK FOLDER")
	print(DIVIDER)

	try:
		os.symlink(PATH_STARTUP_FOLDER,"Startup_Symlink")
	except:
		print("COULD NOT CREATE STARTUP FOLDER, CHECK IF ALREADY EXISTS?")
		time.sleep(1)
	menu_main()

# # ------------------------------------------------------------------------------
# # CLASS
# # ------------------------------------------------------------------------------

# class Menu:
# 	# options_list = []
# 	def __init__(self, name: str, greeting: str):
# 		self.name = name
# 		self.greeting = greeting
# 		self.options_list = []

# 	def __str__(self):
# 		return self.name

# 	def add_option(self, name: 'Menu'):
# 		self.options_list.append(name)

# 	def enter(self):
# 		print(self.greeting)
# 		print(DIVIDER)

# 		for i, option in enumerate(self.options_list):
# 			i += 1
# 			print(f"{int(i)}: {option}")
# 		print(DIVIDER)

# 		user_input = input()

# 		if user_input == "":
# 			pass
# 		else:
# 			user_input = int(user_input) - 1
# 			self.options_list[user_input].enter()