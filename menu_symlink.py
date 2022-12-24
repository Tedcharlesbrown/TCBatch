import os
import time

from classes import MENU
from constants import *

import importlib


# ---------------------------------------------------------------------------- #
#                            STARTUP FOLDER SYMLINK                            #
# ---------------------------------------------------------------------------- #

class MENU_symlink(MENU):
	def enter(self):
		print(DIVIDER)
		print(ASCII_SYMLINK)
		print(DIVIDER)
		print("CREATING STARTUP SYMLINK FOLDER")
		time.sleep(2)
		try:
			os.symlink(PATH_STARTUP_FOLDER,"Startup_Symlink")
		except:
			print("COULD NOT CREATE STARTUP FOLDER, CHECK IF ALREADY EXISTS?")
			time.sleep(1)
			
		main.menu()
		
# ---------------------------------------------------------------------------- #
#                                 BOTTOM IMPORT                                #
# ---------------------------------------------------------------------------- #
main = importlib.import_module('main')