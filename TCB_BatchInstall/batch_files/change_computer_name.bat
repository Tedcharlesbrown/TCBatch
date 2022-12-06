import wmi
import win32api

# Set the new name for the computer
new_name = "MyNewComputerName"

# Connect to the WMI service
c = wmi.WMI()

# Get the current computer name
computer = c.Win32_ComputerSystem()[0]

# Rename the computer
computer.Rename(Name=new_name, Password=None, User=None)

# Restart the computer
win32api.InitiateSystemShutdown(None, None, 0, True, True)