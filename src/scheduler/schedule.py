import logging
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

import aioschedule

from aiogram import Bot
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.client.session.aiohttp import AiohttpSession

from auth.db import get_db
from config.settings import API_TOKEN, Callbacks
from auth.repository import UserRepository


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TIME = '14:30'
DAY = 14


async def send_message(user, message):
    async with AiohttpSession() as session:
        operator = Bot(API_TOKEN, session=session)
        yes_button = InlineKeyboardButton(text="Да", callback_data=Callbacks.SEND.value)
        keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[[yes_button]])
        await operator.send_message(user.tg_id, message, reply_markup=keyboard_inline)


async def ask_question(message):
    if datetime.now().day != DAY:
        return

    async with asynccontextmanager(get_db)() as db:
        repo = UserRepository(db)
        async for user in repo.iterate_all():
            send_message(user, message)


aioschedule.every().day.at(TIME).do(ask_question, message='Готовы отправить показания?')


async def main():
    log.info('Start scheduler')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
