import PySimpleGUI as sg
import random
import sys
from aurrarium_gui import draw_gui

sg.theme("Black")  # colour scheme!

window_timeout = random.randint(800,2000)

# Display splash screen
sg.Window("areijk",no_titlebar=True,keep_on_top=True,layout=[[sg.Image(r"assets/aurrarium_logo_small.png")]]).Read(timeout=2000, close=True)

# # Display GUI from aurrarium_gui.py in the hackiest way possible
# exec(open(r"scripts/aurrarium_gui.py","r",encoding="utf8").read())

draw_gui()
