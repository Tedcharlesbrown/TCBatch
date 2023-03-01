import subprocess

from constants import *

from questions import print_error

# ---------------------------------------------------------------------------- #
#                               INSTALL SOFTWARE                               #
# ---------------------------------------------------------------------------- #

def install_applications(user_input: str):
	if len(user_input) == 0:
		print_error("NO OPTIONS SELECTED, SELECT OPTIONS WITH <space>")
	for app in user_input:
		app_path = APPLICATION_FOLDER_PATH + app
		print(f"INSTALLING: {app_path}")
		if app_path.endswith('.msi'):
			# install MSI file using msiexec
			subprocess.call(['start', app_path], shell=True)
		elif app_path.endswith('.exe'):
			# install EXE file using subprocess
			subprocess.call([app_path])
		else:
			print("UNKNOWN FILE TYPE")