from charpe.handler import Handler


class MockMethod:

    def __init__(self, medium):
        self.routing_key = medium


def test_call_bad_message(config, caplog):
    handler = Handler(config)
    method = MockMethod('email')

    handler(None, method, None, '')

    rec = caplog.records[0]
    assert rec.levelname == 'ERROR'
    assert 'Couldn\'t decode event\'s JSON data' in caplog.text


def test_call_couldnt_import_medium(config, caplog):
    handler = Handler(config)
    method = MockMethod('foo')

    handler(None, method, None, '{}')

    rec = caplog.records[0]
    assert rec.levelname == 'ERROR'
    assert 'Could not import provider module charpe.mediums.foo_handler' in caplog.text


def test_call_email_insuficient_info(config, caplog):
    handler = Handler(config)
    method = MockMethod('email')

    handler(None, method, None, '{}')

    rec = caplog.records[0]
    assert rec.levelname == 'ERROR'
    assert 'Needed key \'email\'' in caplog.text
