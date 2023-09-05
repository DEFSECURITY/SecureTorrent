# 9-DEV
# to do:
# add icon (just let the app run in the background)
# switch to customtkinter

import tkinter as tk
import updater
import webbrowser

Title = "SafeTorrenting"
DiscordLink = "https://discord.gg/YhFsd7TVkN"
CurrentVersion = 11

class Main:
    def __init__(self):
        self.Screen = tk.Tk() # CustomTkinter
        self.Frame = tk.Frame(self.Screen)
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

        help_menu = tk.Menu(menubar, tearoff=0) # Done
        help_menu.add_command(label="Check for updates", command=updater.update)
        help_menu.add_command(label="Join our Discord", command=self.join_discord)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.Screen.config(menu=menubar)

    def join_discord(self):
        webbrowser.open(DiscordLink)

    def run(self):
        self.Screen.mainloop()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()