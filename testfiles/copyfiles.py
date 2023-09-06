import sys
sys.path.append('..')
import os
import shutil
import config
try:
    os.mkdir(config.APP_DATA)
except:
    pass
shutil.copyfile('files.json', config.APP_DATA + '/files.json')
shutil.copyfile('appsettings.json', config.APP_DATA + '/appsettings.json')