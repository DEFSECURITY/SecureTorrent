import random
import platform
import os
GLOBAL_KEY = b'wxHCENbpMitxAt2l1EolOetJYTgMl33IB2Y1Ctriuh4=' # this is use for sending keys and fileinfo
PORT = random.randint(7238, 7243)
APP_DATA = ''
if platform.system() == 'Windows':
    APP_DATA = os.getenv('APP_DATA') + '\\SecureTorrent'
elif platform.system() == 'Linux':
    APP_DATA = os.getenv('HOME') + '/.SecureTorrent'