from ctypes import wintypes, windll
import winshell
import os
import json

APP_NAME = "TCB - Quick Setup"
APP_VERSION = "v1.5.3"
DIVIDER = "----------"

PATH_THIS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PATH_STARTUP_FOLDER = winshell.startup()
PATH_INTEL_PROSET = r'C:\Program Files\Intel\Wired Networking\IntelNetCmdlets'
APPLICATION_DOWNLOAD_LIST = []
APPLICATION_INSTALL_LIST = []
UTILITY_FOLDER_PATH = r'C:\TCBatch/'
DOWNLOAD_FOLDER_PATH = r'C:\TCBatch/'
SETTINGS_FOLDER = "settings.json"
PATH_DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

def save_settings():
    settings = {
        "download path": DOWNLOAD_FOLDER_PATH
    }

    with open(os.path.join(UTILITY_FOLDER_PATH, SETTINGS_FOLDER), 'w') as file:
        json.dump(settings, file)


SUBNET_LIST = ["0.0.0.0", "128.0.0.0", "192.0.0.0", "224.0.0.0", "240.0.0.0", "248.0.0.0", "252.0.0.0", "254.0.0.0", "255.0.0.0", "255.128.0.0", "255.192.0.0", "255.224.0.0", "255.240.0.0", "255.248.0.0", "255.252.0.0", "255.254.0.0", "255.255.0.0", "255.255.128.0",
			   "255.255.192.0", "255.255.224.0", "255.255.240.0", "255.255.248.0", "255.255.252.0", "255.255.254.0", "255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240", "255.255.255.248", "255.255.255.252", "255.255.255.254", "255.255.255.255"]

SUBNET_MAP = {
	"a": "255.0.0.0",
	"b": "255.255.0.0",
	"c": "255.255.255.0",
}
# https://patorjk.com/software/taag/#p=display&h=2&v=2&f=Small&t=TCBatch
APP_NAME = r"""
  _____ ___ ___       _      _    
 |_   _/ __| _ ) __ _| |_ __| |_  
   | || (__| _ \/ _` |  _/ _| ' \ 
   |_| \___|___/\__,_|\__\__|_||_|
"""

ASCII_COMPUTER_NAME = r"""
   ___ _  _   _   _  _  ___ ___ _  _  ___    ___ ___  __  __ ___ _   _ _____ ___ ___   _  _   _   __  __ ___ 
  / __| || | /_\ | \| |/ __|_ _| \| |/ __|  / __/ _ \|  \/  | _ \ | | |_   _| __| _ \ | \| | /_\ |  \/  | __|
 | (__| __ |/ _ \| .` | (_ || || .` | (_ | | (_| (_) | |\/| |  _/ |_| | | | | _||   / | .` |/ _ \| |\/| | _| 
  \___|_||_/_/ \_\_|\_|\___|___|_|\_|\___|  \___\___/|_|  |_|_|  \___/  |_| |___|_|_\ |_|\_/_/ \_\_|  |_|___|
"""

ASCII_NETWORK_SETTINGS = r"""
  _  _ ___ _______      _____  ___ _  __  ___ ___ _____ _____ ___ _  _  ___ ___ 
 | \| | __|_   _\ \    / / _ \| _ \ |/ / / __| __|_   _|_   _|_ _| \| |/ __/ __|
 | .` | _|  | |  \ \/\/ / (_) |   / ' <  \__ \ _|  | |   | |  | || .` | (_ \__ \
 |_|\_|___| |_|   \_/\_/ \___/|_|_\_|\_\ |___/___| |_|   |_| |___|_|\_|\___|___/                                                                                                                                                       
"""

ASCII_IP_ADDRESS = r"""
   ___ _  _   _   _  _  ___ ___ _  _  ___   ___ ___     _   ___  ___  ___ ___ ___ ___ 
  / __| || | /_\ | \| |/ __|_ _| \| |/ __| |_ _| _ \   /_\ |   \|   \| _ \ __/ __/ __|
 | (__| __ |/ _ \| .` | (_ || || .` | (_ |  | ||  _/  / _ \| |) | |) |   / _|\__ \__ \
  \___|_||_/_/ \_\_|\_|\___|___|_|\_|\___| |___|_|   /_/ \_\___/|___/|_|_\___|___/___/                                                                            
"""
ASCII_NETWORK_NAME = """
   ___ _  _   _   _  _  ___ ___     _   ___   _   ___ _____ ___ ___   _  _   _   __  __ ___ 
  / __| || | /_\ | \| |/ __| __|   /_\ |   \ /_\ | _ \_   _| __| _ \ | \| | /_\ |  \/  | __|
 | (__| __ |/ _ \| .` | (_ | _|   / _ \| |) / _ \|  _/ | | | _||   / | .` |/ _ \| |\/| | _| 
  \___|_||_/_/ \_\_|\_|\___|___| /_/ \_\___/_/ \_\_|   |_| |___|_|_\ |_|\_/_/ \_\_|  |_|___|                                                                                                                                                                    
"""
ASCII_VLAN = r"""
 __   ___      _   _  _ ___ 
 \ \ / / |    /_\ | \| / __|
  \ V /| |__ / _ \| .` \__ \
   \_/ |____/_/ \_\_|\_|___/                                                                                                
"""

