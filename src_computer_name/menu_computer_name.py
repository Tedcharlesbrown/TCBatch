from constants import *
from questions import *

import platform
import subprocess


def menu_change_computer_name():
	user_input = ask_name(f"{ASCII_COMPUTER_NAME}\nCURRENT COMPUTER NAME = '{platform.node()}'")

	if user_input == "":
		pass
	else:
		if questionary.confirm(f"CHANGE NAME TO {user_input}?",qmark="",style=custom_style).ask():
			questionary.print("CHANGING NAME TO: " + user_input, style="bold")
			subprocess.call(['powershell.exe', "Rename-Computer -NewName " + user_input])


	print_return()
	return