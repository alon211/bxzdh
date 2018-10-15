import logging
import os
def setlog():
    logfile = 'log.txt'
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logfile = 'log.txt'
    fh = logging.FileHandler(logfile, mode='a', encoding='utf-8')
    fh.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

