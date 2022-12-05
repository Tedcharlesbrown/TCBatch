import os.path
import subprocess

import psutil

# NETWORK INTERFACES ------------------------------------------------------------------------------
network_interfaces = list(psutil.net_if_addrs().keys())

network_interface = ""
ip_address = ""
subnet_address = ""
gateway_address = ""

set_ip = "netsh interface ip set address \"" + network_interface + "\" static " + ip_address + " " + subnet_address + " " + gateway_address 
set_dns_1 = "netsh interface ipv4 set dns \"" + network_interface + "\" static " + subnet_address
set_dns_2 = "netsh interface ipv4 add dns \"" + network_interface + "\" " + gateway_address + " index=2"

# netsh interface ip set address "Ethernet 3" static 192.168.1.26 255.255.255.0 192.168.1.1
# netsh interface ipv4 set dns "Ethernet 3" static 1.1.1.1
# netsh interface ipv4 add dns "Ethernet 3" 8.8.8.8 index=2

# COMPUTER NAME ------------------------------------------------------------------------------

computer_name = ""

set_computer_name = "WMIC ComputerSystem where Name= \"" + computer_name + "\" call Rename Name=NewName"

# WMIC ComputerSystem where Name="COMPUTER-NAME" call Rename Name=NewName


# BATCH FILES ------------------------------------------------------------------------------
batch_folder_path = "batch_files"
if not os.path.exists(batch_folder_path):
		os.makedirs(batch_folder_path)

subprocess.call([batch_folder_path+'\hello_world.bat'])


# APPLICATION INSTALL------------------------------------------------------------------------

def application_init():
	application_folder_path = 'applications' 
	if not os.path.exists(application_folder_path):
		os.makedirs(application_folder_path)
	else:
		application_install_list = os.listdir(application_folder_path)
		print(application_install_list)
		# subprocess.run(["applications/"+application_install_list[0], ""])
		# subprocess.run(["applications/"+application_install_list[1], ""])


# msiexec.exe /i "C:\Users\Rkdns\Desktop\TCB_BatchInstall\applications\SpotifySetup.exe"
