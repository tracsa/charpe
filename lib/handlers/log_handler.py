from . import BaseHandler
import logging
import psycopg2


class LogHandler(BaseHandler):

    def publish(self, message):
        conn = psycopg2.connect(
            dbname   = self.config['POSTGRES_DB'],
            user     = self.config['POSTGRES_USER'],
            password = self.config['POSTGRES_PASSWORD'],
            host     = self.config['POSTGRES_HOST'],
            port     = self.config['POSTGRES_PORT'],
        )
        cur = conn.cursor()

        cur.execute("INSERT INTO log (col1, col2) VALUES (%s, %s)", (1, 2))
        conn.commit()

        cur.close()
        conn.close()

        logging.debug('Log entry created')
