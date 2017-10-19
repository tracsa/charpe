import unittest
from lib.models import Subscription
from coralillo import Engine
from lib.config import Config
import os

if __name__ == '__main__':
    config = Config(os.path.dirname(os.path.realpath(__file__)))
    config.from_pyfile('settings.py')
    config.from_pyfile('settings_testing.py')

    engine = Engine(
        host = config['REDIS_HOST'],
        port = config['REDIS_PORT'],
        db   = config['REDIS_DB'],
    )

    engine.lua.drop(args=['*'])

    def prefix(cls):
        return 'testing'

    Subscription.set_engine(engine)
    Subscription.prefix = classmethod(prefix)

    s1 = Subscription(
        channel = 'testing:class:theid',
        event = 'an-event',
        handler = 'email',
        params = {
            'a': '1',
        },
    ).save()
