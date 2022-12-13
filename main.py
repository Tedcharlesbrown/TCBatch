import os.path
import os
import subprocess
import platform
import subprocess
import msvcrt
import time
import ipaddress
import pyuac
import winshell

from constants import *
from net import *
from name import *
from install import *
from menu import *

# -------------------------------------------------------------------------------

def main():
	folder_application_init()
	menu_main()

if __name__ == "__main__":
	if not pyuac.isUserAdmin():
		print("RE-LAUNCHING AS ADMIN!")
		time.sleep(1)
		pyuac.runAsAdmin()
	else:        
		main()  # Already an admin here.

		