import asyncio
import logging
import base64
from contextlib import asynccontextmanager
from datetime import datetime

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import UserCreds, ClientCreds

from aiogram import Bot, Dispatcher, F

from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from decouple import config

from auth.repository import UserRepository
from auth.utils import get_authorize_url, CLIENT_CREDS

from auth.db import get_db

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

API_TOKEN = config('API_TOKEN')

dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: Message):
    auth_button = InlineKeyboardButton(text="Авторизация", url=get_authorize_url(message.from_user.id))
    keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[[auth_button]])
    await message.answer(
        'Подключаем Gmail',
        reply_markup=keyboard_inline,
    )


class Form(StatesGroup):
    data = State()


@dp.message(Command(commands=['send']))
async def send(message: Message, state: FSMContext):
    await state.set_state(Form.data)
    await message.answer(
        "Введите показания счетчика.",
        reply_markup=ReplyKeyboardRemove(),
    )


def make_email_message(from_: str, to: str, subject: str) -> dict:
    data = {
        "From": from_,
        "To": to,
        "Subject": subject,
    }
    msg = "\n".join([f"{k}: {v}" for k, v in data.items()])

    log.info(msg)
    return {
        'raw': base64.urlsafe_b64encode(msg.encode('utf-8')).decode('utf-8')
    }

async def send_data(message: Message):
    client_creds = ClientCreds(
        client_id=CLIENT_CREDS['client_id'],
        client_secret=CLIENT_CREDS['client_secret'],
        scopes=CLIENT_CREDS['scopes'],
    )

    async with asynccontextmanager(get_db)() as db:
        repo = UserRepository(db)
        user = await repo.get(message.from_user.id)

        log.info('User: %s', user.tg_id)

        user_creds = UserCreds(
            access_token=user.access_token,
            refresh_token=user.refresh_token,
            expires_at=user.expires_at,
        )

        async with Aiogoogle(user_creds=user_creds, client_creds=client_creds) as google:
            if google.oauth2.is_expired(creds=user_creds):
                refreshed, user_creds = await google.oauth2.refresh(user_creds=user_creds)
                if refreshed:
                    await repo.update(
                        user.tg_id,
                        access_token=user_creds.access_token,
                        refresh_token=user_creds.refresh_token,
                        expires_at=datetime.fromisoformat(user_creds['expires_at']),
                    )

            gmail = await google.discover('gmail', 'v1',)

            msg = make_email_message(
                from_=user.email_from,
                to=user.email_to,
                subject=f'{user.account_number} {message.text}',
            )

            response = await google.as_user(
                gmail.users.messages.send(userId='me', json=msg),
                user_creds=user_creds,
            )
            await message.answer(f"Data sent: {response}")


@dp.message(Form.data)
async def process_name(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await message.answer(
            f"Отправляю показания: {message.text}",
        )
        await send_data(message)
        await state.clear()
        await message.answer("Показания отправлены.")
    else:
        await message.answer("Введите число.")


@dp.callback_query(F.data =='send')
async def callback_send(callback: CallbackQuery, state: FSMContext):
    log.info('Callback: %s', callback)
    await state.set_state(Form.data)
    await callback.message.answer(
        "Введите показания счетчика.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def main():
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
