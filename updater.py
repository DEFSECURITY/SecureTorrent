# Updater: 9-DEV
import requests
import client
from CTkMessagebox import CTkMessagebox
import webbrowser

def update():
    try:
        response = requests.get("https://raw.githubusercontent.com/DEFSECURITY/SafeTorrenting/main/build")
        latest_build = int(response.text.strip())
        print("CLI | Current downloaded build:", client.CurrentVersion, "and the latest one is:", latest_build)
        
        if client.CurrentVersion != latest_build: # for e.g.: 9 => 10
            msg = CTkMessagebox(
                title="Available stable update",
                message=f"There's a newer version available \nDo you want to download it? \nCurrent Version: {client.CurrentVersion}\nLatest: {latest_build}",
                icon="question",
                option_1="No",
                option_2="Yes"
            )
            
            response = msg.get()
            
            if response == "Yes":
                webbrowser.open("https://github.com/DEFSecurity/SafeTorrenting/releases/")
            else:
                print("CLI | Exiting Updater")
    except Exception as e:
        print("CLI | " + str(e))