from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import callback_subject, callback_marks


def create_subject_keyboard(subjects: list):
    keyboard = []
    for subj in subjects:
        keyboard.append([InlineKeyboardButton(subj, callback_data=callback_subject.new(subj=subj))])
    keyboard.append([InlineKeyboardButton('❌', callback_data=callback_subject.new(subj='close'))])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
