import os.path
import os

import winshell

import subprocess

import zipfile

from constants import *
from application_list import *

from download_software import download_from_archive



path_to_grafana_setup = os.path.join(UTILITY_FOLDER_PATH,"GrafanaSetup")
path_to_grafana_zip = os.path.join(path_to_grafana_setup,"GrafanaSetup.zip")

path_grafana_msi = os.path.join(path_to_grafana_setup,"grafana.msi")
path_prometheus_exe = os.path.join(path_to_grafana_setup,"prometheus.exe")
path_prometheus_yml = os.path.join(path_to_grafana_setup,"prometheus.yml")
path_prtg_exe = os.path.join(path_to_grafana_setup,"prtg.exe")

path_windows_exporter = os.path.join(path_to_grafana_setup,"exporter.msi")
path_ohm_graphite = os.path.join(path_to_grafana_setup,"OhmGraphite.exe")

def check_and_download_grafana():
    if os.path.exists(path_to_grafana_setup):
        # print("UNZIP EXISTS")
        pass
    elif os.path.exists(path_to_grafana_zip):
        print("UNZIPPING GRAFANA SETUP")
        with zipfile.ZipFile(path_to_grafana_zip, 'r') as zip_ref:
            zip_ref.extractall(UTILITY_FOLDER_PATH)
        os.remove(path_to_grafana_zip)
        check_and_download_grafana()
    else:
        print("GRAFANA SETUP NOT FOUND")
        download_from_archive("Grafana")
        check_and_download_grafana()

def install_grafana_host(target_names: list, target_ips: list):
    edit_prometheus_yml(target_names, target_ips)
    # ---------------------------------- GRAFANA --------------------------------- # #3000
    subprocess.call(['start', path_grafana_msi], shell=True) #Install Grafana

    # -------------------------------- PROMETHEUS -------------------------------- # #9090
    try:
        with winshell.shortcut(f"{PATH_STARTUP_FOLDER}/TCBatch_Prometheus.lnk") as shortcut:
            print(path_prometheus_exe)
            shortcut.path = path_prometheus_exe
            shortcut.arguments = f"--config.file {path_prometheus_yml}"
            shortcut.description = "Shortcut for Prometheus"
            shortcut.write()
    except:
        pass

# subprocess.Popen([path_prometheus_exe, "--config.file",path_prometheus_yml],creationflags=subprocess.CREATE_NEW_CONSOLE)

    # ----------------------------------- PRTG ----------------------------------- #
    subprocess.call([path_prtg_exe]) #Install PRTG

def edit_prometheus_yml(target_names: list, target_ips: list):
    yml_prefix = '''# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'Default'
    static_configs:
  '''
    
    yml_addition = ""
    
    for i, target in enumerate(target_names):

        yml_targets = f'''      - targets: ['{target_ips[i]}:9182', '{target_ips[i]}:4445']
          labels:
            server_name: '{target}\'
  '''
        
        yml_addition += yml_targets

    with open(path_prometheus_yml, "w") as file:
        file.write(yml_prefix + yml_addition)


#IDK WHY THIS DOESNT WORK, CANT INSTALL AND RUN PROMETHEUS AS SERVICE
    # command = [f"{path_to_grafana}/nssm.exe", "install", "prometheus", f"{path_to_grafana}/prometheus.exe"]
    # result = subprocess.run(command, capture_output=True, text=True)

    # # Check the result
    # if result.returncode == 0:
    #     print("Prometheus installation succeeded.")
    #     print("Output:", result.stdout)
    # else:
    #     print("Prometheus installation failed.")
    #     print("Error message:", result.stderr)

def install_grafana_client():
    check_and_download_grafana()
    # ----------------------------- WINDOWS EXPORTER ----------------------------- # #9182
    command = f"msiexec /i {path_windows_exporter} ENABLED_COLLECTORS=cpu,cs,logical_disk,net,os,service,system,textfile,tcp,thermalzone,memory,logon,dhcp,dns,cpu_info LISTEN_PORT=9182"
    subprocess.run(command, shell=True)

    # ------------------------------- OHM GRAPHITE ------------------------------- # #4445
    command = f'{path_ohm_graphite} install' 
    subprocess.run(command, shell=True)


