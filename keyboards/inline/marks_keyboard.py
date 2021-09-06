from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .marks_callback import callback_marks


marks = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton('Вчера', callback_data=callback_marks.new(day='yesterday')),
        InlineKeyboardButton('Сегодня', callback_data=callback_marks.new(day='now'))
    ]
])
