from . import BaseHandler
import logging


class LogHandler(BaseHandler):

    def initialize(self):
        from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

        self.metadata = MetaData()
        self.engine = create_engine(self.config['LOG_DATABASE_URI'])

        self.log_table = Table('log', MetaData())

    def publish(self, message):
        logging.debug('Wil write message to log')
