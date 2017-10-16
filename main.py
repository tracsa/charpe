from lib.logger import log
from lib.broker import Broker
from lib.config import Config
import os

if __name__ == '__main__':
    # Logging stuff
    import logging

    logging.basicConfig(
            format = '[%(asctime)s] %(module)s %(levelname)s %(message)s %(filename)s:%(lineno)s',
        level  = logging.DEBUG,
    )
    log.debug('de')

    # Load the config
    config = Config(os.path.dirname(os.path.realpath(__file__)))
    config.from_pyfile('settings.py')
    config.from_envvar('BROKER_SETTINGS', silent=True)

    # Run the broker class
    brok = Broker(config)
    brok.run()
