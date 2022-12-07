import os.path
import os
import subprocess
import platform
import subprocess
import msvcrt
import time


APP_NAME = "TCB - Quick Setup"
DIVIDER = "----------"
PATH_BATCH_FOLDER = "batch_files"

SUBNET_LIST = ["0.0.0.0", "128.0.0.0", "192.0.0.0", "224.0.0.0", "240.0.0.0", "248.0.0.0", "252.0.0.0", "254.0.0.0", "255.0.0.0", "255.128.0.0", "255.192.0.0", "255.224.0.0", "255.240.0.0", "255.248.0.0", "255.252.0.0", "255.254.0.0", "255.255.0.0", "255.255.128.0",
               "255.255.192.0", "255.255.224.0", "255.255.240.0", "255.255.248.0", "255.255.252.0", "255.255.254.0", "255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240", "255.255.255.248", "255.255.255.252", "255.255.255.254", "255.255.255.255"]

print(SUBNET_LIST[24])

# NETWORK INTERFACES ------------------------------------------------------------------------------


def get_network_adapters():
    # Create an empty list to store the interface names
    interfaces = []

    # Run the "ipconfig" command and save the output
    output = subprocess.check_output("ipconfig")

    # Decode the output from bytes to a string
    output = output.decode("utf-8")

    # Split the output into a list of lines
    for line in output.split("\n"):

        # Check if the line contains the word "adapter"
        if "adapter" in line:

            # Split the line on the word "adapter" and extract the adapter name
            adapter = line.split("adapter ")
            adapter = adapter[1].split(":")

            # Add the adapter name to the list of interfaces
            interfaces.append(adapter[0])

    # Return the list of interfaces
    return interfaces


def parse_subnet(subnet_input: str):
    subnet = ""
    if subnet_input.lower() == "a":
        subnet = "255.0.0.0"
    elif subnet_input.lower() == "b":
        subnet = "255.255.0.0"
    elif subnet_input.lower() == "c":
        subnet = "255.255.255.0"
    elif int(subnet_input) <= 33:
        subnet = SUBNET_LIST[int(subnet_input)]
    else:
        subnet = subnet_input
    return subnet


def parse_dns(dns_input: str, is_primary: bool):
    dns = ""
    if len(dns_input) == 0:
        if is_primary:
            dns = "1.1.1.1"
        else:
            dns = "8.8.8.8"
    else:
        dns = dns_input

    return dns


