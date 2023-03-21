from constants import *
from dataclasses import dataclass

# ---------------------------------------------------------------------------- #
#                               CLASS DEFINITION                               #
# ---------------------------------------------------------------------------- #

class MENU():
	# options_list = []
	def __init__(self, name: str, greeting: str):
		self.name = name
		self.greeting = greeting
		self.options_list = []

	def __str__(self):
		return self.name

	def add_option(self, name: 'Menu'):
		self.options_list.append(name)

	def enter(self):
		print(self.greeting)
		print(DIVIDER)	
		self.list_options()

	def list_options(self):
		for i, option in enumerate(self.options_list):
			i += 1
			print(f"{int(i)}: {option}")
		print(DIVIDER)
		self.wait_for_input()

	def wait_for_input(self):
		user_input = input()

		if user_input == "":
			pass
		else:
			user_input = int(user_input) - 1
			self.options_list[user_input].enter()


# ---------------------------------------------------------------------------- #
#                              CLASS: APPLICATION                              #
# ---------------------------------------------------------------------------- #
@dataclass
class APPLICATION:
	display: str
	name: str
	link: str

@dataclass
class BLOATWARE:
	display: str
	name: list