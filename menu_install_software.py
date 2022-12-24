import subprocess
import time
import os

from classes import MENU
from constants import *

import importlib

# ---------------------------------------------------------------------------- #
#                               INSTALL SOFTWARE                               #
# ---------------------------------------------------------------------------- #

class MENU_software(MENU):
	def enter(self):
		application_install_list = os.listdir(APPLICATION_FOLDER_PATH)
		print(ASCII_SOFTWARE)
		print(DIVIDER)
		if len(application_install_list) == 0:
			print("NO SOFTWARE FOUND IN 'APPLICATIONS' FOLDER!")
			time.sleep(1)
			print(DIVIDER)
			main.menu()
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
				main.menu()
			else:
				self.install_applications(user_input, application_install_list)

	def install_applications(self, user_input: str, apps: list):
		user_input = user_input.split(",")
		# print(user_input)
		for i, n in enumerate(user_input):
			if n.isdigit():
				n = int(n)
				if n <= len(apps):
					print(f"INSTALLING: {apps[n]}")
					subprocess.call([APPLICATION_FOLDER_PATH + apps[n]])
					# time.sleep(1)
					if i < len(user_input):
						print("INSTALL COMPLETE")
						time.sleep(0.5)
					else:
						print("INSTALL COMPLETE, GOING BACK TO MAIN MENU")
						time.sleep(2)
				else:
					print("INPUT IS NOT VALID")
			else:
				print("INPUT IS NOT VALID")
		main.menu()

# ---------------------------------------------------------------------------- #
#                                 BOTTOM IMPORT                                #
# ---------------------------------------------------------------------------- #
main = importlib.import_module('main')