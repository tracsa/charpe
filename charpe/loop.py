from multiprocessing import Pool
import signal
import pika
import logging

from charpe.handler import Handler

LOGGER = logging.getLogger(__name__)


class Loop:

    def __init__(self, config):
        self.config = config
        self.handler = Handler(config)

        LOGGER.info('Initialized loop')

    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config['RABBIT_HOST'],
        ))
        channel = connection.channel()

        channel.exchange_declare(
            exchange=self.config['RABBIT_NOTIFY_EXCHANGE'],
            exchange_type='direct'
        )

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(
            exchange=self.config['RABBIT_NOTIFY_EXCHANGE'],
            queue=queue_name,
            routing_key='email',
        )

        channel.basic_consume(
            self.handler,
            queue=queue_name,
            consumer_tag=self.config['RABBIT_CONSUMER_TAG'],
            no_ack=True
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            LOGGER.info('PVM stopped')
