import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)


import os
import logging
import datetime as dt


from collections import namedtuple

# Ensure if dir exists
def ensure_dir(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)


'''
Start logger config
'''
LOGS_DIR = 'logs'
LOG_FILENAME = 'run_{}.log'.format(dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

ensure_dir('logs')

# Logger formatter
log_formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s')
logger = logging.getLogger()

# Logger file handler
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, LOG_FILENAME))
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Logger console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# Logger level
logger.setLevel(os.environ.get('LOG_LEVEL') or logging.INFO)
logger.setLevel(os.environ.get('LOG_LEVEL') or logging.DEBUG)
'''
End logger config
'''

