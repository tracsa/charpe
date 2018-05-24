from importlib import import_module
import logging
import simplejson as json


LOGGER = logging.getLogger(__name__)


class Handler:

    # this function runs in a different process...
    def __init__(self, config):
        self.config = config.copy()
        self.handlers = dict()

    # ...than this one, so no conexion can be shared between the two
    def __call__(self, channel, method, properties, body: bytes):
        parsed_event = self.parse_event(body)

        if parsed_event is None:
            return

        self.get_medium('Email').publish(parsed_event)

    def get_medium(self, name):
        if name not in self.handlers:
            module = import_module(
                'charpe.mediums.{}_handler'.format(name.lower()),
            )
            self.handlers[name] = getattr(module, name+'Handler')(self.config)

        return self.handlers[name]

    def parse_event(self, payload):
        try:
            data = json.loads(payload)
        except json.decoder.JSONDecodeError as e:
            LOGGER.warning('Couldn\'t decode event\'s JSON data:')
            return

        return data
