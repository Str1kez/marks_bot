import datetime as dt
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data.config import YESTERDAY
from keyboards.inline import marks, callback_marks
from loader import dp
from utils import get_marks


# Эхо хендлер, куда летят команды с оценками
@dp.message_handler(Command('marks'))
async def bot_echo(message: types.Message):
    await message.answer('Выберите день:\n', reply_markup=marks)


@dp.callback_query_handler(callback_marks.filter(day=str(YESTERDAY)))
async def get_yesterday_mark(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(get_marks(YESTERDAY))
