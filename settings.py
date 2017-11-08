import logging

# Redis connection
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Process management
WORKERS = 4
SLEEP_TIME = 0.001

# Channels
CHANNEL_PATTERN = '*:*:*'

# Do not log this events as they happen too often.
# Events are loggued automatically
DO_NOT_LOG = [
    'device-update',
]

# Postgres connection params
POSTGRES_DB = 'fleety'
POSTGRES_USER = None
POSTGRES_PASSWORD = None
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432

# Log configuration
LOG_LEVEL = logging.INFO

# Time settings
TIMEZONE = 'UTC'

# Needed to send mails
MAIL_SERVER             = 'smtp.mailgun.org'
MAIL_PORT               = '587'
MAIL_USE_TLS            = True
MAIL_USE_SSL            = False
MAIL_USERNAME           = 'devel@mg.getfleety.com'
MAIL_PASSWORD           = ''
MAIL_DEFAULT_SENDER     = '"Fleety Devel" <devel@mg.getfleety.com>'

# For template rendering
URL_PROTOCOL = 'https'
URL_SUBDOMAIN = 'com'

# For google static maps
GOOGLE_API_STATIC_MAPS_KEY = ''
