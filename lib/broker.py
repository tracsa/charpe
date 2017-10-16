from .logger import log
from .handler import handler
from multiprocessing import Pool
import redis
import time
import signal

# https://stackoverflow.com/questions/27745842/redis-pubsub-and-message-queueing
# https://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool#1408476

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


class Broker:

    def __init__(self):
        self.redis = redis.StrictRedis() # TODO read connections settings
        self.pool = Pool(4, init_worker) # TODO make this a setting

        log.info('Initialized broker')

    def run(self):
        log.info('Running broker')

        ps = self.redis.pubsub()

        ps.psubscribe('*') # TODO this might me a setting

        with self.pool as pool:
            while True:
                try:
                    message = ps.get_message()

                    if message:
                        pool.apply_async(handler, [message])

                    time.sleep(0.001) # TODO make this a config
                except KeyboardInterrupt as e:
                    break

        log.info('Stopped broker')
