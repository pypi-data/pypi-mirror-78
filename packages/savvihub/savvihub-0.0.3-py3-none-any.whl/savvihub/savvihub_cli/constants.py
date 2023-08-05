import os
from pathlib import Path


HOST_URL = 'http://localhost:10000'
CUR_DIR = os.getcwd()
DEFAULT_SAVVI_DIR = os.path.join(str(Path.home()), '.savvihub')
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_SAVVI_DIR, 'config.yml')
