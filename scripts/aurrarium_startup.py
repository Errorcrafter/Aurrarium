import PySimpleGUI as sg
import random
import sys
from aurrarium_gui import draw_gui

sg.theme("Black")  # colour scheme!

window_timeout = random.randint(800,2000)

# Display splash screen
sg.Window("areijk",no_titlebar=True,keep_on_top=True,layout=[[sg.Image(r"assets/aurrarium_logo_small.png")]]).Read(timeout=2000, close=True)

# Somewhat less hackier way to run aurrarium_gui.py, but there may still be issues.
draw_gui()