def change_network_adapters(interface: str, addresses: list):
    temp_bat = PATH_BATCH_FOLDER + "/" + "change_network_adapters.bat"

    # CREATE / OVERWRITE BAT FILE
    open(temp_bat, 'w').close()

    if addresses[0].lower() == "dhcp":
        with open(temp_bat, "a") as file:
            file.write("netsh interface ip set address \"" + interface + "\" source=dhcp")

    if len(addresses) == 1:

        print("NO SUBNET GIVEN, DEFAULTING TO 255.255.255.0")
        with open(temp_bat, "a") as file:
            file.write("netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " 255.255.255.0")
    elif len(addresses) == 2:

        with open(temp_bat, "a") as file:
            file.write("netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1]))

    elif len(addresses) == 3:

        with open(temp_bat, "a") as file:
            file.write("netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1]) + " " + addresses[2])

    elif len(addresses) == 4:
        with open(temp_bat, "a") as file:
            file.write("netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1]) + " " + addresses[2])
            file.write("\r")
            file.write("netsh interface ip set dns \"" + interface + "\" static " + parse_dns(addresses[3], True))

    elif len(addresses) == 5:
        with open(temp_bat, "a") as file:
            file.write("netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + parse_subnet(addresses[1]) + " " + addresses[2])
            file.write("\r")
            file.write("netsh interface ip set dns \"" + interface + "\" static " + parse_dns(addresses[3], True))
            file.write("\r")
            file.write("netsh interface ip add dns \"" + interface + "\" " + parse_dns(addresses[3], False) + " index=2")

    # with open(temp_bat, "a") as file:
        # file.write("netsh interface ip set address \"" + interface + "\" static 192.168.0.11 255.255.255.0 192.168.1.1")
        # file.write("netsh interface ipv4 set dns \"" + interface + "\" static " + addresses[3])
        # file.write("netsh interface ipv4 add dns \"" + interface + "\" " + addresses[4] + " index=2")

        # file.write("netsh interface ip set address \"" + interface + "\" static " + addresses[0] + " " + addresses[1] + " " + addresses[2])
        # file.write("netsh interface ipv4 set dns \"" + interface + "\" static " + addresses[3])
        # file.write("netsh interface ipv4 add dns \"" + interface + "\" " + addresses[4] + " index=2")

# COMPUTER NAME ------------------------------------------------------------------------------


def change_computer_name(computer_name: str):
    # temp_bat = PATH_BATCH_FOLDER + "/" + "change_computer_name.bat"

    # # CREATE / OVERWRITE BAT FILE
    # open(temp_bat, 'w').close()

    # with open(temp_bat, "a") as file:
    # 	file.write("@echo off\r")
    # 	file.write("\r")
    # 	file.write("rem Set the new computer name\r")
    # 	file.write("set COMPUTER_NAME=" + "\"" + computer_name + "\"\r")
    # 	file.write("\r")
    # 	file.write("rem Change the computer name\r")
    # 	file.write("wmic computersystem where name=" + "\"" "%computername%" "\"" +"call rename name=" + "\"" + "%COMPUTER_NAME%")

    subprocess.call(
        ['powershell.exe', "Rename-Computer -NewName " + computer_name])


# BATCH FILES ------------------------------------------------------------------------------

# if not os.path.exists(batch_folder_path):
    # os.makedirs(batch_folder_path)

# subprocess.call([batch_folder_path+'\hello_world.bat'])


# APPLICATION INSTALL------------------------------------------------------------------------

def application_init():
    application_folder_path = 'applications'
    if not os.path.exists(application_folder_path):
        os.makedirs(application_folder_path)
    else:
        application_install_list = os.listdir(application_folder_path)
        print(application_install_list)
        # subprocess.run(["applications/"+application_install_list[0], ""])
        # subprocess.run(["applications/"+application_install_list[1], ""])


# msiexec.exe /i "C:\Users\Rkdns\Desktop\TCB_BatchInstall\applications\SpotifySetup.exe"


def menu_main():
    print("1: Change computer name")
    print("2: Change IP Addresses")
    print("3: Install Software")
    print(DIVIDER)

    user_input = input()

    if user_input == "1":
        menu_change_computer_name()
    elif user_input == "2":
        menu_change_network()
    elif user_input == "3":
        print("SOFTWARE INSTALL: NOT IMPLEMENTED YET")
        print(DIVIDER)
        menu_main()


def menu_change_computer_name():
    print(DIVIDER)
    print("CHANGING COMPUTER NAME")
    print(DIVIDER)
    time.sleep(1)
    print("TYPE NEW NAME AND PRESS 'ENTER', OR PRESS 'ENTER' TO CANCEL")
    print("CURRENT COMPUTER NAME = " + "'" + platform.node() + "'")
    print(DIVIDER)

    user_input = input()

    if user_input == "":
        print("GOING BACK TO MAIN MENU")
        print(DIVIDER)
        menu_main()
    else:
        print(DIVIDER)
        print("CHANGING NAME TO: " + user_input)
        change_computer_name(user_input)
        time.sleep(1)
        print("NAME WILL UPDATE ON RESTART")
        print(DIVIDER)
        time.sleep(1)
        menu_main()


def menu_change_adapter(adapter: int):
    if adapter == "0":
        print("EDITING IP ADDRESS:")
        print(DIVIDER)
    elif adapter == "1":
        print("EDITING SUBNET:")
        print(DIVIDER)
    elif adapter == "2":
        print("EDITING GATEWAY:")
        print(DIVIDER)
    elif adapter == "3":
        print("EDITING DNS:")
        print(DIVIDER)
    else:
        menu_change_network()

    user_input = input()


def menu_change_network():
    print(DIVIDER)
    print("CHANGING IP ADDRESSES")
    print("TYPE THE NUMBER OF THE INTERFACE YOU WOULD LIKE TO CHANGE, OR PRESS 'ENTER' TO CANCEL")
    network_adapters = get_network_adapters()
    for i, interface in enumerate(network_adapters):
        print(str(i) + ": " + "\"" + interface + "\"")
    print(DIVIDER)

    user_input = input()
    selected_network_adapter = ""

    if user_input == "":
        print("GOING BACK TO MAIN MENU")
        print(DIVIDER)
        menu_main()
    elif user_input.isdigit():
        print(DIVIDER)
        selected_network_adapter = network_adapters[int(user_input)]
        print("EDITING ADAPTER: " + selected_network_adapter)
        print("USE FOLLOWING SYNTAX TO CHANGE NETWORK ADAPTER")
        print("\"IP ADDRESS/SUBNET/GATEWAY/PRIMARY DNS/SECONDARY DNS\"")
        # print("\"192.168.1.11/255.255.255.0/192.168.1.1\"")
        print(DIVIDER)
        user_input = input()
        if user_input == "":
            print("GOING BACK")
            menu_change_network()
        else:
            addresses = user_input.split("/")
            if user_input == "":
                print("GOING BACK")
                menu_change_network()
            else:
                change_network_adapters(selected_network_adapter, addresses)


print(APP_NAME)
print("Press number then 'ENTER' to make selection")
print(DIVIDER)
menu_main()
