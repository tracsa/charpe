from . import BaseHandler
import logging
import psycopg2
import json


class LogHandler(BaseHandler):

    def publish(self, message):
        if message['type'] != 'pmessage':
            return

        data = message['data']

        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            logging.warning('Couldn\'t decode event\'s JSON data:')
            logging.warning(message)
            return

        if 'event' not in data:
            logging.warning('Received non-event message')
            logging.warning(message)
            return

        if 'data' not in data:
            logging.warning('Received event without data')
            logging.warning(message)
            return

        channel = message['channel'].decode('utf8')
        subdomain = channel.split(':')[0]
        event = data['event']
        data = json.dumps(data['data'])

        conn = psycopg2.connect(
            dbname   = self.config['POSTGRES_DB'],
            user     = self.config['POSTGRES_USER'],
            password = self.config['POSTGRES_PASSWORD'],
            host     = self.config['POSTGRES_HOST'],
            port     = self.config['POSTGRES_PORT'],
        )
        cur = conn.cursor()

        cur.execute("INSERT INTO log (org_subdomain, channel, event, data) VALUES (%s, %s, %s, %s)", (subdomain, channel, event, data))
        conn.commit()

        cur.close()
        conn.close()

        logging.debug('Log entry created')
