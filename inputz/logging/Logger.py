import logging
from logging import getLogger


class Logger(object):
    """
    Logger

    This class is a libary made for easy and uniform implementation of logging.
    """

    def __init__(self):
        logging.basicConfig(
            format='[%(name)s][%(levelname)s]: %(message)s'
        )

        self.log = getLogger(self.__class__.__name__)
        # self.log.setLevel(DEBUG)
        self.log.setLevel(logging.INFO)
