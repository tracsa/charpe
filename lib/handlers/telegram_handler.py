import logging
import requests

from . import BaseHandler

TEMPLATES = {
    'alarm': 'Alarma tipo {} para {}',
    'geofence-enter': '{{ device.name }} entró a {{ geofence.name }}',
    'geofence-leave': '{{ device.name }} salió de {{ geofence.name }}',
    'trip-started': '{{ device.name }} inició viaje desde {{ trip.origin }} hasta {{ trip.destination }}',
    'trip-finished': '{{ device.name }} terminó viaje desde {{ trip.origin }} hasta {{ trip.destination }}',
    'trip-stop': '{{ device.name }} se detivo durante el viaje',
    'trip-offroute': '{{ device.name }} se salió de la ruta planeada',
    'user-registered': 'Bienvenido a Fleety',
    'report-finished': 'Tu reporte {% if report.name %}{{ report.name }}{% else %}{{ report.builder }}{% endif %} está listo',

    'server-error': 'Server error',
}

class TelegramHandler(BaseHandler):

    def publish(self, message):
        for user in message['users']:
            if not user['telegram_chat_id']:
                continue

            requests.post('https://api.telegram.org/bot{}/sendMessage'.format(self.config['TELEGRAM_BOT_KEY']), data={
                'chat_id': user['telegram_chat_id'],
                'text': message['event'],
            })

            from pprint import pprint

            pprint(message)

        logging.info('Telegram message for event {} sent'.format(message['event']))
