from constants import *
from classes import APPLICATION
from classes import BLOATWARE


APPLICATION_DOWNLOAD_LIST = [
    
    # ------------------------------------- A ------------------------------------ #
    APPLICATION("Artnetominator","Artnetominator.msi", "https://www.lightjams.com/artnetominator/"),
    # ------------------------------------- B ------------------------------------ #
    APPLICATION("Barco Event Master","Barco-Event-Master.exe","Archive"),
    APPLICATION("BGInfo","BGInfo.exe","https://learn.microsoft.com/en-us/sysinternals/downloads/bginfo"),
    APPLICATION("Bitfocus Companion","Bitfocus-Companion.exe","Archive"),
    APPLICATION("Blackmagic Atem","Blackmagic-Atem.msi","Archive"),
    APPLICATION("Blackmagic Multiview","Blackmagic-Multiview.msi","Archive"),
    APPLICATION("Blackmagic Videohub","Blackmagic-Videohub.msi","Archive"),
    APPLICATION("Brompton - Tessera", "Brompton-Tessera.exe","Archive"),
    APPLICATION("Bulk Rename Utility","Bulk-Rename-Utility.exe","https://www.bulkrenameutility.co.uk/Download.php"),
    # ------------------------------------- C ------------------------------------ #
    # ------------------------------------- D ------------------------------------ #
    APPLICATION("D3 Disguise","d3.exe", "Archive"),
    APPLICATION("Dashboard","Dashboard.exe","https://www.opengear.tv/frame-and-control/control-system/download/"),
    APPLICATION("Decimator Control Software","Decimator-Control-Software.msi","http://decimator.com/DOWNLOADS/DOWNLOADS.html"),
    # ------------------------------------- E ------------------------------------ #
    APPLICATION("ETC Eos","EOS-Family.exe","Archive"),
    # ------------------------------------- F ------------------------------------ #
    APPLICATION("Free File Sync","Free-File-Sync.exe","https://freefilesync.org/download.php"),
    # ------------------------------------- G ------------------------------------ #
    APPLICATION("Github","Github.exe","https://central.github.com/deployments/desktop/desktop/latest/win32"),
    # ------------------------------------- H ------------------------------------ #
    # ------------------------------------- I ------------------------------------ #
    APPLICATION("Intel PROset","Intel-PROset.exe","Archive"),
    # ------------------------------------- J ------------------------------------ #
    # ------------------------------------- K ------------------------------------ #
    # ------------------------------------- L ------------------------------------ #
    # ------------------------------------- M ------------------------------------ #
    APPLICATION("Midi-Ox","Midi-Ox.exe","http://www.midiox.com/zip/midioxse.exe"),
    APPLICATION("myFFmpeg","myFFmpeg.exe","https://www.myffmpeg.com/download.html"),
    # ------------------------------------- N ------------------------------------ #
    APPLICATION("NDI Tools","NDI-Tools.exe","Archive"),
    APPLICATION("Netgear Switch Discovery", "Netgear-Discovery.exe","Archive"),
    APPLICATION("NetSetMan","Net-Set-Man.exe","Archive"),
    # ------------------------------------- O ------------------------------------ #
    APPLICATION("OBS Studio","OBS-Studio.exe","https://obsproject.com/download"),
    # ------------------------------------- P ------------------------------------ #
    APPLICATION("Panasonic Easy IP", "Panasonic-EasyIP.zip","Archive"),
    APPLICATION("Parsec","Parsec.exe","https://builds.parsec.app/package/parsec-windows.exe"),
    APPLICATION("Pixera Hub","PixeraHub.exe","https://pixera.one/en/support/downloads"),
    APPLICATION("Processing","Processing.zip","Archive"),
    APPLICATION("Protokol","Protokol.exe","https://hexler.net/protokol#windows"),
    APPLICATION("PuTTY","Putty.msi","https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"),
    APPLICATION("Python","Python.exe","https://www.python.org/downloads/"),
    # ------------------------------------- Q ------------------------------------ #
    # ------------------------------------- R ------------------------------------ #
    APPLICATION("Real VNC","RealVNC.exe","https://www.realvnc.com/en/connect/download/viewer/windows/"),
    APPLICATION("Reaper","Reaper.exe","https://www.reaper.fm/download.php"),
    APPLICATION("Rufus","Rufus.exe","https://rufus.ie/en/"),
    # ------------------------------------- S ------------------------------------ #
    APPLICATION("Sublime Text Editor","Sublime.exe","https://www.sublimetext.com/download_thanks?target=win-x64"),
    # ------------------------------------- T ------------------------------------ #
    APPLICATION("Tailscale","Tailscale.exe","https://pkgs.tailscale.com/stable/"),
    APPLICATION("Tight VNC","TightVNC.msi","https://www.tightvnc.com/download.php"),
    APPLICATION("TouchOSC","touchosc.exe","https://hexler.net/touchosc#windows"),
    # ------------------------------------- U ------------------------------------ #
    # ------------------------------------- V ------------------------------------ #
    APPLICATION("vMix","vMix.exe","https://www.vmix.com/software/download.aspx"),
    APPLICATION("Visual Studio Code", "vscode.exe","Archive"),
    # ------------------------------------- W ------------------------------------ #
    APPLICATION("WinDirStat", "windirstat.exe","https://www.fosshub.com/WinDirStat.html"),
    APPLICATION("Wireshark", "Wireshark.exe","https://www.wireshark.org/download.html"),
    # ------------------------------------- X ------------------------------------ #
    # ------------------------------------- Y ------------------------------------ #
    # ------------------------------------- Z ------------------------------------ #

    APPLICATION("Grafana","","Archive"),
    APPLICATION("Custom Scripts","", "http://gofile.me/70auI/6qt31duqE"),
]


# TODO
# VISTALKINK PRO (MASTERCLOCK)
# Scopes (Verification only)
# NDI Discovery Server
# Unifi
# P-Touch Editor
# Blender
# fSpy
# Instant Meshes
# CloneZilla

BLOATWARE_APPLICATION_LIST = [
    "Microsoft.3DBuilder",
    "Microsoft.Microsoft3DViewer",
    "Microsoft.MixedReality.Portal",
    "*Microsoft.549981C3F5F10", #CORTANA,
    "*Microsoft.549981C3F5F10*", #CORTANA,
    "Microsoft.WindowsCommunicationsApps",
    "Microsoft.Messaging",
    "Microsoft.People",
    "Microsoft.SkypeApp",
    "Microsoft.YourPhone",
    "Microsoft.XboxApp",
    "Microsoft.XboxGameOverlay",
    "Microsoft.ZuneMusic",
    "Microsoft.ZuneVideo",
    # "Microsoft.Windows.Photos",
    "Microsoft.WindowsAlarms",
    "Microsoft.WindowsMaps",
    "Microsoft.ScreenSketch",
    "Microsoft.MicrosoftSolitaireCollection", 
    "Microsoft.WindowsSoundRecorder",
    "Microsoft.MicrosoftStickyNotes",
    "Microsoft.BingWeather",
    "Microsoft.BingFinance",
    "Microsoft.BingSports",
    "*linkedin*",
    "Microsoft.MicrosoftOfficeHub",
    "Microsoft.OneConnect",
    "Microsoft.Office.OneNote",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.GetHelp",
    "Microsoft.Getstarted",
    "Microsoft.MSPaint",
]