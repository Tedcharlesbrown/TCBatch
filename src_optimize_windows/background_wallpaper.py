import os
import ctypes
from PIL import Image
import win32api

from constants import *

def set_color_background(red: int, green: int, blue: int):
    # Get the screen dimensions in pixels
    width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    # Define the image size and color
    size = (width, height)  # Desktop resolution
    color = (red, green, blue)  # Blue color in RGB format

    # Create the image and save it as a BMP file
    img = Image.new("RGB", size, color)
    img.save(f"{UTILITY_FOLDER_PATH}background.bmp")
    print("TEST")

    set_background()

def set_background():
    # Get the absolute path to the background.bmp file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    background = os.path.join(script_dir, f"{UTILITY_FOLDER_PATH}background.bmp")

    # Set the BMP file as the desktop background
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE = 0x2
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, background, SPIF_UPDATEINIFILE)

def set_tcb_background():
    # Get the absolute path to the background.bmp file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    background = os.path.join(script_dir, f"tcb_bg.bmp")

    # Set the BMP file as the desktop background
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE = 0x2
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, background, SPIF_UPDATEINIFILE)
    
# set_tcb_background()