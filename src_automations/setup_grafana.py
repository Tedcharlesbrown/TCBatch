import os.path
import os
import yaml
import subprocess
import win32com.client
import win32serviceutil
from datetime import datetime
import zipfile
import time

from constants import *
from questions import *
from src_software.application_list import *
from src_software.download_software import download_from_archive
from src_software.install_software import install_msi
from src_software.install_software import install_exe

path_to_grafana_setup = os.path.join(UTILITY_FOLDER_PATH,"GrafanaSetup")
path_to_grafana_zip = os.path.join(UTILITY_FOLDER_PATH,"GrafanaSetup.zip")

path_to_grafana_addon = r"C:\Program Files\GrafanaLabs\grafana\data"
path_to_prtg_zip = os.path.join(path_to_grafana_setup,"jasonlashua-prtg-datasource.zip")

path_grafana_msi = os.path.join(path_to_grafana_setup,"grafana.msi")
path_prometheus_exe = os.path.join(path_to_grafana_setup,"prometheus.exe")
path_prometheus_yml = os.path.join(path_to_grafana_setup,"prometheus.yml")
path_prtg_exe = os.path.join(path_to_grafana_setup,"prtg.exe")

path_windows_exporter = os.path.join(path_to_grafana_setup,"exporter.msi")
path_ohm_graphite = os.path.join(path_to_grafana_setup,"OhmGraphite.exe")

TASK_TRIGGER_AT_LOGON = 5

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
		try:
			install_msi(path_grafana_msi,"")

			if os.path.exists(path_to_grafana_addon):
				print("PATH EXISTS")
				try:
					with zipfile.ZipFile(path_to_prtg_zip, 'r') as zip_ref:
						path = f'{path_to_grafana_addon}/plugins'
						print(path)
						zip_ref.extractall(path)
				except Exception as e:
					# print(e)
					print("COULD NOT UNZIP PRTG PLUGIN")
			else:
				print("PATH DOES NOT EXIST")

			try:
				win32serviceutil.StopService("Grafana")
				time.sleep(3)  # wait a few seconds to ensure the service stops
				win32serviceutil.StartService("Grafana")
			except:
				print("COULD NOT RESTART GRAFANA SERVICE")

			print("INSTALLED GRAFANA, localhost:3000")
		except:
			print("COULD NOT INSTALL GRAFANA")
		
		input()

		# -------------------------------- PROMETHEUS -------------------------------- # #9090
		try:
			create_task(path_prometheus_exe,path_to_grafana_setup)
		except Exception as e:
			# print(e)
			print("COULD NOT SCHEDULE PROMETHEUS AT LOGON")
		try:
			os.chdir(path_to_grafana_setup) #UNTESTED WITH NORMAL MSI (NON WINDOWS EXPORTER)
			subprocess.Popen([path_prometheus_exe, "--config.file",path_prometheus_yml],creationflags=subprocess.CREATE_NEW_CONSOLE)
			print("INSTALLED PROMETHEUS, localhost:9090")

		except Exception as e:
			# print(e)
			print("COULD NOT INSTALL PROMETEHUS")

		# ----------------------------------- PRTG ----------------------------------- #
		try:
			if questionary.confirm(f"INSTALL PRTG?",qmark="",style=custom_style).ask():
				install_exe(path_prtg_exe)
				print("INSTALLED PRTG, localhost:80")
		except:
			print("COULD NOT INSTALL PRTG")

def create_task(path_to_executable,directory_path):
	computer_name = ""  # leave blank for local machine
	username = ""  # leave blank for current user
	task_name = "Prometheus AutoStart"
	action_path = path_to_executable  # path to your executable

	TASK_TRIGGER_AT_LOGON = 9
	TASK_ACTION_EXEC = 0
	TASK_CREATE_OR_UPDATE = 6
	TASK_LOGON_INTERACTIVE_TOKEN = 3
	TASK_RUNLEVEL_HIGHEST = 1

	scheduler = win32com.client.Dispatch("Schedule.Service")
	scheduler.Connect(computer_name)

	root_folder = scheduler.GetFolder("\\")

	task_def = scheduler.NewTask(0)

	# Create trigger
	start_trigger = task_def.Triggers.Create(TASK_TRIGGER_AT_LOGON)
	start_trigger.Enabled = True

	# Create action
	action = task_def.Actions.Create(TASK_ACTION_EXEC)
	action.Path = action_path
	action.WorkingDirectory = directory_path

	# Set parameters
	info = task_def.RegistrationInfo
	info.Author = username
	info.Description = "Python created task"

	# Set principal - this is where you set the highest privileges
	principal = task_def.Principal
	principal.RunLevel = TASK_RUNLEVEL_HIGHEST

	# Register the task (create or update, just keep the task name the same)
	result = root_folder.RegisterTaskDefinition(
		task_name,
		task_def,
		TASK_CREATE_OR_UPDATE,
		"",  # No user
		"",  # No password
		TASK_LOGON_INTERACTIVE_TOKEN,
	)


def edit_prometheus_yml(target_names: list, target_ips: list):
	valid_yaml = True
	# Check if the input lists are empty or contain only empty strings
	if not target_names or all(name == "" for name in target_names):
		# print("Target names list is empty or contains only empty strings. Skipping modification.")
		valid_yaml = False
	if not target_ips or all(ip == "" for ip in target_ips):
		# print("Target IPs list is empty or contains only empty strings. Skipping modification.")
		valid_yaml = False
	
	# Construct the base configuration
	config = {
		"global": {
			"scrape_interval": "15s",
			"evaluation_interval": "15s"
		},
		"alerting": {
			"alertmanagers": [
				{
					"static_configs": [
						{
							"targets": [
								# "alertmanager:9093"
							]
						}
					]
				}
			]
		},
		"rule_files": [
			# "first_rules.yml",
			# "second_rules.yml"
		],
		"scrape_configs": [
			{
				"job_name": "Default",
				"static_configs": []
			}
		]
	}
	
	# Add the targets to the configuration
	for name, ip in zip(target_names, target_ips):
		target = {
			"targets": [f"{ip}:9182", f"{ip}:4445"],
			"labels": {
				"server_name": name
			}
		}
		config["scrape_configs"][0]["static_configs"].append(target)

	# Convert the configuration to YAML and write the file
	if valid_yaml:
		with open(path_prometheus_yml, "w") as file:
			yaml.dump(config, file)

def install_grafana_client():
		check_and_download_grafana()
		# ----------------------------- WINDOWS EXPORTER ----------------------------- # #9182
		try:
			command = "ENABLED_COLLECTORS=cpu,cs,logical_disk,net,os,service,system,textfile,tcp,thermalzone,memory,logon,dhcp,dns,cpu_info LISTEN_PORT=9182"
			install_msi(path_windows_exporter,command)
			print("INSTALLED WINDOWS EXPORTER, localhost:9182/metrics")
		except:
				print("COULD NOT INSTALL WINDOWS EXPORTER")

		# ------------------------------- OHM GRAPHITE ------------------------------- # #4445
		try:
			command = f'"{path_ohm_graphite}" install'
			subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			command = f'"{path_ohm_graphite}" start'
			subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			print("INSTALLED OHM GRAPHITE, localhost:4445/metrics")
		except:
				print("COULD NOT INSTALL OHM GRAPHITE")




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