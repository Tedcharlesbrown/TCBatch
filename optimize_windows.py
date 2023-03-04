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
from application_list import BLOATWARE_APPLICATION_LIST

# ---------------------------------------------------------------------------- #
#                               REMOVE BLOATWARE                               #
# ---------------------------------------------------------------------------- #


def remove_bloatware_apps(app_list: list):
    if len(app_list) == 0:
      print_error("NO OPTIONS SELECTED, SELECT OPTIONS WITH <space>")
    else:
                
      cmd = "$AppsList = "

      for i, app in enumerate(app_list):
          cmd += f"\"{BLOATWARE_APPLICATION_LIST[app].name}\""

          if app != app_list[-1]:
              cmd += ","

          cmd += "\n"
      
      cmd += "\n"
      cmd += """ForEach ($App in $AppsList)
  {
    $PackageFullName = (Get-AppxPackage $App).PackageFullName
    $ProPackageFullName = (Get-AppxProvisionedPackage -online | where {$_.Displayname -eq $App}).PackageName
    write-host $PackageFullName
    Write-Host $ProPackageFullName
  
    if ($PackageFullName)
    {
      Write-Host “Removing Package: $App”
      remove-AppxPackage -package $PackageFullName
    }
    else
    {
      Write-Host “Unable to find package: $App”
    }
  
    if ($ProPackageFullName)
    {
      Write-Host “Removing Provisioned Package: $ProPackageFullName”
      Remove-AppxProvisionedPackage -online -packagename $ProPackageFullName
    }
    else
    {
      Write-Host “Unable to find provisioned package: $App”
    }
  }"""

      subprocess.call(["powershell.exe", cmd])

# ---------------------------------------------------------------------------- #
#                           TURN OFF WINDOWS FEATURES                          #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                               CHANGE WALLPAPER                               #
# ---------------------------------------------------------------------------- #
