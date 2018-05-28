from importlib import import_module
import logging
import simplejson as json
from case_conversion import pascalcase

from charpe.errors import InsuficientInformation, MisconfiguredProvider, \
    InsuficientInformation, MediumError


LOGGER = logging.getLogger(__name__)


class Handler:

    # this function runs in a different process...
    def __init__(self, config):
        self.config = config.copy()
        self.handlers = dict()

    # ...than this one, so no conexion can be shared between the two
    def __call__(self, channel, method, properties, body: bytes):
        medium = method.routing_key

        try:
            data = json.loads(body)
        except json.decoder.JSONDecodeError:
            return LOGGER.error('Couldn\'t decode event\'s JSON data')

        try:
            self.get_medium(medium).publish(data)
        except MisconfiguredProvider as e:
            return LOGGER.error(str(e))
        except InsuficientInformation as e:
            return LOGGER.error(str(e))
        except MediumError as e:
            return LOGGER.error(str(e))

    def get_medium(self, name):
        if name not in self.handlers:
            module_name = 'charpe.mediums.{}_handler'.format(name)
            class_name = pascalcase(name) + 'Handler'

            try:
                module = import_module(module_name)
                self.handlers[name] = getattr(module, class_name)(self.config)
            except ImportError:
                raise MisconfiguredProvider(
                    'Could not import provider module {}'.format(module_name)
                )
            except AttributeError:
                raise MisconfiguredProvider(
                    'Provider module {} does not define class {}'.format(
                        module_name,
                        class_name,
                    )
                )

        return self.handlers[name]
