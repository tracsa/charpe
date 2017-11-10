from datetime import datetime
from pytz import timezone
import pytz

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
ES_MX_FORMAT = '%d/%m/%y %H:%M'
tz = timezone('America/Mexico_City')

def datetimeformat(date):
    utc_dt = pytz.utc.localize(datetime.strptime(date, ISO_FORMAT))

    return utc_dt.astimezone(tz).strftime(ES_MX_FORMAT)

def diffinhours(date, otherdate):
    hours = (datetime.strptime(date, ISO_FORMAT) - datetime.strptime(otherdate, ISO_FORMAT)).seconds // 3600
    return '{}h'.format(hours)
