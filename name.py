from constants import *
from main import *

# ------------------------------------------------------------------------------
# COMPUTER NAME
# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------

def change_computer_name(computer_name: str):

	subprocess.call(['powershell.exe', "Rename-Computer -NewName " + computer_name])