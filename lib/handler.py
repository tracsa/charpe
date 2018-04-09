from .logger import log
import simplejson as json
from importlib import import_module
from .models import Subscription, User


class Handler:

    # this function runs in a different process...
    def __init__(self, config):
        self.config = config.copy()
        self.handlers = dict()

    # ...than this one, so no conexion can be shared between the two
    def __call__(self, channel, method, properties, body:bytes):
        parsed_event = self.parse_event(body)

        if parsed_event is None:
            return

        # for sub in self.get_subscribers(parsed_event):
        self.get_handler('Email').publish(parsed_event)

    def get_subscribers(self, event):
        ''' Reads and groups subscriptions to an event '''
        channel  = event['channel']

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
                    'data': event['data'] if 'data' in event else dict(),
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

    def parse_event(self, payload):
        try:
            data = json.loads(payload)
        except json.decoder.JSONDecodeError as e:
            log.warning('Couldn\'t decode event\'s JSON data:')
            return

        return data
