# -*- coding: utf-8 -*-

import logging
import sys
from logging.handlers import  TimedRotatingFileHandler
import time

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname) %(pathname)s %(filename)s %(funcName)s %(thread)s %(threadName)s %(process)s-8s: %(message)s')
file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

count = 0
while(count<5):
    logger.info("Start print log")
    logger.debug("Do something")
    logger.warning("Something maybe fail.")
    logger.info("Finish")
    print('\n')
    count = count + 1
    time.sleep(2)

