from lib.logger import log
from lib.broker import Broker

if __name__ == '__main__':
    # Logging stuff
    import logging

    logging.basicConfig(
            format = '[%(asctime)s] %(module)s %(levelname)s %(message)s %(filename)s:%(lineno)s',
        level  = logging.DEBUG,
    )
    log.debug('de')

    # run the broker class
    brok = Broker()
    brok.run()
