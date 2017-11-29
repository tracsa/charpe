from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import os
import logging

from . import BaseHandler
from .. import mail
from ..template_filters import datetimeformat, diffinhours

SUBJECTS = {
    'alarm': Template('[Fleety] Alarma tipo {{ type }} para {{ device.name }}'),
    'geofence-enter': Template('[Fleety] {{ device.name }} entró a {{ geofence.name }}'),
    'geofence-leave': Template('[Fleety] {{ device.name }} salió de {{ geofence.name }}'),
    'trip-started': Template('[Fleety] {{ device.name }} inició viaje desde {{ trip.origin }} hasta {{ trip.destination }}'),
    'trip-finished': Template('[Fleety] {{ device.name }} terminó viaje desde {{ trip.origin }} hasta {{ trip.destination }}'),
    'trip-stop': Template('[Fleety] {{ device.name }} se detivo durante el viaje'),
    'trip-offroute': Template('[Fleety] {{ device.name }} se salió de la ruta planeada'),
    'user-registered': Template('[Fleety] Bienvenido a Fleety'),

    'server-error': Template('[Fleety] Server error'),
}

class EmailHandler(BaseHandler):

    def initialize(self):
        self.jinja = Environment(
            loader = FileSystemLoader(os.path.join(os.path.dirname(__name__), 'templates')),
            autoescape = select_autoescape(['html']),
        )
        self.jinja.filters['datetimeformat'] = datetimeformat
        self.jinja.filters['diffinhours'] = diffinhours
        self.mail = mail.Mail(self.config)

    def render_template(self, name, **kwargs):
        template = self.jinja.get_template('{}.html'.format(name),
            globals = {
                'config': self.config,
            },
        )

        return template.render(**kwargs)

    def publish(self, message):
        if message['event'] not in SUBJECTS:
            return logging.error('Subject for event {} not defined, email will not be sent'.format(message['event']))

        def build_recipient(user):
            return '{} {} <{}>'.format(
                user['name'],
                user['last_name'] if user['last_name'] else '',
                user['email'],
            )

        recipients = list(map(
            build_recipient,
            message['users']
        ))

        subject = SUBJECTS[message['event']].render(**message['data'])

        msg = mail.Message(
            subject = subject,
            bcc = recipients,
        )

        msg.html = self.render_template(message['event'], **message['data'])

        self.mail.send(msg)

        logging.info('Email for event {} sent to {}'.format(message['event'], ', '.join(recipients)))
