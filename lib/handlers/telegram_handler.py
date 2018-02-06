from jinja2 import Template
import logging
import requests

from . import BaseHandler

TEMPLATES = {
    'alarm': Template('⚠️ #Alarma tipo #{{ type }} para el dispositivo [{{ device.name }}]({{ URL_PROTOCOL }}://{{ org_name }}.getfleety.{{ URL_SUBDOMAIN }}/#/device/{{ device.id }}) ⚠️'),
    'geofence-enter': Template('⭕️ ⬅️ 🚲 El dispositivo {{ device.name }} #entróAGeocerca {{ geofence.name }}'),
    'geofence-leave': Template('🚲 ⬅️ ⭕️ El dispositivo {{ device.name }} #salióDeGeocerca {{ geofence.name }}'),
    'report-finished': Template('📈 Tu reporte {% if report.name %}{{ report.name }}{% else %}{{ report.builder }}{% endif %} está listo, descárgalo [aqui]({{ report.url }}).'),
}

class TelegramHandler(BaseHandler):

    def publish(self, message):
        if message['event'] not in TEMPLATES:
            return logging.error('Template for event {} not defined, telegram message will not be sent'.format(message['event']))

        for user in message['users']:
            if not user['telegram_chat_id']:
                continue

            msg = TEMPLATES[message['event']].render(**{**message['data'], **self.config})

            requests.post('https://api.telegram.org/bot{}/sendMessage'.format(self.config['TELEGRAM_BOT_KEY']), data={
                'chat_id': user['telegram_chat_id'],
                'text': msg,
                'parse_mode': 'Markdown',
            })

            if 'device' in message['data']:
                requests.post('https://api.telegram.org/bot{}/sendLocation'.format(self.config['TELEGRAM_BOT_KEY']), data={
                    'chat_id': user['telegram_chat_id'],
                    'latitude': message['data']['device']['last_pos']['lat'],
                    'longitude': message['data']['device']['last_pos']['lon'],
                })

        logging.info('Telegram message for event {} sent'.format(message['event']))
