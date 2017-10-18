from .logger import log
import json
import redis
from importlib import import_module

# These variables are global to the forked process
red_client = None
handlers = dict()


class MessageHandler:

    # this function runs in a different process...
    def __init__(self, config):
        self.config = config.copy()

    # ...than this one, so no conexion can be shared between the two
    def __call__(self, event):
        parsed_event = self.parse_event(event)

        if parsed_event is None:
            return

        self.get_handler('Log').publish(parsed_event)

        # we will now check for suscriptions and dispatch them with
        # the handlers
        channel  = event['channel'].decode('utf8')
        ch_parts = channel.split(':')
        org      = ch_parts[0]

        subscription_keys = self.get_redis().sunion(
            org + ':subscription:tree_key_name:' + ':'.join(ch_parts[0:i+1])
            for i in range(len(ch_parts))
        )

        for sub_id in subscription_keys:
            print(sub_id)

    def get_handler(self, name):
        global handlers

        if name not in handlers:
            module = import_module('.handlers.{}_handler'.format(name.lower()), 'lib')
            handlers[name] = getattr(module, name+'Handler')(self.config)

        return handlers[name]

    def parse_event(self, event):
        if event['type'] != 'pmessage':
            # it's not even a message... discard
            return

        data = event['data']

        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            log.warning('Couldn\'t decode event\'s JSON data:')
            log.warning(event)
            return

        if 'event' not in data:
            log.warning('Received event without event field')
            log.warning(event)
            return

        if 'data' not in data:
            log.warning('Received event without data field')
            log.warning(event)
            return

        return {
            'data': data,
            'channel': event['channel'].decode('utf8'),
        }

    def get_redis(self):
        global red_client

        if red_client is not None:
            return red_client

        red_client = redis.StrictRedis(
            host = self.config['REDIS_HOST'],
            port = self.config['REDIS_PORT'],
            db = self.config['REDIS_DB'],
        )

        return red_client
