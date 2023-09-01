import psutil
import subprocess
from questions import *

# def is_valid_ip(ip):
#     try:
#         socket.inet_aton(ip)  # For IPv4
#         return True
#     except socket.error:
#         try:
#             socket.inet_pton(socket.AF_INET6, ip)  # For IPv6
#             return True
#         except socket.error:
#             return False
        
def is_pingable(host):
    try:
        # Executing the ping command and checking the response
        output = subprocess.check_output(['ping', '-n', '1', host])
        return True
    except subprocess.CalledProcessError:
        return False

def get_shared_folders(ip):
    if is_pingable(ip):
        credentials_needed = False
        TIMEOUT = 5  # set a 5 seconds timeout

        try:
            if not credentials_needed:
                subprocess.check_output(['net', 'use', f'\\\\{ip}'], timeout=TIMEOUT)
            else:
                subprocess.check_output(['net', 'use', f'\\\\{ip}', password, f'/user:{username}'], timeout=TIMEOUT)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            if not credentials_needed:
                print("Error establishing connection with no credentials.")
                credentials_needed = True
                username = ask_text("USERNAME:")
                password = ask_text("PASSWORD:")
                
                try:
                    subprocess.check_output(['net', 'use', f'\\\\{ip}', password, f'/user:{username}'], timeout=TIMEOUT)
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    print("Error establishing connection with provided credentials.")
                    return

        try:
            result = subprocess.check_output(['net', 'view', f'\\\\{ip}']).decode('utf-8').splitlines()
            shares = []
            start_parsing = False
            for line in result:
                if ip in line:
                    start_parsing = True
                    continue
                if start_parsing and line and not line.startswith('---') and not line.startswith('The command'):
                    if "Disk" in line:  # Checking if "Disk" is in line to get only shared folders
                        folder_name = line.split('Disk')[0].strip()
                        shares.append(folder_name)
            return shares
        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return

# Example usage:
# ip = '192.168.1.182'
# ip = '192.168.0.6'

# print(get_shared_folders(ip))


def get_mounted_drives():
    return [p.device for p in psutil.disk_partitions()]

# print(get_mounted_drives())