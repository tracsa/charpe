import unittest
from lib.models import Subscription, User
from coralillo import Engine
from lib.message_handler import MessageHandler
from lib.handlers.email_handler import EmailHandler
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
        User.set_engine(self.eng)

        self.eng.lua.drop(args=['*'])

        self.maxDiff = None

    def test_can_subscribe_to_all_events_of_channel(self):
        u1 = User().save()
        s1 = Subscription(channel='a:b:c', event='*', handler='Email').save()
        s1.proxy.user.set(u1)

        mh = MessageHandler(self.config)

        e1 = { 'event': 'foo', 'channel': 'a:b:c', 'org': 'testing' }
        e2 = { 'event': 'var', 'channel': 'a:b:c', 'org': 'testing' }
        e3 = { 'event': 'var', 'channel': 'a:b:d', 'org': 'testing' }

        out1 = {
            'channel': 'a:b:c',
            'event': 'foo',
            'handler': 'Email',
            'params': [{}],
            'users': [u1.to_json()],
        }
        out2 = {
            'channel': 'a:b:c',
            'event': 'var',
            'handler': 'Email',
            'params': [{}],
            'users': [u1.to_json()],
        }

        self.assertEqual(list(mh.get_subscribers(e1)), [out1])
        self.assertEqual(list(mh.get_subscribers(e2)), [out2])
        self.assertEqual(list(mh.get_subscribers(e3)), [])

    def test_subscription_respects_events(self):
        u1 = User().save()
        s1 = Subscription(channel='a:b:c', event='d', handler='Email').save()
        s1.proxy.user.set(u1)
        u2 = User().save()
        s2 = Subscription(channel='a:b:c', event='e', handler='Email').save()
        s2.proxy.user.set(u2)

        e1 = { 'event': 'd', 'channel': 'a:b:c', 'org': 'testing' }
        e2 = { 'event': 'e', 'channel': 'a:b:c', 'org': 'testing' }

        mh = MessageHandler(self.config)

        o1 = {
            'event': 'd',
            'channel': 'a:b:c',
            'handler': 'Email',
            'users': [u1.to_json()],
            'params': [{}],
        }
        o2 = {
            'event': 'e',
            'channel': 'a:b:c',
            'handler': 'Email',
            'users': [u2.to_json()],
            'params': [{}],
        }

        self.assertEqual(list(mh.get_subscribers(e1)), [o1])
        self.assertEqual(list(mh.get_subscribers(e2)), [o2])

    def test_subscription_respects_channel_hierarchy(self):
        u1 = User().save()
        u2 = User().save()
        u3 = User().save()

        s1 = Subscription(channel='a', event='z', handler='Email').save()
        s1.proxy.user.set(u1)
        s2 = Subscription(channel='a:b', event='z', handler='Email').save()
        s2.proxy.user.set(u2)
        s3 = Subscription(channel='a:b:c', event='z', handler='Email').save()
        s3.proxy.user.set(u3)

        e1 = { 'event': 'z', 'channel': 'a:b:c', 'org': 'testing' }
        e2 = { 'event': 'z', 'channel': 'a:b:d', 'org': 'testing' }
        e3 = { 'event': 'z', 'channel': 'a:e:f', 'org': 'testing' }

        o1 = { 'channel': 'a:b:c', 'event': 'z', 'handler': 'Email', 'params': [{}, {}, {}], 'users': [u1.to_json(), u2.to_json(), u3.to_json()] }
        o2 = { 'channel': 'a:b:d', 'event': 'z', 'handler': 'Email', 'params': [{}, {}], 'users': [u1.to_json(), u2.to_json()] }
        o3 = { 'channel': 'a:e:f', 'event': 'z', 'handler': 'Email', 'params': [{}], 'users': [u1.to_json()] }

        mh = MessageHandler(self.config)

        self.assertEqual(list(mh.get_subscribers(e1)), [o1])
        self.assertEqual(list(mh.get_subscribers(e2)), [o2])
        self.assertEqual(list(mh.get_subscribers(e3)), [o3])

    def test_send_email(self):
        u1 = User(name='John', last_name='Doe', email='john@testing.com').save()

        eh = EmailHandler(self.config)

        with eh.mail.record_messages() as outbox:
            eh.publish({
                'channel': 'a:b:c',
                'event': 'demo-event',
                'users': [u1.to_json()],
                'handler': 'Email',
                'params': [{'a': '1'}],
            })

            self.assertEqual(len(outbox), 1)

            msg = outbox[0]
            self.assertEqual(msg.subject, 'Evento demo')
            self.assertEqual(msg.bcc, ['{} {} <{}>'.format(u1.name, u1.last_name, u1.email)])

    def test_group_subscriptions(self):
        u1 = User().save()
        u2 = User().save()

        s1 = Subscription(channel='a:b', event='z', handler='Email', params={'a': 1}).save()
        s1.proxy.user.set(u1)
        s2 = Subscription(channel='a:b', event='*', handler='Email', params={'a': 2}).save()
        s2.proxy.user.set(u2)
        s3 = Subscription(channel='a:b', event='z', handler='Sms', params={'a': 3}).save()
        s3.proxy.user.set(u1)
        s4 = Subscription(channel='a:b', event='*', handler='Sms', params={'a': 4}).save()
        s4.proxy.user.set(u2)

        mh = MessageHandler(self.config)

        subs = list(mh.get_subscribers({
            'event': 'z',
            'channel': 'a:b:c',
            'org': 'testing',
        }))

        self.assertDictEqual(subs[0], {
            'channel': 'a:b:c',
            'event': 'z',
            'users': [u1.to_json(), u2.to_json()],
            'handler': 'Email',
            'params': [{'a': '1'}, {'a': '2'}],
        })
        self.assertDictEqual(subs[1], {
            'channel': 'a:b:c',
            'event': 'z',
            'users': [u1.to_json(), u2.to_json()],
            'handler': 'Sms',
            'params': [{'a': '3'}, {'a': '4'}],
        })

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
