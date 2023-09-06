# Updater: 9-DEV
import sys
sys.path.append('core')
import os
import requests
import config
from CTkMessagebox import CTkMessagebox
import webbrowser
import logger as Logger

logger = Logger.logger(os.path.basename(__file__))

def update():
    try:
        response = requests.get("https://raw.githubusercontent.com/DEFSECURITY/SafeTorrenting/main/build")
        latest_build = int(response.text.strip())
        logger.log("Current downloaded build:", config.CurrentVersion, "and the latest one is:", latest_build)
        
        if config.CurrentVersion != latest_build: # for e.g.: 9 is not equal 10 - update, or 10 is not equal 9, update.
            msg = CTkMessagebox(
                title="Available stable update",
                message=f"There's a newer version available \nDo you want to download it?\nCurrent Version: {config.CurrentVersion}\nLatest: {latest_build}",
                icon="question",
                option_1="No",
                option_2="Yes"
            )
            
            response = msg.get()
            
            if response == "Yes":
                webbrowser.open("https://github.com/DEFSecurity/SafeTorrenting/releases/")
                exit()
    except Exception as e:
        logger.error(e)