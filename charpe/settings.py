import logging


WORKERS = int(os.getenv(
    'CHARPE_WORKERS',
    '2',
))

# Rabbitmq
RABBIT_HOST = os.getenv(
    'CHARPE_RABBITMQ_HOST',
    'localhost',
)
RABBIT_PORT = int(os.getenv(
    'CHARPE_RABBITMQ_PORT',
    '5672',
)
RABBIT_USER = os.getenv(
    'CHARPE_RABBITMQ_USER',
    'guest',
)
RABBIT_PASS = os.getenv(
    'CHARPE_RABBITMQ_PASS',
    'guest',
)
RABBIT_NOTIFY_EXCHANGE = os.getenv(
    'CHARPE_RABBITMQ_NOTIFY_EXCHANGE',
    'charpe_notify',
)
RABBIT_CONSUMER_TAG = os.getenv(
    'CHARPE_RABBITMQ_CONSUMER_TAG',
    'charpe_notifier_consumer_1',
)
RABBIT_NO_ACK = os.getenv(
    'CHARPE_RABBITMQ_NO_ACK',
    'True',
) == 'True'
RABBIT_QUEUE = os.getenv(
    'CHARPE_RABBITMQ_QUEUE',
    'charpe_queue',
)

# Log configuration
LOG_LEVEL = logging.INFO

# Time settings
TIMEZONE = 'UTC'

# Which available mediums we have
MEDIUMS = [
    'email',
    'telegram',
]

# Needed to send mails
MAIL_SERVER = os.getenv(
    'CHARPE_MAIL_SERVER',
    'smtp.mailgun.org',
)
MAIL_PORT = os.getenv(
    'CHARPE_MAIL_PORT',
    '587',
)
MAIL_USE_TLS = os.getenv(
    'CHARPE_MAIL_USE_TLS',
    'True',
) == 'True'
MAIL_USE_SSL = os.getenv(
    'CHARPE_MAIL_USE_SSL',
    'False',
) == 'True'
MAIL_USERNAME = os.getenv(
    'CHARPE_MAIL_USERNAME',
    '',
)
MAIL_PASSWORD = os.getenv(
    'CHARPE_MAIL_PASSWORD',
    '',
)
MAIL_DEFAULT_SENDER = os.getenv(
    'CHARPE_MAIL_DEFAULT_SENDER',
    'charpe@example.com',
)
MAIL_SUPPRESS_SEND = os.getenv(
    'CHARPE_MAIL_SUPPRESS_SEND',
    'False',
) == 'True'

# For template rendering
URL_PROTOCOL = 'https'
URL_SUBDOMAIN = 'com'

# For the telegram handler
TELEGRAM_BOT_KEY = os.getenv(
    'CHARPE_TELEGRAM_BOT_KEY',
    '<bot key>',
)

# Override or add telegram teplates
TELEGRAM_TEMPLATES = {}
# Override or add email templates
EMAIL_TEMPLATES = os.getenv(
    'CHARPE_EMAIL_TEMPLATES',
    '/var/templates/',
)
