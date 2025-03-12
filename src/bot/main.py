import asyncio
import logging

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

from config.settings import API_TOKEN, Callbacks
from bot.mail_sender import send_mail

from auth.utils import get_authorize_url


log = logging.getLogger(__name__)


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
async def wait_user_data(message: Message, state: FSMContext):
    await state.set_state(Form.data)
    await message.answer(
        "Введите показания счетчика.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(Form.data)
async def process_meter_readings(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await message.answer(
            f"Отправляю показания: {message.text}",
        )
        await send_mail(message.from_user.id, message.text)
        await state.clear()
        await message.answer("Показания отправлены.")
    else:
        await message.answer("Введите число.")


@dp.callback_query(F.data == Callbacks.SEND.value)
async def handle_send_button_click(callback: CallbackQuery, state: FSMContext) -> None:
    log.info('Callback: %s', callback)
    await state.set_state(Form.data)
    await callback.message.answer(
        "Введите показания счетчика.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def main():
    await dp.start_polling(Bot(token=API_TOKEN))


if __name__ == '__main__':
    asyncio.run(main())
