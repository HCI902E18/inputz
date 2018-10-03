import logging
from logging import getLogger, DEBUG


class Logger(object):
    def __init__(self):
        logging.basicConfig(
            format='[%(name)s][%(levelname)s]: %(message)s'
        )

        self.log = getLogger(self.__class__.__name__)
        self.log.setLevel(DEBUG)
