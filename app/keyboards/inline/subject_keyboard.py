from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards.inline import callback_subject


def create_subject_keyboard(subjects: list):
    keyboard = []
    for subj in subjects:
        keyboard.append([InlineKeyboardButton(subj, callback_data=callback_subject.new(subj=subj[:31]))])
    keyboard.append([InlineKeyboardButton("❌", callback_data=callback_subject.new(subj="close"))])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
