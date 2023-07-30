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
		app_path = UTILITY_FOLDER_PATH + app
		print(f"INSTALLING: {app_path}")
		if app_path.endswith('.msi'):
			install_msi(app_path,"")
		elif app_path.endswith('.exe'):
			install_exe(app_path)
		else:
			print("UNKNOWN FILE TYPE")


def install_exe(path: str):
	subprocess.call([path])

def install_msi(path: str, parameters: str):
	path = path.replace('/', '\\')
	# os.chdir(os.path.dirname(path)) #UNTESTED WITH NORMAL MSI (NON WINDOWS EXPORTER)

	command = f'msiexec /i "{path}" {parameters}'
	subprocess.call(command, shell=True)
