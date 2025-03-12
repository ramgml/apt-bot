from aiogoogle import Aiogoogle

from config.settings import GOOGLE_CLIENT_CREDS


aiogoogle_client = Aiogoogle(client_creds=GOOGLE_CLIENT_CREDS)


def get_authorize_url(tg_id: int):
    uri = aiogoogle_client.oauth2.authorization_url(
        state=tg_id,
        access_type="offline",
        include_granted_scopes=True,
        prompt="consent",
    )
    return uri
