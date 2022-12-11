from constants import *
from main import *

# ------------------------------------------------------------------------
# APPLICATION INSTALL
# ------------------------------------------------------------------------

def folder_application_init():
	if not os.path.exists(APPLICATION_FOLDER_PATH):
		os.makedirs(APPLICATION_FOLDER_PATH)
		print(DIVIDER)
		print("APPLICATION INSTALL FOLDER NOT FOUND - CREATING ONE")
		print(DIVIDER)

def install_applications(user_input: str, apps: list):
	user_input = user_input.split(",")
	for n in user_input:
		if n.isdigit():
			n = int(n)
			if n <= len(apps):
				subprocess.call([APPLICATION_FOLDER_PATH + apps[n]])
				time.sleep(1)
			else:
				print("INPUT IS NOT VALID")
		else:
			print("INPUT IS NOT VALID")
	menu_install_software(False)