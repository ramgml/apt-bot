from datetime import datetime
import logging

from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from auth.db import get_db
from auth.repository import UserRepository
from auth.utils import aiogoogle_client, get_tg_id_from_state

from config.settings import BOT_URL


log = logging.getLogger(__name__)


app = FastAPI(
    docs_url=None,
    redoc_url=None,
)


@app.get('/callback/gmail')
async def callback(db: AsyncSession = Depends(get_db), code: str | None = None, state: str | None = None):
    """Callback from Google OAuth2."""
    if code is None:
        return {"error": "No code received"}
    if (tg_id := get_tg_id_from_state(state)) is None:
        return {"error": "Invalid state"}

    async with aiogoogle_client as google:
        google.user_creds = await google.oauth2.build_user_creds(grant=code)
        gmail = await google.discover('gmail', 'v1')
        request = gmail.users.getProfile(userId="me")
        profile = await google.as_user(request)
        log.info('Profile: %s', profile)

        await UserRepository(db).update_or_create(
            tg_id=tg_id,
            access_token=google.user_creds['access_token'],
            refresh_token=google.user_creds['refresh_token'],
            expires_at=datetime.fromisoformat(google.user_creds['expires_at']),
            email_from=profile['emailAddress'],
        )

    return RedirectResponse(url=BOT_URL)
