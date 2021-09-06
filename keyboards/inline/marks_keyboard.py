import datetime as dt

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import YESTERDAY, NOW
from .marks_callback import callback_marks


marks = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton('Вчера', callback_data=callback_marks.new(day=YESTERDAY.date())),
        InlineKeyboardButton('Сегодня', callback_data=callback_marks.new(day=NOW.date()))
    ]
])
