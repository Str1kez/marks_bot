import datetime as dt
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline import marks, callback_marks
from loader import dp
from utils import get_marks, pretty_output


# Эхо хендлер, куда летят команды с оценками
from utils.misc import rate_limit


@rate_limit(10)
@dp.message_handler(Command('marks'))
async def bot_echo(message: types.Message):
    await message.answer('Выберите день:\n', reply_markup=marks)


@dp.callback_query_handler(callback_marks.filter(day='yesterday'))
async def get_yesterday_mark(call: CallbackQuery):
    yesterday = dt.date.today() - dt.timedelta(days=5)
    answer = f"<b>Успехи за {yesterday.strftime('%d/%m/%y')}:</b>\n{pretty_output(get_marks(yesterday))}"
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(answer)


@dp.callback_query_handler(callback_marks.filter(day='now'))
async def get_now_mark(call: CallbackQuery):
    now = dt.date.today()
    answer = f"<b>Успехи за {now.strftime('%d/%m/%y')}:</b>\n{pretty_output(get_marks(now))}"
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(answer)
