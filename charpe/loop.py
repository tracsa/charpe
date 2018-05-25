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
        LOGGER.info('Declared exchange {}'.format(
            self.config['RABBIT_NOTIFY_EXCHANGE']
        ))

        queue_name = self.config['RABBIT_QUEUE']
        result = channel.queue_declare(
            queue=queue_name,
            durable=True,
        )
        LOGGER.info('Declared queue {}'.format(
            queue_name
        ))

        for medium in self.config['MEDIUMS']:
            channel.queue_bind(
                exchange=self.config['RABBIT_NOTIFY_EXCHANGE'],
                queue=queue_name,
                routing_key=medium,
            )
            LOGGER.info('Bound queue with routing key: {}'.format(
                medium,
            ))

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
