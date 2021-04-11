import PySimpleGUI as sg
import random

sg.theme("Black")  # colour scheme!

window_timeout = random.randint(800,2000)

# Display splash screen
sg.Window("areijk",no_titlebar=True,keep_on_top=True,layout=[[sg.Image(r"assets/aurarrium_logo_small.png")]]).Read(timeout=2000, close=True)