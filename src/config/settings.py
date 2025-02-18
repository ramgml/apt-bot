from enum import Enum
import logging.config

from decouple import config

APP_SECRET=config('APP_SECRET', default='secret')
API_TOKEN = config('API_TOKEN', default='token')

POSTGRES_USER = config('POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', default='postgres')
POSTGRES_DB = config('POSTGRES_DB', default='postgres')
POSTGRES_HOST = config('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = config('POSTGRES_PORT', default='5432')

AUTH_PORT = config('AUTH_PORT', default='8000')
AUTH_HOST = config('AUTH_HOST', default='http://localhost')

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', default='client_id')
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET', default='client_secret')
GOOGLE_CLIENT_CREDS = {
    'client_id': GOOGLE_CLIENT_ID,
    'client_secret': GOOGLE_CLIENT_SECRET,
    'scopes': [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ],
    'redirect_uri': f'{AUTH_HOST}/callback/gmail',
}

ACCOUNT_NUMBER = config('ACCOUNT_NUMBER', default='1234567890')

LOG_LEVEL = config('LOG_LEVEL', default='INFO')
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] - %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },

    'loggers': {
        'apt_bot': {
            'handlers': ['stream_handler'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}
logging.config.dictConfig(LOGGING_CONFIG)


BOT_URL = config('BOT_URL', default='https://t.me/your_bot_name')

# Callbacks
class Callbacks(Enum):
    SEND = 'send'
