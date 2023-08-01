from constants import *
import time
import threading
import os

# ---------------------------------------------------------------------------- #
#                               RESTART COMPUTER                               #
# ---------------------------------------------------------------------------- #

def menu_restart_computer():
	global cancel_restart_flag
	print("RESTARTING COMPUTER IN 5 SECONDS, PRESS 'ENTER' TO CANCEL")
	
	# Create a flag variable to cancel the thread
	cancel_restart_flag = False
	
	# Start a new thread to restart the computer
	t = threading.Thread(target=restart_computer)
	t.start()

	# Wait for user input
	user_input = input()
	if user_input == "":
		# Cancel the restart
		cancel_restart_flag = True
		print("RESTART CANCELLED")
		print(DIVIDER)
		time.sleep(1)
		return

	else:
		# Restart the computer
		t.join()
	

def restart_computer():
	global cancel_restart_flag
	timeout = 5
	time.sleep(1)
	while timeout > 0:
		# Check the flag and exit if necessary
		if cancel_restart_flag:
			return
		print(timeout)
		timeout -= 1
		time.sleep(1)
	
	# Restart the computer
	print("RESTARTING")
	os.system("shutdown /r /t 0")