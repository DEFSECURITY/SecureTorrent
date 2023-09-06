# 9-DEV
# to do:
# add icon (just let the app run in the background)
import updater # this will exit the app if the user updates

import sys
sys.path.append("core")
import hashfile
import stsocket
import config
from PIL import Image
from infi.systray import SysTrayIcon
import tkinter 
import customtkinter

# this is really broken for some reason
systray = None
try:
    def do_nothing(sysTrayIcon):
        pass
    menu_options = ((config.Title, None, do_nothing),)
    systray = SysTrayIcon("logo.ico", config.Title, menu_options, on_quit=quit)
    systray.start()
except: 
    pass

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()

def quit():
    try: 
        systray.shutdown()
    except:
        pass
    try:
        app.quit()
    except:
        pass
    exit()

app.geometry("1280x720")

def button_function():
    print("button pressed")

button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

menubar = tkinter.Menu(app)
filemenu = tkinter.Menu(menubar, tearoff=0)

filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="App", menu=filemenu)

app.config(menu=menubar)
app.mainloop()

