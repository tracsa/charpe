import logging
import json
from unittest.mock import MagicMock

from charpe import CharpeHandler


def test_logs_complete_message(mocker):
    mocked_connection = MagicMock()
    mocker.patch(
        'pika.BlockingConnection',
        new=mocked_connection
    )
    msg = 'Traceback: Most recent call last'

    logger = logging.getLogger('foo')

    logger.addHandler(CharpeHandler('host', 'medium', 'exchange', {
        'params': 1,
    }, 'service'))

    logger.error(msg)

    assert json.loads(
        mocked_connection.mock_calls[2][2]['body']
    )['data']['traceback'] == msg
