from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html.parser import HTMLParser
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound
import logging
import os
import smtplib

from charpe.mediums import BaseMedium
from charpe.template_filters import datetimeformat, diffinhours
from charpe.errors import InsuficientInformation, MediumError

LOGGER = logging.getLogger(__name__)


# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class StripTagsParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = []

    def handle_data(self, data):
        self.data.append(data)

    def get_data(self):
        return ''.join(self.data)


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

    def publish(self, message):
        try:
            recipient = message['recipient']
            subject = message['subject']
            sender = message.get('sender', self.config['MAIL_DEFAULT_SENDER'])
            template = message.get('template', 'basic.html')
            data = message['data']
        except KeyError as e:
            raise InsuficientInformation('Needed key {}'.format(str(e)))

# https://stackoverflow.com/questions/882712/sending-html-email-using-python#882770
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

# Create the body of the message (a plain-text and an HTML version).
        try:
            rendered_template = self.render_template(template, **data)

            # now we build a text-only version of the message
            stp = StripTagsParser()
            stp.feed(rendered_template)

            msg.attach(MIMEText(rendered_template, 'html'))
            msg.attach(MIMEText(stp.get_data(), 'plain'))
        except TemplateNotFound:
            raise MediumError('Could not load jinja template: {}'.format(
                template
            ))

        # now deal with SMTP
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

        host.set_debuglevel(self.config['LOG_LEVEL'] == logging.DEBUG)

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
