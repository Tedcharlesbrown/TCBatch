import subprocess
import pyuac
import re
import time
import psutil

def list_adapters():
	# Run PowerShell command to get network adapter info
	cmd = 'Get-NetAdapter | Format-Table -HideTableHeaders Name, InterfaceDescription, -Wrap'
	adapter_info = subprocess.check_output(['powershell.exe', '-Command', cmd])

	# Convert output to string and split into lines
	adapter_info = adapter_info.decode('utf-8').split('\n')

	interfaces = []

	# Loop through adapter info and print adapter name and friendly name
	for line in adapter_info:
		if line.strip():
			values = line.strip().split('  ')
			if values[0].find("Tailscale") == -1 and values[0].find("Bluetooth") == -1 and values[0].find("Local Area Connection") == -1:
				interfaces.append([values[0].strip(),values[-1].strip()])
				# Sort the list by the first element of each sublist
				interfaces = sorted(interfaces, key=lambda x: x[0])

	# for name in interfaces:
	# 	print(name)
	
	return interfaces

def main():
	list_adapters()
	input()

	ps_script = r"""Import-Module -Name 'C:\Program Files\Intel\Wired Networking\IntelNetCmdlets\IntelNetCmdlets'
			Get-IntelNetAdapter | Select-Object Name"""

	result = subprocess.run(['powershell', '-ExecutionPolicy', 'Unrestricted', '-Command', ps_script], capture_output=True, text=True)
	# Get-IntelNetAdapter | ConvertTo-Csv -NoTypeInformation -Delimiter ';'"""

	print(result)

	input()

	if result.returncode != 0:
		print(result.stderr)
		exit(1)

	# Extract the adapter names using regular expressions
	adapter_result = re.findall(r'\d+:\d+:\d+:\d+\s+(.*)\s+\d+\.\d+\s+Gbps', result.stdout)

	vlan_name = []
	connection_name = []

	# Print the adapter names
	for adapter in adapter_result:
		adapter = adapter.split("  ") 
		# print(adapter)
		for name in adapter:
			if len(name) > 1: #ignore spaces
				if name[0] == " ": #connection name
					connection_name.append(name.strip())
				else:
					vlan_name.append(name.strip())
				# adapter_list.append(name)

	print(vlan_name,connection_name)
	input()

if __name__ == "__main__":
	if not pyuac.isUserAdmin():
		print("RE-LAUNCHING AS ADMIN!")
		time.sleep(1)
		pyuac.runAsAdmin()
	else:        
		main()  # Already an admin here.