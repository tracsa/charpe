from lib.logger import log
from lib.broker import Broker
from lib.config import Config
import time
import os

if __name__ == '__main__':
    # Load the config
    config = Config(os.path.dirname(os.path.realpath(__file__)))
    config.from_pyfile('settings.py')
    config.from_envvar('BROKER_SETTINGS', silent=True)

    # Set the timezone
    os.environ['TZ'] = config.TIMEZONE
    time.tzset()

    # Logging stuff
    import logging

    logging.basicConfig(
        format = '[%(levelname)s] %(message)s - %(filename)s:%(lineno)s',
        level  = config.LOG_LEVEL,
    )

    # Run the broker class
    brok = Broker(config)
    brok.run()
