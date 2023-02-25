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
				print(str(i + 1) + ": " + "\"" + app + "\"")
			print(DIVIDER)

			user_input = input()
			if user_input == "":
				print("GOING BACK TO MAIN MENU")
				print(DIVIDER)
				main.menu()
			else:
				self.install_applications(user_input, application_install_list)


	def install_applications(self, user_input: str, apps: list):
		if user_input == "0" or user_input.lower() == "all":
			print(apps)
			user_input = ""
			for i in range(len(apps)):
				user_input += str(i + 1) + ","	
				
		user_input = user_input.split(",")
		for i, n in enumerate(user_input):
			if n.isdigit():
				n = int(n) - 1
				if n <= len(apps):
					app_path = APPLICATION_FOLDER_PATH + apps[n]
					print(f"INSTALLING: {app_path}")
					if app_path.endswith('.msi'):
						# install MSI file using msiexec
						subprocess.call(['start', app_path], shell=True)
					elif app_path.endswith('.exe'):
						# install EXE file using subprocess
						subprocess.call([app_path])
					else:
						print("UNKNOWN FILE TYPE")
						continue

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