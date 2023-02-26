import subprocess

from constants import *

# ---------------------------------------------------------------------------- #
#                               INSTALL SOFTWARE                               #
# ---------------------------------------------------------------------------- #

def install_applications(user_input: str):
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