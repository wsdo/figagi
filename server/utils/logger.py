'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-14 09:47:01
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-16 20:30:49
Description: create logger
'''
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from logging import Logger

def create_logger(name: str | None) -> Logger:
    # Create a logger
    # logger = logging.getLogger(name)
    # logger.setLevel(logging.DEBUG)

    # Create a file handler
    # os.makedirs('logs', exist_ok=True)
    # fh = TimedRotatingFileHandler('logs/agi-ai-search-server.log', interval=1, when='D')
    # fh.setLevel(logging.DEBUG)

    # Create a console handler
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)

    # # Create a formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # ch.setFormatter(formatter)

    # # Add handlers to the logger
    # logger.addHandler(fh)
    # logger.addHandler(ch)

    return logger
