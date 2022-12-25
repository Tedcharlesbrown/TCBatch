# TCBatch
 ## What
 Small command line interface application for quickly setting up new computers / servers.

Currently only for windows systems, requires that the exe is run as an administrator.

## Background
On every gig I am on, I need to do the same thing for every computer in the system. Rename, set the IPs, download / install software, etc... So, I created this script to help automate that process

## Usage
- Upon startup, the script will search for a sub-directory named "applications", if no folder is found - one will be created.
- Most functionality can be accessed with the number keys and 'enter'

## Current Capabilities

### Change Computer Name
- Displays the current computer name
- Typing a new computer name and pressing `enter` will trigger windows to rename the computer on restart
- To cancel and go back, press `enter` with nothing written
### Change IP Addresses
- Displays all current network adapters
- Typing the number of the corresponding network adapter and pressing 'enter' to edit the settings for that adapter
	- Use `/` to separate settings
	- "IP ADDRESS/SUBNET/GATEWAY/PRIMARY DNS/SECONDARY DNS"
		- Examples:
			- `192.168.0.11`
				- Manually sets IP, and Subnet automatically to default
			- `192.168.0.11/255.255.255.0`
			- `192.168.0.11/24`
			- `192.168.0.11/A`
				- Manually sets IP. Subnet to 255.255.255.0
			- `192.168.0.11/24/192.168.0.1`
			- `192.168.0.11/24/1`
				- Manually sets IP and Subnet. Manually sets gateway to 192.168.0.1
			- `192.168.0.11/24/1/x.x.x.x/x.x.x.x`
				- Manually sets IP, Subnet, and Gateway. Manually sets DNS addresses
			- `192.168.0.11/24/1//`
				- Manually sets IP, Subnet, and Gateway, Automatically sets DNS to 1.1.1.1 and 8.8.8.8
			- `dhcp`
				- Manually sets adapter to DHCP
			-  To cancel and go back, press `enter` with nothing written
- To cancel and go back, press `enter` with nothing written
### Download Software
- Displays current list of applications I have listed.
- Entering the corresponding number will attempt to download the application from it's website. If that cannot be found, the script will connect to my NAS via FTP and download an archived version.
- Downloads will be placed in the "applications" folder that was created by the script on startup
- To que downloads
	- separate the corresponding numbers with `,`
- To manually download from the archive, append the number with `/`
	- Examples:
		- `10`
			- Will first attempt to download the software corresponding to 10, falling back to the archive if needed
		- `10,11`
			- Will first attempt to download the softwares corresponding to 10 and 11, falling back to the archive if needed
		- 10/,11
			- Will download the software corresponding to 10 from the archive, and will attempt to download the software corresponding to 11 from the internet
- To cancel and go back, press `enter` with nothing written
### Install Software
- Displays the current contents of the "applications" folder that was created by the script on startup
- Entering the corresponding number and will install the software
-   To que downloads
    -   separate the corresponding numbers with  `,`
### Create Symlink Folder
- Creates Symlink to the windows startup folder
### Restart Computer
- Starts a countdown to restart the computer
- To cancel and go back, press `enter` with nothing written

## Dependencies
- OS
- subprocess
- platform
- time
- pyuac
- bs4, BeautifulSoup
- ftplib
- importlib
