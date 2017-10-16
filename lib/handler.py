from .logger import log
from .handlers.log_handler import LogHandler

handlers = {
    'log': LogHandler(),
}

def handler(data):
    if data['type'] != 'pmessage':
        return

    channel, msg = data['channel'].decode('utf8'), data['data'].decode('utf8')

    handlers['log'].publish(msg)
