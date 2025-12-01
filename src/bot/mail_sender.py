from contextlib import asynccontextmanager
import logging
import base64


from api.dependencies import get_db_session
from repositories.user import UserRepository


log = logging.getLogger(__name__)


def make_email_message(from_: str, to: str, subject: str) -> dict[str, str]:
    data = {
        "From": from_,
        "To": to,
        "Subject": subject,
    }
    msg = "\n".join([f"{k}: {v}" for k, v in data.items()])

    return {"raw": base64.urlsafe_b64encode(msg.encode("utf-8")).decode("utf-8")}


async def send_mail(tg_id: int, data: str) -> None:
    async with asynccontextmanager(get_db_session)() as db:
        repo = UserRepository(db)
        user = await repo.get_by_telegram_id(telegram_id=tg_id)
        log.debug("User: %s", tg_id)

        if user is None:
            log.error("User not found: %s", tg_id)
            return

        log.info("Fake email")

        # user_creds = UserCreds(
        #     access_token=user.access_token,
        #     refresh_token=user.refresh_token,
        #     expires_at=user.expires_at,
        # )

        # async with aiogoogle_client as google:
        #     if google.oauth2.is_expired(creds=user_creds):
        #         refreshed, user_creds = await google.oauth2.refresh(user_creds=user_creds)
        #         google.user_creds = user_creds
        #         if refreshed:
        #             await repo.update(
        #                 user.tg_id,
        #                 access_token=user_creds.access_token,
        #                 refresh_token=user_creds.refresh_token,
        #                 expires_at=datetime.fromisoformat(user_creds['expires_at']),
        #             )

        #     gmail = await google.discover('gmail', 'v1',)

        #     msg = make_email_message(
        #         from_=user.email_from,
        #         to=user.email_to,
        #         subject=f'{user.account_number} {data}',
        #     )

        #     response = await google.as_user(
        #         gmail.users.messages.send(userId='me', json=msg),
        #     )
        #     log.info('Response: %s', response)


class MailSender:
    def __init__(self, message) -> None:
        self.message = message

    def send(self, from_: str, to: str, subject: str) -> None:
        pass
