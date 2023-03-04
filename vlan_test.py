import subprocess
import pyuac
import re
import time

def main():
	ps_script = r"""Import-Module -Name 'C:\Program Files\Intel\Wired Networking\IntelNetCmdlets\IntelNetCmdlets'
			Get-IntelNetAdapter"""

	result = subprocess.run(['powershell', '-ExecutionPolicy', 'Unrestricted', '-Command', ps_script], capture_output=True, text=True)
	# Get-IntelNetAdapter | ConvertTo-Csv -NoTypeInformation -Delimiter ';'"""

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