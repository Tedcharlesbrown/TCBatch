import platform
import subprocess

from class_menu import MENU
from constants import *

import importlib

# ---------------------------------------------------------------------------- #
#                                  NAME CHANGE                                 #
# ---------------------------------------------------------------------------- #

class MENU_name(MENU):
	def enter(self):
		print(DIVIDER)
		print(ASCII_COMPUTER_NAME)
		print(DIVIDER)
		print("TYPE NEW NAME AND PRESS 'ENTER', OR PRESS 'ENTER' TO CANCEL")
		print("CURRENT COMPUTER NAME = " + "'" + platform.node() + "'")
		print(DIVIDER)

		user_input = input()

		if user_input == "":
			print("GOING BACK TO MAIN MENU")
			print(DIVIDER)	
			main.menu()
		else:
			print(DIVIDER)
			print("CHANGING NAME TO: " + user_input)
			self.change_computer_name(user_input)
			print(DIVIDER)
			main.menu()

	def change_computer_name(self, computer_name: str):

		subprocess.call(['powershell.exe', "Rename-Computer -NewName " + computer_name])


# ---------------------------------------------------------------------------- #
#                                 BOTTOM IMPORT                                #
# ---------------------------------------------------------------------------- #
main = importlib.import_module('main')