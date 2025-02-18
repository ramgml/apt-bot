import base64
from aiogoogle import Aiogoogle

from config.settings import GOOGLE_CLIENT_CREDS, APP_SECRET


aiogoogle_client = Aiogoogle(client_creds=GOOGLE_CLIENT_CREDS)


def make_state(tg_id: int) -> str:
    input_string = f'{str(tg_id)}.{APP_SECRET}'
    encoded_bytes = base64.b64encode(input_string.encode("utf-8"))
    encoded_str = encoded_bytes.decode()
    return encoded_str

def get_tg_id_from_state(state: str) -> int:
    if state := base64.b64decode(state).decode().split('.'):
        return int(state[0])


def get_authorize_url(tg_id: int) -> str:
    return aiogoogle_client.oauth2.authorization_url(
        state=make_state(tg_id),
        access_type="offline",
        include_granted_scopes=True,
        prompt="consent",
    )
