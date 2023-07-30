from constants import *
from questions import *
from .setup_grafana import check_and_download_grafana
from .setup_grafana import install_grafana_host
from .setup_grafana import install_grafana_client

# ---------------------------------------------------------------------------- #
#                                 SETUP GRAFANA                                #
# ---------------------------------------------------------------------------- #

def menu_setup_grafana():
	choices = [
		"Setup Host",			#0
		"Setup Client"]			#1					
	choices.append("[cancel]")
	cancel = choices[-1]

	match ask_select("SETUP GRAFANA",choices,True):
		case 0:
			check_and_download_grafana()
			print(DIVIDER)
			menu_setup_grafana_host()
		case 1:
			install_grafana_client()
		case cancel:
			return

	print_return()
	return


def menu_setup_grafana_host():
	targets = 0
	names = []
	ips = []
	
	while True:
		name = ask_text(f"{targets}: TARGET NAME:")
		if not name:
			break
		names.append(name)
		ip = ask_text(f"{targets}: {name} IP:")
		ips.append(ip)

		targets+= 1


	install_grafana_host(names, ips)