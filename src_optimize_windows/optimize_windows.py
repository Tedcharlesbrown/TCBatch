# ------------------------- CREDIT GOES TO ANDY BABIN ------------------------ #
# https://github.com/andybabin/systemimaging
# https://github.com/andybabin/systemimaging/blob/main/removeapps.ps1
# https://github.com/andybabin/systemimaging/blob/main/winclean.ps1

# ---------------------------- DATATON SUGGESTIONS --------------------------- #
# WINDOWS 7 - DISABLE WINDOWS MEDIA CENTER
# DISABLE UAC (USER ACCESS CONTROL)
# DISABLE AUTOMATIC UPDATES

import subprocess
from constants import *
from questions import *
from src_optimize_windows.bloatware_list import BLOATWARE_APPLICATION_LIST

# ---------------------------------------------------------------------------- #
#                               REMOVE BLOATWARE                               #
# ---------------------------------------------------------------------------- #


def remove_bloatware_apps():
    for app in BLOATWARE_APPLICATION_LIST:
        # print(f"removing {app}")
        cmd = f"Get-AppxPackage {app} | Remove-AppxPackage"
        subprocess.call(["powershell.exe", cmd])

    remove_news()
    

# ---------------------------------------------------------------------------- #
#                           SET WINDOWS FEATURES                               #
# ---------------------------------------------------------------------------- #

def set_windows_features():
    
  choices = [
    "Disable UAC",                  #0
    "Enable dark mode",             #1
    "Disable lock screen",          #2
    "Show file extensions",         #3
    "Show hidden files",            #4
    "Remove Search from Task Bar",  #5
    "Hide Task Bar button",         #6
    "Disable XBOX DVR capture",     #7
    ]
  
  response = ask_checkbox(ASCII_SET_WINDOWS_FEATURES,choices,True)
  for task in response:
      match task:
        case 0:
            disable_uac()
        case 1:
            enable_dark_mode()
        case 2:
            disable_lock_screen()
        case 3:
            show_file_extensions()
        case 4:
            show_hidden_files()
        case 5:
            remove_search_bar()
        case 6:
            remove_task_bar()
        case 7:
            disable_xbox_dvr()

      

def disable_uac():
    command = r'reg add HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def enable_dark_mode():
    command = r'reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)
    command = r'reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v SystemUsesLightTheme /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def disable_lock_screen():
    command = r'reg add HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Personalization /v NoLockScreen /t REG_DWORD /d 1 /f'
    subprocess.run(command, shell=True)

def show_file_extensions():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v HideFileExt /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def show_hidden_files():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v Hidden /t REG_DWORD /d 1 /f'
    subprocess.run(command, shell=True)

def remove_search_bar():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Search /v SearchboxTaskbarMode /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def remove_task_bar():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v ShowTaskViewButton /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def disable_xbox_dvr():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR /v AppCaptureEnabled /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR /v HistoricalCaptureEnabled /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)


# ---------------------------------- TASKBAR --------------------------------- #

def remove_cortana():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v ShowCortanaButton /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def hide_people():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\People /v PeopleBand /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def hide_windows_defender():
    command = r'reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v SecurityHealth /f'
    subprocess.run(command, shell=True)

def disable_skype():
    command = r'reg add "HKCU\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\SystemAppData\Microsoft.SkypeApp_kzf8qxf38zg5c\SkypeStartup" /v State /t REG_DWORD /d 0 /f'
    subprocess.run(command, shell=True)

def remove_news():
    command = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Feeds /v ShellFeedsTaskbarViewMode /t REG_DWORD /d 2 /f'
    subprocess.run(command, shell=True)
    command = r'reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Feeds /v ShellFeedsTaskbarViewMode /t REG_DWORD /d 2 /f'
    subprocess.run(command, shell=True)

