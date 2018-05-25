import logging

WORKERS = 2

# Rabbitmq
RABBIT_HOST = 'localhost'
RABBIT_NOTIFY_EXCHANGE = 'charpe_notify'
RABBIT_CONSUMER_TAG = 'charpe_notifier_consumer_1'
RABBIT_NO_ACK = True
RABBIT_QUEUE = 'charpe_queue'

# Log configuration
LOG_LEVEL = logging.INFO

# Time settings
TIMEZONE = 'UTC'

# Which available mediums we have
MEDIUMS = ['email', 'telegram']

# Needed to send mails
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'charpe@example.com'
MAIL_SUPPRESS_SEND = False

# For template rendering
URL_PROTOCOL = 'https'
URL_SUBDOMAIN = 'com'

# For the telegram handler
TELEGRAM_BOT_KEY = '<bot key>'
