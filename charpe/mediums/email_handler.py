from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from jinja2.exceptions import TemplateNotFound
import logging
import os
import smtplib

from charpe.mediums import BaseMedium
from charpe.template_filters import datetimeformat, diffinhours
from charpe.errors import InsuficientInformation, MediumError

SUBJECTS = {
    'subject': Template('---'),
}

LOGGER = logging.getLogger(__name__)


class EmailHandler(BaseMedium):

    def initialize(self):
        self.jinja = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), '../templates')
            ),
            autoescape=select_autoescape(['html']),
        )

        self.jinja.filters['datetimeformat'] = datetimeformat
        self.jinja.filters['diffinhours'] = diffinhours

    def render_template(self, name, **kwargs):
        template = self.jinja.get_template(
            '{}.html'.format(name),
            globals={
                'config': self.config,
            },
        )

        return template.render(**kwargs)

    def publish(self, message):
        try:
            recipient = message['recipient']
            subject = message['subject']
            sender = message.get('sender', self.config['MAIL_DEFAULT_SENDER'])
            template = message.get('template', 'basic')
            data = message['data']
        except KeyError as e:
            raise InsuficientInformation('Needed key {}'.format(str(e)))

        msg = EmailMessage()

        try:
            msg.set_content(self.render_template(template, **data))
        except TemplateNotFound:
            raise MediumError('Could not load jinja template: {}'.format(
                template
            ))

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        if self.config['MAIL_USE_SSL']:
            host = smtplib.SMTP_SSL(
                self.config['MAIL_SERVER'],
                self.config['MAIL_PORT'],
            )
        else:
            host = smtplib.SMTP(
                self.config['MAIL_SERVER'],
                self.config['MAIL_PORT'],
            )

        host.set_debuglevel(1)

        if self.config['MAIL_USE_TLS']:
            host.starttls()

        if self.config['MAIL_USERNAME'] and self.config['MAIL_PASSWORD']:
            host.login(
                self.config['MAIL_USERNAME'],
                self.config['MAIL_PASSWORD'],
            )

        host.send_message(msg)
        host.quit()

        LOGGER.info('Email sent to {}'.format(recipient))
