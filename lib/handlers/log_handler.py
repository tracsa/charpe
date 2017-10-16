from . import Handler
import logging


class LogHandler(Handler):

    def publish(self, message):
        logging.debug('Wil write message to log')
