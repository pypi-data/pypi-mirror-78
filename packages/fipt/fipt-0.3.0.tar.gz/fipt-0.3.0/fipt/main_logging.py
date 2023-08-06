

import logging
from logging import Formatter
from copy import copy

MAPPING = {
    'DEBUG'   : 37, # white
    'INFO'    : 36, # cyan
    'WARNING' : 33, # yellow
    'ERROR'   : 31, # red
    'CRITICAL': 41, # white on red bg
}

PREFIX = '\033['
SUFFIX = '\033[0m'

class ColoredFormatter(Formatter):

    def __init__(self, patern):
        Formatter.__init__(self, patern)

    def format(self, record):
        colored_record = copy(record)
        levelname = colored_record.levelname
        seq = MAPPING.get(levelname, 37) # default white
        colored_levelname = ('{0}{1}m{2}{3}') \
            .format(PREFIX, seq, levelname, SUFFIX)
        colored_record.levelname = colored_levelname
        return Formatter.format(self, colored_record)

# from colored_log import ColoredFormatter

# # Create top level logger
# log = logging.getLogger()

# # Add console handler using our custom ColoredFormatter
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# cf = ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
# ch.setFormatter(cf)
# log.addHandler(ch)

def configure_colored_logger(remove_existing_handlers=True, level=logging.INFO):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if remove_existing_handlers:
        for hdl in root_logger.handlers.copy():
            root_logger.removeHandler(hdl)

    # Add console handler using our custom ColoredFormatter
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
#     cf = ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
    cf = ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s")
    ch.setFormatter(cf)
    root_logger.addHandler(ch)
