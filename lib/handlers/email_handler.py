from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import os
import logging

from . import BaseHandler
from .. import mail
from ..template_filters import datetimeformat, diffinhours

SUBJECTS = {
    'report-finished': Template('[Fleety] Tu reporte {% if report.name %}{{ report.name }}{% else %}{{ report.builder }}{% endif %} está listo'),
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
        recipients = [message['email']]

        subject = 'Tarea asignada'

        msg = mail.Message(
            subject=subject,
            recipients=recipients,
            sender='procesos@tracsa.com.mx',
        )

        msg.html = self.render_template('cacahuate')

        self.mail.send(msg)

        logging.info('Email for event {} sent to {}'.format(message['event'], ', '.join(recipients)))
