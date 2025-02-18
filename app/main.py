import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from decouple import config

API_TOKEN = config('API_TOKEN')

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.reply("Hello! I am your bot.")


@dp.message(Command(commands=['email']))
async def change_email_address(message: Message, event_from_user):
    log.info(event_from_user)
    email = message.text.strip('/email')
    await message.answer(f"New email: {email}")


@dp.message(Command(commands=[':']))
async def send_data(message: Message):
    datum = message.text.strip('/:')
    await message.answer(f"Data sent {datum}")


async def main():
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
