from constants import *
from questions import *

from src_optimize_windows.optimize_windows import remove_bloatware_apps
from src_optimize_windows.optimize_windows import set_windows_features
from src_optimize_windows.background_wallpaper import set_color_background
from src_optimize_windows.background_wallpaper import set_tcb_background

# ---------------------------------------------------------------------------- #
#                               OPTIMIZE WINDOWS                               #
# ---------------------------------------------------------------------------- #

def menu_optimize_windows():
	choices = [
	"Remove Bloatware Applications",
	"Set Windows Features",
	"Change Wallpaper",
	"Power Settings",
	"Firewall Settings",
	]
	choices.append("[cancel]")
	cancel = choices[-1]
	
	match ask_select(ASCII_OPTIMIZE_WINDOWS,choices,True):
		case 0:
			menu_remove_bloatware()
		case 1:
			print_error("WARNING, EDITING WINDOWS REGISTRY, PROCEED WITH CAUTION")
			menu_set_windows_features()
		case 2:
			menu_change_background()
		case 3:
			pass
		case 4:
			pass
		case cancel:
			pass

	print_return()
	return

# ------------------------ REMOVE WINDOWS APPLICATIONS ----------------------- #
def menu_remove_bloatware():

	remove_bloatware_apps()

	print_return()
	return

# -------------------------- CHANGE WINDOWS SETTINGS ------------------------- #
def menu_set_windows_features():

	set_windows_features()

	print_return()
	return

# ------------------------- CHANGE WINDOWS BACKGROUND ------------------------ #
def menu_change_background():
	choices = ["Clear Wallpaper","Set Color", "Set TCB"]
	colors = ["Red","Orange","Yellow","Green","Blue","Purple","Pink","[cancel]"]
	choices.append("[cancel]")
	cancel = choices[-1]

	try:
		match ask_select("CHANGE WALLPAPER",choices,True):
			case 0:
				set_color_background(0,0,0)
			case 1:
					match ask_select("SET BACKGROUND COLOR",colors,True):
						case 0:
							set_color_background(100,0,0)
						case 1:
							set_color_background(100,50,0)
						case 2:
							set_color_background(100,100,0)
						case 3:
							set_color_background(0,100,0)
						case 4:
							set_color_background(0,0,100)
						case 5:
							set_color_background(50,0,100)
						case 6:
							set_color_background(100,0,75)
						case 6:
							return
			case 2:
				set_tcb_background()
					
			case cancel:
				pass

	except:
		print_error("COULD NOT CHANGE WALLPAPER")

			
	print_return()
	return