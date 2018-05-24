from jinja2 import Template
import logging
import requests

from charpe.mediums import BaseMedium

LOGGER = logging.getLogger(__name__)

TEMPLATES = {
    'server-error': Template('--'),
}


class TelegramHandler(BaseMedium):

    def publish(self, message):
        if message['event'] not in TEMPLATES:
            return LOGGER.error(
                'Template for event {} not defined, telegram'
                'message will not be sent'.format(
                    message['event']
                )
            )

        for user in message['users']:
            if not user['telegram_chat_id']:
                continue

            msg = TEMPLATES[message['event']].render(**{
                **message['data'],
                **self.config
            })

            requests.post('https://api.telegram.org/bot{}/sendMessage'.format(
                self.config['TELEGRAM_BOT_KEY']
            ), data={
                'chat_id': user['telegram_chat_id'],
                'text': msg,
                'parse_mode': 'Markdown',
            })

        LOGGER.info('Telegram message for event {} sent'.format(
            message['event']
        ))
