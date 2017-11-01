from . import BaseHandler
from .. import mail
from ..i18n import _
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import logging


class EmailHandler(BaseHandler):

    def initialize(self):
        self.jinja = Environment(
            loader = FileSystemLoader(os.path.join(os.path.dirname(__name__), 'templates')),
            autoescape = select_autoescape(['html']),
        )
        self.mail = mail.Mail(self.config)

    def render_template(self, name, **kwargs):
        template = self.jinja.select_template([name])

        return template.render(**kwargs)

    def publish(self, message):
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

        msg = mail.Message(
            subject = _.get(message['event'], ''),
            bcc = recipients,
        )

        msg.html = self.render_template('{}.html'.format(message['event']),
            event          = _.get(message['event'], ''),
        )

        self.mail.send(msg)

        logging.debug('Email sent')
