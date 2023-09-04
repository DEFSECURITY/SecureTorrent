# client.py - https://github.com/DEFSECURITY/SafeTorrenting
# todo: allow client to run in the background, add a logo?
# import tkinter as tk
# from tkinter import ttk

import customtkinter as tk
import updater
import webbrowser
from PIL import Image

Title = "SafeTorrenting"
DiscordLink = "https://discord.gg/YhFsd7TVkN"
CurrentVersion = 11

def Discord():
    webbrowser.open(DiscordLink)

class Main:
    def __init__(self):
        self.Screen = tk.CTk()
        self.Frame = tk.CTkFrame(self.Screen)
        self.Screen.title(f"{Title} - v{CurrentVersion}")
    
        menubar = tk.Menu(self.Screen)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add a torrent file")
        file_menu.add_command(label="Add a magnet link")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.Screen.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Resume")
        edit_menu.add_command(label="Stop")
        edit_menu.add_command(label="Resume all")
        edit_menu.add_command(label="Stop all")
        edit_menu.add_separator()
        edit_menu.add_command(label="Delete")

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Torrent Creator")
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings")

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Check for updates", command=updater.UpdateCheck)
        help_menu.add_command(label="Join our Discord", command=Discord)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.Screen.config(menu=menubar)
        
        self.Screen.mainloop()

if __name__ == "__main__":
    updater.UpdateCheck()
    app = Main()