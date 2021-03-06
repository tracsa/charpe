from unittest.mock import MagicMock
import pytest

from charpe.mediums.email_handler import EmailHandler
from charpe.errors import InsuficientInformation


def test_send_requirements(config):
    handler = EmailHandler(config)

    with pytest.raises(InsuficientInformation):
        handler.publish({})

    with pytest.raises(InsuficientInformation):
        handler.publish({
            'recipient': 'charpe@mailinator.com',
        })

    with pytest.raises(InsuficientInformation):
        handler.publish({
            'recipient': 'charpe@mailinator.com',
            'subject': 'The subject',
        })


def test_send(config, caplog, mocker):
    the_mock = MagicMock()
    smoke = MagicMock(return_value=the_mock)
    mocker.patch('smtplib.SMTP', new=smoke)

    handler = EmailHandler(config)

    handler.publish({
        'recipient': 'charpe@mailinator.com',
        'subject': 'The subject',
        'data': {
            'content': 'El mensaje',
        },
    })

    the_mock.send_message.assert_called_once()
    msg = the_mock.send_message.call_args[0][0]

    assert msg.get('From') == config['MAIL_DEFAULT_SENDER']
    assert msg.get('To') == 'charpe@mailinator.com'

    html, text = msg.get_payload()

    assert 'El mensaje' in text.get_payload()
    assert '<p>El mensaje</p>' in html.get_payload()

    the_mock.quit.assert_called_once()
