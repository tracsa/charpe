from .logger import log
from .message_handler import MessageHandler
from multiprocessing import Pool
import redis
import time
import signal

# https://stackoverflow.com/questions/27745842/redis-pubsub-and-message-queueing
# https://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool#1408476

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


class Broker:

    def __init__(self, config):
        self.redis = redis.StrictRedis(
            host             = config.REDIS_HOST,
            port             = config.REDIS_PORT,
            db               = config.REDIS_DB,
            decode_responses = True,
        )
        self.pool = Pool(config.WORKERS, init_worker)
        self.config = config
        self.handler = MessageHandler(config)

        log.info('Initialized broker')

    def run(self):
        log.info('Running broker')

        ps = self.redis.pubsub()

        ps.psubscribe(self.config.CHANNEL_PATTERN)

        with self.pool as pool:
            while True:
                try:
                    message = ps.get_message()

                    if message:
                        pool.apply_async(self.handler,
                            args           = [message],
                        )

                    time.sleep(self.config.SLEEP_TIME)
                except KeyboardInterrupt as e:
                    break

        log.info('Stopped broker')
