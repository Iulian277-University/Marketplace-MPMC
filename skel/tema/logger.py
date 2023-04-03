"""
This module represents the Logger.
"""

import sys
import time
import logging
import logging.handlers

class Logger:
    """
    Class that represents a logger. It's used for debugging purposes.
    """

    def __init__(self, name):
        """
        Constructor
        
        :type name: String
        :param name: the name of the logger
        """
        self.logger = logging.getLogger(name)
        self.logger.propagate = False

        self.handler = logging.handlers.RotatingFileHandler('marketplace.log',
                                                            mode='w',
                                                            maxBytes=1*1024*1024,
                                                            backupCount=5)
        self.handler.setFormatter(
            logging.Formatter('[%(asctime)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)
        logging.Formatter.converter = time.gmtime

    def log(self, msg):
        """
        Logs a message.
        """
        self.logger.info(msg)
        
    @staticmethod
    def disable():
        """
        Disables the logger.
        """
        logging.disable(sys.maxsize)
    