ASCII_DOWNLOAD = r"""
  ___   _____      ___  _ _    ___   _   ___    ___  ___  ___ _______      ___   ___ ___ 
 |   \ / _ \ \    / / \| | |  / _ \ /_\ |   \  / __|/ _ \| __|_   _\ \    / /_\ | _ \ __|
 | |) | (_) \ \/\/ /| .` | |_| (_) / _ \| |) | \__ \ (_) | _|  | |  \ \/\/ / _ \|   / _| 
 |___/ \___/ \_/\_/ |_|\_|____\___/_/ \_\___/  |___/\___/|_|   |_|   \_/\_/_/ \_\_|_\___|                                                                                    
"""

ASCII_SOFTWARE = r"""
  ___ _  _ ___ _____ _   _    _    ___ _  _  ___   ___  ___  ___ _______      ___   ___ ___ 
 |_ _| \| / __|_   _/_\ | |  | |  |_ _| \| |/ __| / __|/ _ \| __|_   _\ \    / /_\ | _ \ __|
  | || .` \__ \ | |/ _ \| |__| |__ | || .` | (_ | \__ \ (_) | _|  | |  \ \/\/ / _ \|   / _| 
 |___|_|\_|___/ |_/_/ \_\____|____|___|_|\_|\___| |___/\___/|_|   |_|   \_/\_/_/ \_\_|_\___|																					
"""
ASCII_OPTIMIZE_WINDOWS = r"""
   ___  ___ _____ ___ __  __ ___ _______  __      _____ _  _ ___   _____      _____ 
  / _ \| _ \_   _|_ _|  \/  |_ _|_  / __| \ \    / /_ _| \| |   \ / _ \ \    / / __|
 | (_) |  _/ | |  | || |\/| || | / /| _|   \ \/\/ / | || .` | |) | (_) \ \/\/ /\__ \
  \___/|_|   |_| |___|_|  |_|___/___|___|   \_/\_/ |___|_|\_|___/ \___/ \_/\_/ |___/                                                                                 																					
"""

ASCII_SYMLINK = r"""
  _____   ____  __ _    ___ _  _ _  __  ___ ___  _    ___  ___ ___ 
 / __\ \ / /  \/  | |  |_ _| \| | |/ / | __/ _ \| |  |   \| __| _ \
 \_   \\ V /| |\/| | |__ | || .` | ' <  | _| (_) | |__| |) | _||   /
 |___/ |_| |_|  |_|____|___|_|\_|_|\_\ |_| \___/|____|___/|___|_|_\
"""

ASCII_RESTART = r"""
  ___ ___ ___ _____ _   ___ _____    ___ ___  __  __ ___ _   _ _____ ___ ___ 
 | _ \ __/ __|_   _/_\ | _ \_   _|  / __/ _ \|  \/  | _ \ | | |_   _| __| _ \
 |   / _|\__ \ | |/ _ \|   / | |   | (_| (_) | |\/| |  _/ |_| | | | | _||   /
 |_|_\___|___/ |_/_/ \_\_|_\ |_|    \___\___/|_|  |_|_|  \___/  |_| |___|_|_\
"""

ASCII_MANAGE_WINDOWS = r"""
  __  __   _   _  _   _   ___ ___  __      _____ _  _ ___   _____      _____   ___ ___ _____ _____ ___ _  _  ___ ___ 
 |  \/  | /_\ | \| | /_\ / __| __| \ \    / /_ _| \| |   \ / _ \ \    / / __| / __| __|_   _|_   _|_ _| \| |/ __/ __|
 | |\/| |/ _ \| .` |/ _ \ (_ | _|   \ \/\/ / | || .` | |) | (_) \ \/\/ /\__ \ \__ \ _|  | |   | |  | || .` | (_ \__ \
 |_|  |_/_/ \_\_|\_/_/ \_\___|___|   \_/\_/ |___|_|\_|___/ \___/ \_/\_/ |___/ |___/___| |_|   |_| |___|_|\_|\___|___/
"""

ASCII_SET_WINDOWS_FEATURES = r"""
  ___ ___ _____  __      _____ _  _ ___   _____      _____   ___ ___   _ _____ _   _ ___ ___ ___ 
 / __| __|_   _| \ \    / /_ _| \| |   \ / _ \ \    / / __| | __| __| /_\_   _| | | | _ \ __/ __|
 \__ \ _|  | |    \ \/\/ / | || .` | |) | (_) \ \/\/ /\__ \ | _|| _| / _ \| | | |_| |   / _|\__ \
 |___/___| |_|     \_/\_/ |___|_|\_|___/ \___/ \_/\_/ |___/ |_| |___/_/ \_\_|  \___/|_|_\___|___/
"""

ASCII_AUTOMATIONS = r"""
    _  _   _ _____ ___  __  __   _ _____ ___ ___  _  _ ___ 
   /_\| | | |_   _/ _ \|  \/  | /_\_   _|_ _/ _ \| \| / __|
  / _ \ |_| | | || (_) | |\/| |/ _ \| |  | | (_) | .` \__ \
 /_/ \_\___/  |_| \___/|_|  |_/_/ \_\_| |___\___/|_|\_|___/
"""

ASCII_GRAFANA = r"""
  ___ ___ _____ _   _ ___    ___ ___    _   ___ _   _  _   _   
 / __| __|_   _| | | | _ \  / __| _ \  /_\ | __/_\ | \| | /_\  
 \__ \ _|  | | | |_| |  _/ | (_ |   / / _ \| _/ _ \| .` |/ _ \ 
 |___/___| |_|  \___/|_|    \___|_|_\/_/ \_\_/_/ \_\_|\_/_/ \_\
"""