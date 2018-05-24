import logging

WORKERS = 2

# Rabbitmq
RABBIT_HOST = 'localhost'
RABBIT_NOTIFY_EXCHANGE = 'cacahuate_notify'
RABBIT_CONSUMER_TAG = 'cacahuate_notifier_consumer_1'
RABBIT_NO_ACK = True

# Log configuration
LOG_LEVEL = logging.INFO

# Time settings
TIMEZONE = 'UTC'

# Needed to send mails
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'procesos@tracsa.com.mx'
MAIL_SUPPRESS_SEND = False

# For template rendering
URL_PROTOCOL = 'https'
URL_SUBDOMAIN = 'com'

# For the telegram handler
TELEGRAM_BOT_KEY = '<bot key>'
