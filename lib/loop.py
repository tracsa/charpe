from .logger import log
from .message_handler import MessageHandler
from multiprocessing import Pool
import signal
import pika

# https://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool#1408476

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


class Loop:

    def __init__(self, config):
        self.pool = Pool(config['WORKERS'], init_worker)
        self.config = config
        self.handler = MessageHandler(config)

        log.info('Initialized loop')

    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = self.config['RABBIT_HOST'],
        ))
        channel = connection.channel()

        channel.queue_declare(
            queue = self.config['RABBIT_QUEUE'],
            durable = True,
        )

        channel.basic_consume(
            self.handler,
            queue = self.config['RABBIT_QUEUE'],
            consumer_tag = self.config['RABBIT_CONSUMER_TAG'],
            no_ack = self.config['RABBIT_NO_ACK'],
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            log.info('PVM stopped')
