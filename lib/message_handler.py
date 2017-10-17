from .logger import log
from .handlers.log_handler import LogHandler


class MessageHandler:

    def __init__(self, config):
        self.log = LogHandler(config.copy())

    def __call__(self, data):
        self.log.publish(data)
