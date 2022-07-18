import json
import logging
import pika


class CharpeHandler(logging.Handler):

    def __init__(self, host, medium, exchange, params, service_name, **kwargs):
        super().__init__()

        self.host = host
        self.medium = medium
        self.exchange = exchange
        self.params = params
        self.service_name = service_name
        self.port = kwargs.get('port', 5672)
        self.credentials = pika.PlainCredentials(
            username=kwargs.get('username', 'guest'),
            password=kwargs.get('password', 'guest'),
        )

    def emit(self, record):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
        ))
        channel = connection.channel()

        try:
            traceback = record.getMessage()

            params = self.params.copy()
            params['data'] = {
                'traceback': traceback,
                'service_name': self.service_name,
            }

            channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.medium,
                body=json.dumps(params),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )

        except Exception:
            self.handleError(record)
        else:
            channel.close()
