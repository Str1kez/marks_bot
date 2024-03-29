import datetime as dt

import pytz
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.filters import IsGroup
from app.keyboards.inline import callback_marks, callback_subject, marks, more_marks
from app.keyboards.inline.subject_keyboard import create_subject_keyboard
from app.loader import dp, session
from app.utils import get_marks, get_subject, get_subjects, get_table, pretty_diary
from app.utils.misc import rate_limit


@rate_limit(10)
@dp.message_handler(IsGroup(), Command("marks"))
async def bot_echo(message: types.Message):
    """
    Эхо хендлер, куда летят команды с оценками в группе
    """
    await message.answer("Выберите:\n", reply_markup=marks, disable_notification=True)


@rate_limit(2)
@dp.message_handler(Command("marks"))
async def bot_echo(message: types.Message):
    """
    Эхо хендлер, куда летят команды с оценками в личке
    """
    await message.answer("Выберите:\n", reply_markup=marks)


@dp.callback_query_handler(callback_marks.filter(day="yesterday"))
async def get_yesterday_mark(call: CallbackQuery):
    utc = dt.datetime.utcnow()
    common_tz = pytz.timezone("UTC")
    target_tz = pytz.timezone("Europe/Moscow")
    today = common_tz.localize(utc).astimezone(target_tz).date()
    yesterday = today - dt.timedelta(days=1)
    answer = f"<b>Успехи за {yesterday.strftime('%d/%m/%y')}:</b>\n{pretty_diary(await get_marks(yesterday, session))}"
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(answer)


@dp.callback_query_handler(callback_marks.filter(day="now"))
async def get_now_mark(call: CallbackQuery):
    utc = dt.datetime.utcnow()
    common_tz = pytz.timezone("UTC")
    target_tz = pytz.timezone("Europe/Moscow")
    today = common_tz.localize(utc).astimezone(target_tz).date()
    answer = f"<b>Успехи за {today.strftime('%d/%m/%y')}:</b>\n{pretty_diary(await get_marks(today, session))}"
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(answer)


@dp.callback_query_handler(callback_marks.filter(type="table"))
async def get_marks_table(call: CallbackQuery):
    table = await get_table(session)
    await call.answer()
    await call.message.edit_text(table)
    await call.message.edit_reply_markup(reply_markup=more_marks)


@dp.callback_query_handler(callback_marks.filter(type="close"))
async def close_keyboard(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup()


@dp.callback_query_handler(callback_marks.filter(type="more"))
async def get_more_marks(call: CallbackQuery):
    subjects = get_subjects()
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer("Выберите:\n", reply_markup=create_subject_keyboard(subjects), disable_notification=True)


@dp.callback_query_handler(callback_subject.filter(subj="close"))
async def close_keyboard(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.delete()


@dp.callback_query_handler(callback_subject.filter())
async def get_list_subjects(call: CallbackQuery):
    subject = call.data.split(":")[1]
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.edit_text(get_subject(subject))
