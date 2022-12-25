import time
import threading
import os

from classes import MENU
from constants import *

import importlib

# ---------------------------------------------------------------------------- #
#                                   RESTART                                    #
# ---------------------------------------------------------------------------- #

class MENU_restart(MENU):
    def enter(self):
        print(self.greeting)
        print("RESTARTING COMPUTER IN 5 SECONDS, PRESS 'ENTER' TO CANCEL")
        
        # Create a flag variable to cancel the thread
        self.cancel_thread = False
        
        # Start a new thread to restart the computer
        self.t = threading.Thread(target=self.restart_computer)
        self.t.start()

        # Wait for user input
        user_input = input()
        if user_input == "":
            # Cancel the restart
            self.cancel_thread = True
            print("RESTART CANCELLED")
            print(DIVIDER)
            time.sleep(1)

        else:
            # Restart the computer
            self.t.join()

        main.menu()

    def restart_computer(self):
        timeout = 5  # Timeout in seconds
        time.sleep(1)
        while timeout > 0:
            # Check the flag and exit if necessary
            if self.cancel_thread:
                return
            print(timeout)
            timeout -= 1
            time.sleep(1)
        
        
        
        # Restart the computer
        print("RESTARTING")
        # os.system("shutdown /r")


# ---------------------------------------------------------------------------- #
#                                 BOTTOM IMPORT                                #
# ---------------------------------------------------------------------------- #
main = importlib.import_module('main')

