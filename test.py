import unittest
from lib.models import Subscription
from coralillo import Engine
from lib.message_handler import MessageHandler
from lib.config import Config
import os
import json


class BrokerTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config(os.path.dirname(os.path.realpath(__file__)))
        self.config.from_pyfile('settings.py')

        def prefix(cls):
            return 'testing'

        self.eng = Engine()

        Subscription.prefix = classmethod(prefix)
        Subscription.set_engine(self.eng)

        self.eng.lua.drop(args=['*'])

    def test_can_subscribe_to_all_events_of_channel(self):
        s1 = Subscription(channel='a:b:c', event='*').save()

        mh = MessageHandler(self.config)

        e1 = { 'event': 'foo', 'channel': 'a:b:c', 'org': 'testing' }
        e2 = { 'event': 'var', 'channel': 'a:b:c', 'org': 'testing' }
        e3 = { 'event': 'var', 'channel': 'a:b:d', 'org': 'testing' }

        self.assertEqual(list(mh.get_subscribers(e1)), [s1])
        self.assertEqual(list(mh.get_subscribers(e2)), [s1])
        self.assertEqual(list(mh.get_subscribers(e3)), [])

    def test_subscription_respects_events(self):
        s1 = Subscription(channel='a:b:c', event='d').save()
        s2 = Subscription(channel='a:b:c', event='e').save()

        e1 = { 'event': 'd', 'channel': 'a:b:c', 'org': 'testing' }
        e2 = { 'event': 'e', 'channel': 'a:b:c', 'org': 'testing' }

        mh = MessageHandler(self.config)

        self.assertEqual(list(mh.get_subscribers(e1)), [s1])
        self.assertEqual(list(mh.get_subscribers(e2)), [s2])

    def test_subscription_respects_channel_hierarchy(self):
        s1 = Subscription(channel='a', event='z').save()
        s2 = Subscription(channel='a:b', event='z').save()
        s3 = Subscription(channel='a:b:c', event='z').save()

        e1 = { 'event': 'z', 'channel': 'a:b:c', 'org': 'testing' }
        e2 = { 'event': 'z', 'channel': 'a:b:d', 'org': 'testing' }
        e3 = { 'event': 'z', 'channel': 'a:e:f', 'org': 'testing' }

        mh = MessageHandler(self.config)

        self.assertEqual(list(mh.get_subscribers(e1)), [s1, s2, s3])
        self.assertEqual(list(mh.get_subscribers(e2)), [s1, s2])
        self.assertEqual(list(mh.get_subscribers(e3)), [s1])

    def test_event_parsing(self):
        ps = self.eng.redis.pubsub(ignore_subscribe_messages=True)
        ps.psubscribe('*:*:*')

        self.eng.redis.publish('a:b:c', json.dumps({
            'event': 'foo',
            'data': {
                'a': 'b',
            },
        }))

        ps.get_message()
        original_event = ps.get_message()

        mh = MessageHandler(self.config)

        self.assertDictEqual(mh.parse_event(original_event), {
            'data': {'a': 'b'},
            'event': 'foo',
            'channel': 'a:b:c',
            'org': 'a',
        })


if __name__ == '__main__':
    unittest.main()
