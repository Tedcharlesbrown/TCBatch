import os.path
import subprocess



# subprocess.call([r'current_date.bat'])


# APPLICATION INSTALL------------------------------------------------------------------------
application_folder_path = 'applications' 
if not os.path.exists(application_folder_path):
    os.makedirs(application_folder_path)
else:
	application_install_list = os.listdir(application_folder_path)
	print(application_install_list)
	# subprocess.run(["applications/"+application_install_list[0], ""])
	# subprocess.run(["applications/"+application_install_list[1], ""])


# msiexec.exe /i "C:\Users\Rkdns\Desktop\TCB_BatchInstall\applications\SpotifySetup.exe"
