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

def end_task(res):
    pass

def task_failed(error):
    log.warning('Failed task with error: "{} {}"'.format(type(error).__name__, error))


class Broker:

    def __init__(self, config):
        self.redis = redis.StrictRedis(
            host = config.REDIS_HOST,
            port = config.REDIS_PORT,
            db = config.REDIS_DB,
        )
        self.pool = Pool(config.WORKERS, init_worker)
        self.config = config

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
                        pool.apply_async(handler,
                            args           = [message],
                            callback       = end_task,
                            error_callback = task_failed,
                        )

                    time.sleep(self.config.SLEEP_TIME)
                except KeyboardInterrupt as e:
                    break

        log.info('Stopped broker')
