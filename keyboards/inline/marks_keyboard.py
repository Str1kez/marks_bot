from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .marks_callback import callback_marks


marks = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton('Вчера', callback_data=callback_marks.new(day='yesterday', type='diary')),
        InlineKeyboardButton('Сегодня', callback_data=callback_marks.new(day='now', type='diary'))
    ],
    [
        InlineKeyboardButton('Табель', callback_data='get:quarter:table')
    ]
])

more_marks = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton('Больше', callback_data='get:quarter:more'),
        InlineKeyboardButton('Закрыть', callback_data='get:quarter:close')
    ]
])
