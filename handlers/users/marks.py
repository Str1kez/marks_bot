import datetime as dt
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from filters import IsGroup
from keyboards.inline import marks, callback_marks
from loader import dp, session
from utils import get_marks, pretty_diary, get_table
from utils.misc import rate_limit


# Эхо хендлер, куда летят команды с оценками в группе
@rate_limit(10)
@dp.message_handler(IsGroup(), Command('marks'))
async def bot_echo(message: types.Message):
    await message.answer('Выберите:\n', reply_markup=marks)


# Эхо хендлер, куда летят команды с оценками в личке
@rate_limit(2)
@dp.message_handler(Command('marks'))
async def bot_echo(message: types.Message):
    await message.answer('Выберите:\n', reply_markup=marks)


@dp.callback_query_handler(callback_marks.filter(day='yesterday'))
async def get_yesterday_mark(call: CallbackQuery):
    yesterday = dt.date.today() - dt.timedelta(days=1)
    answer = f"<b>Успехи за {yesterday.strftime('%d/%m/%y')}:</b>\n{pretty_diary(get_marks(yesterday, session))}"
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(answer)


@dp.callback_query_handler(callback_marks.filter(day='now'))
async def get_now_mark(call: CallbackQuery):
    now = dt.date.today()
    answer = f"<b>Успехи за {now.strftime('%d/%m/%y')}:</b>\n{pretty_diary(get_marks(now, session))}"
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(answer)


@dp.callback_query_handler(callback_marks.filter(type='table'))
async def get_marks_table(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(get_table(session))
