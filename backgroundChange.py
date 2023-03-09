from PIL import Image

# Define the image size and color
size = (1920, 1080)  # Desktop resolution
color = (0, 0, 255)  # Blue color in RGB format

# Create the image and save it as a BMP file
img = Image.new("RGB", size, color)
img.save("background.bmp")

# Set the image as the desktop background
import ctypes
ctypes.windll.user32.SystemParametersInfoW(20, 0, "background.bmp", 0)
