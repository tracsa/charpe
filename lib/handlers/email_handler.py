from . import BaseHandler
from .. import mail
from ..i18n import _
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os


class EmailHandler(BaseHandler):

    def initialize(self):
        self.jinja = Environment(
            loader = FileSystemLoader(os.path.join(os.path.dirname(__name__), 'templates')),
            autoescape = select_autoescape(['html']),
        )
        self.mail = mail.Mail(self.config)

    def render_template(self, template, **kwargs):
        template = self.jinja.get_template(template)

        return template.render(**kwargs)

    def publish(self, message):
        def build_recipient(user):
            return '{} {} <{}>'.format(
                user['name'],
                user['last_name'] if user['last_name'] else '',
                user['email'],
            )

        msg = mail.Message(
            subject = _.get(message['event'], ''),
            bcc = list(map(
                build_recipient,
                message['users']
            ))
        )

        msg.html = self.render_template('{}.html'.format(message['event']),
            event          = _.get(message['event'], ''),
            # org_name       = message['org'],
            # static_map_url = static_map_url,
            # device_name    = device_name,
            # geofence_name  = geofence_name,
            # device_href    = device_href,
            # geofence_href  = geofence_href,
        )

        self.mail.send(msg)