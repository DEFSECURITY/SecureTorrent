# updater.js
import requests
import client
from tkinter import messagebox
import webbrowser

def UpdateCheck():
    try:
        response = requests.get("https://raw.githubusercontent.com/DEFSECURITY/SafeTorrenting/main/build")
        LatestBuild = int(response.text.strip())
        print("CLI | Current downloaded build:",client.CurrentVersion)
        print("CLI | Latest build from GitHub:",LatestBuild)
        if client.CurrentVersion != LatestBuild: # or > ?
            result = messagebox.askyesno("Available update", "Theres a newer version available. \nDo you want to download it?")
            if result:
                webbrowser.open("https://github.com/DEFSecurity/SafeTorrenting/releases/")
            else:
                exit
        else:
            print("CLI | Exiting Updater")
    except Exception as e:
        print("CLI Updater | "+str(e))