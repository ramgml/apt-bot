from aiogoogle import Aiogoogle

from config.settings import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    AUTH_HOST,
)


CLIENT_CREDS = {
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

aiogoogle_client = Aiogoogle()


def get_authorize_url(tg_id: int):
    uri = Aiogoogle().oauth2.authorization_url(
        client_creds=CLIENT_CREDS,
        state=tg_id,
        access_type="offline",
        include_granted_scopes=True,
        prompt="consent",
    )
    return uri
