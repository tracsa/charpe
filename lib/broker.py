from .logger import log

class Broker:

    def __init__(self):
        log.info('Initialized broker')

    def run(self):
        log.info('Running broker')
