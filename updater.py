# Usage of CTkMessagebox instead of normal's tkinter's 

# Known bugs:
# No development builds. (due to my huge amount of pull requests)
# (INITIALIZE) CTkMessagebox opens up a new screen. Fix this

import requests
import client
from CTkMessagebox import CTkMessagebox
import webbrowser

def Update():
    try:
        response = requests.get("https://raw.githubusercontent.com/DEFSECURITY/SafeTorrenting/main/build")
        LatestBuild = int(response.text.strip())
        print("CLI | Current downloaded build:",client.CurrentVersion,"and the latest one is:",LatestBuild)
        if client.CurrentVersion != LatestBuild:
            msg = CTkMessagebox(title="Available stable update", message=f"Theres a newer version available \nDo you want to download it? \nCurrent Version: {client.CurrentVersion}\nLatest: {LatestBuild}",
                            icon="question", option_1="No", option_2="Yes")
            response = msg.get()
            if response=="Yes":
               # Maybe in the future, automatic updater?
               webbrowser.open("https://github.com/DEFSecurity/SafeTorrenting/releases/")
            else:
               print("CLI | Exiting Updater")
    except Exception as e:
        print("CLI | "+str(e))