from aiogram import types

from app.filters import IsGroup
from app.loader import dp


@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def greetings_to_new_user(message: types.Message):
    new_members = (member.get_mention() for member in message.new_chat_members)
    await message.answer(f'Приветствуем {", ".join(new_members)}!')


@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def goodbye_to_user(message: types.Message):
    if message.from_user.id == message.left_chat_member.id:
        await message.answer(f"Возвращайся, {message.from_user.get_mention()}")
    else:
        await message.answer(f"{message.from_user.get_mention()} выгнал {message.left_chat_member.get_mention()}")
