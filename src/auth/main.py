from datetime import datetime
import logging

from fastapi import FastAPI, Depends, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ClientCreds

from auth.utils import aiogoogle_client, CLIENT_CREDS
from auth.db import get_db
from auth.repository import UserRepository


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


app = FastAPI(
    docs_url=None,
    redoc_url=None,
)


@app.get('/callback/gmail')
async def callback(db: AsyncSession = Depends(get_db), code: str | None = None, state: str | None = None):
    if code is None:
        return {"error": "No code received"}

    user_creds = await aiogoogle_client.oauth2.build_user_creds(
        grant=code,
        client_creds=CLIENT_CREDS,
    )

    expires_at = datetime.fromisoformat(user_creds['expires_at'])

    client_creds = ClientCreds(
        client_id=CLIENT_CREDS['client_id'],
        client_secret=CLIENT_CREDS['client_secret'],
        scopes=CLIENT_CREDS['scopes'],
    )

    async with Aiogoogle(user_creds=user_creds, client_creds=client_creds) as google:
        gmail = await google.discover('gmail', 'v1',)
        profile = await google.as_user(
            gmail.users.getProfile(userId="me"),
        )

    repo = UserRepository(db)

    await repo.update_or_create(
        tg_id=state,
        access_token=user_creds['access_token'],
        refresh_token=user_creds['refresh_token'],
        expires_at=expires_at,
        email_from=profile['emailAddress'],
    )
    log.info('Profile: %s', profile)

    return RedirectResponse(url='https://t.me/apt_179_bot')
