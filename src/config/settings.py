from decouple import config


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

ACCOUNT_NUMBER = config('ACCOUNT_NUMBER', default='1234567890')
