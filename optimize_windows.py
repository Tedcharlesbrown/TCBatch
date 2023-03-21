# ------------------------- CREDIT GOES TO ANDY BABIN ------------------------ #
# https://github.com/andybabin/systemimaging
# https://github.com/andybabin/systemimaging/blob/main/removeapps.ps1
# https://github.com/andybabin/systemimaging/blob/main/winclean.ps1

# ---------------------------- DATATON SUGGESTIONS --------------------------- #
# WINDOWS 7 - DISABLE WINDOWS MEDIA CENTER
# DISABLE UAC (USER ACCESS CONTROL)
# DISABLE AUTOMATIC UPDATES

import subprocess
from questions import print_error
from questions import ask_select
from application_list import BLOATWARE_APPLICATION_LIST

# ---------------------------------------------------------------------------- #
#                               REMOVE BLOATWARE                               #
# ---------------------------------------------------------------------------- #


def remove_bloatware_apps():
      for app in BLOATWARE_APPLICATION_LIST:
        cmd = f"Get-AppxPackage {app} | Remove-AppxPackage"
              
        subprocess.call(["powershell.exe", cmd])

# ---------------------------------------------------------------------------- #
#                           SET WINDOWS FEATURES                               #
# ---------------------------------------------------------------------------- #

def set_windows_features():
    
  choices = [
    "Disable UAC",
    "Enable dark mode",
    "Disable lock screen",
    "Explorer opens in 'This PC'",
    "Show file extensions",
    "Show hidden files",
    "Remove Search from Task Bar",
    "Hide Task Bar button",
    "Disable XBOX DVR capture",
    ]
  
  choices.append("[cancel]")
  cancel = choices[-1]
  
  match ask_select("SET WINDOWS FEATURES",choices,True):
    case 0: #UAC
        # reg add HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
        pass
    case 1: #DARK MODE
        # reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f
        # reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v SystemUsesLightTheme /t REG_DWORD /d 0 /f
        pass
    case 2: #LOCK SCREEN
        # reg add HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Personalization /v NoLockScreen /t REG_DWORD /d 1 /f
        pass
    case 3: #THIS PC
        # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v LaunchTo /t REG_DWORD /d 1 /f
        pass
    case 4: #EXSTENSIONS
        # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v HideFileExt /t REG_DWORD /d 0 /f
        pass
    case 5: #HIDDEN FILES
        # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v Hidden /t REG_DWORD /d 1 /f
        pass
    case 6: #SEARCH
        # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Search /v SearchboxTaskbarMode /t REG_DWORD /d 0 /f
        pass
    case 7: #HIDE TASK BAR
        # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v ShowTaskViewButton /t REG_DWORD /d 0 /f
        pass
    case 8: #XBOX DVR
        # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR /v AppCaptureEnabled /t REG_DWORD /d 0 /f
        # reg add HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR /v HistoricalCaptureEnabled /t REG_DWORD /d 0 /f
        pass
    case cancel:
        pass

# ---------------------------------------------------------------------------- #
#                               CHANGE WALLPAPER                               #
# ---------------------------------------------------------------------------- #
