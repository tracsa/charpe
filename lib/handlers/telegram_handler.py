from jinja2 import Template
import logging
import requests

from . import BaseHandler

TEMPLATES = {
    'alarm': Template('\u26a0 #Alarma tipo #{{ type }} para {{ device.name }} \u26a0'),
}

class TelegramHandler(BaseHandler):

    def publish(self, message):
        if message['event'] not in TEMPLATES:
            return logging.error('Template for event {} not defined, telegram message will not be sent'.format(message['event']))

        for user in message['users']:
            if not user['telegram_chat_id']:
                continue

            msg = TEMPLATES[message['event']].render(**message['data'])

            requests.post('https://api.telegram.org/bot{}/sendMessage'.format(self.config['TELEGRAM_BOT_KEY']), data={
                'chat_id': user['telegram_chat_id'],
                'text': msg,
            })

        logging.info('Telegram message for event {} sent'.format(message['event']))
