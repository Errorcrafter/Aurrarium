import PySimpleGUI as sg
import random
import sys

sg.theme("Black")  # colour scheme!

window_timeout = random.randint(800,2000)

# Display splash screen
sg.Window("areijk",no_titlebar=True,keep_on_top=True,layout=[[sg.Image(r"assets/aurarrium_logo_small.png")]]).Read(timeout=2000, close=True)

# Display GUI from gui.py in the hackiest way possible
exec(open(r"./scripts/gui.py","r",encoding="utf8").read())