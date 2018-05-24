from charpe.handler import Handler


def test_load_handler(config):
    handler = Handler(config)

    handler.get_medium('Email')
