import random
import platform
from pathlib import Path
INIT_KEY = b'wxHCENbpMitxAt2l1EolOetJYTgMl33IB2Y1Ctriuh4=' # this is use for sending keys and fileinfo
PORT = 7238
APP_DATA = ''
if platform.system() == 'Windows':
    APP_DATA = str(Path.home()) + '\\AppData\\Roaming\\SecureTorrent'
elif platform.system() == 'Linux':
    APP_DATA = str(Path.home()) + '/.SecureTorrent'

Title = 'SecureTorrent'
DiscordLink = 'https://discord.gg/YhFsd7TVkN'
CurrentVersion = 9
GitHub = 'https://raw.githubusercontent.com/DEFSECURITY/SecureTorrent'