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

try:
    response = requests.get(config.GitHub + "/main/build")
    latest_build = int(response.text.strip())
    logger.log("Current build:", config.CurrentVersion, "and the latest one is:", latest_build)
    
    if config.CurrentVersion != latest_build: # for e.g.: 9 is not equal 10 - update, or 10 is not equal 9, update.
        msg = CTkMessagebox( # this code is causing a blank window to be opened
            title="Available update",
            message=f"There's a newer version available.\nDo you want to download it?\nCurrent Version: {config.CurrentVersion} Latest: {latest_build}",
            icon="question",
            option_1="No",
            option_2="Yes"
        )
        
        response = msg.get()
        
        if response == "Yes":
            logger.log("Opening GitHub to download the new version...")
            webbrowser.open(config.GitHub + "/releases/")
            exit()
except Exception as e:
    logger.error(e)