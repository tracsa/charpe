from jinja2 import Environment, DictLoader
import logging
import requests

from charpe.mediums import BaseMedium

LOGGER = logging.getLogger(__name__)


class TelegramHandler(BaseMedium):

    def initialize(self):
        self.jinja = Environment(
            loader=DictLoader({
                'basic': '{{ content }}',
                'server-error':
                    '⚠️ #{{ service_name }} ⚠️\n```{{ traceback }}```',
            }),
        )

    def publish(self, message):
        try:
            template = message.get('template', 'basic')
            chat_id = message['chat_id']
            data = message['data']
        except KeyError as e:
            raise InsuficientInformation('Needed key {}'.format(str(e)))

        LOGGER.debug('Using template {}'.format(template))

        try:
            rendered_template = self.render_template(template, **data)
        except TemplateNotFound:
            raise MediumError('Could not load jinja template: {}'.format(
                template
            ))

        LOGGER.debug('Content: {}'.format(rendered_template))

        res = requests.post(
            'https://api.telegram.org/bot{}/sendMessage'.format(
                self.config['TELEGRAM_BOT_KEY']
            ), data={
                'chat_id': chat_id,
                'text': rendered_template,
                'parse_mode': 'Markdown',
            })

        LOGGER.info('Sent message to telegram chat {}. Response: {}'.format(
            chat_id,
            res.status_code,
        ))

        LOGGER.debug(res.text)
