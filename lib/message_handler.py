from .logger import log
import json
from importlib import import_module
from .models import Subscription
from coralillo import Engine


class MessageHandler:

    # this function runs in a different process...
    def __init__(self, config):
        self.config = config.copy()
        self.engine = None
        self.handlers = dict()

    # ...than this one, so no conexion can be shared between the two
    def __call__(self, event):
        parsed_event = self.parse_event(event)

        if parsed_event is None:
            return

        self.get_handler('Log').publish(parsed_event)

        for sub in self.get_subscribers(parsed_event):
            self.get_handler(sub.handler).publish(parsed_event)

    def get_subscribers(self, event):
        # we will now check for suscriptions and dispatch them with
        # the handlers
        channel  = event['channel']

        # We need to bind the models to the engine and add prefix function
        self.bind_models(event['org'])

        def filter_events(sub):
            return sub.event == '*' or sub.event == event['event']

        subs = {}

        for sub in filter(filter_events, Subscription.tree_match('channel', channel)):
            if sub.handler not in subs:
                subs[sub.handler] = {
                    'channel': channel,
                    'event': event['event'],
                    'users': [sub.proxy.user.get().to_json()],
                    'handler': sub.handler,
                    'params': [sub.params],
                }
            else:
                subs[sub.handler]['users'].append(sub.proxy.user.get().to_json())
                subs[sub.handler]['params'].append(sub.params)

        return subs.values()

    def get_handler(self, name):
        if name not in self.handlers:
            module = import_module('.handlers.{}_handler'.format(name.lower()), 'lib')
            self.handlers[name] = getattr(module, name+'Handler')(self.config)

        return self.handlers[name]

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

        channel = event['channel'].decode('utf8')

        return {
            'data': data['data'],
            'event': data['event'],
            'channel': channel,
            'org': channel.split(':')[0],
        }

    def bind_models(self, org):
        ''' bind the models to an engine, and set the prefix function '''
        if self.engine is None:
            self.engine = Engine(
                host = self.config['REDIS_HOST'],
                port = self.config['REDIS_PORT'],
                db = self.config['REDIS_DB'],
            )

            Subscription.set_engine(self.engine)

        def prefix(cls):
            return org

        Subscription.prefix = classmethod(prefix)
