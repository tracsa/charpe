from . import BaseHandler
import logging
import psycopg2
import json
from datetime import datetime


class LogHandler(BaseHandler):

    def publish(self, message):
        channel = message['channel']
        subdomain = channel.split(':')[0]
        event = message['data']['event']
        data = json.dumps(message['data']['data'])
        created_at = datetime.now()

        conn = psycopg2.connect(
            dbname   = self.config['POSTGRES_DB'],
            user     = self.config['POSTGRES_USER'],
            password = self.config['POSTGRES_PASSWORD'],
            host     = self.config['POSTGRES_HOST'],
            port     = self.config['POSTGRES_PORT'],
        )
        cur = conn.cursor()

        cur.execute("INSERT INTO log (org_subdomain, channel, event, data, created_at) VALUES (%s, %s, %s, %s, %s)", (subdomain, channel, event, data, created_at))
        conn.commit()

        cur.close()
        conn.close()

        logging.debug('Log entry created')
