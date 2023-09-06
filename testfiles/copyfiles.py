import sys
sys.path.append('..')
import os
import shutil
import config

os.mkdir(config.APP_DATA)
shutil.copyfile('files.json', config.APP_DATA + '/files.json')
shutil.copyfile('appsettings.json', config.APP_DATA + '/appsettings.json')