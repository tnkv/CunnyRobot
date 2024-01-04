from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.utils import utils, filters

router = Router()


@router.message(Command('ban'), filters.AdminFilter())
async def command_ban(message: Message) -> Message | None:
    if message.reply_to_message:
        if await utils.is_admin(message.reply_to_message.from_user.id, message):
            return await message.reply('Этого пользователя забанить нельзя.')

        if message.reply_to_message.from_user.id == 136817688 and message.reply_to_message.sender_chat:
            await message.chat.ban_sender_chat(message.reply_to_message.sender_chat.id)
            return

        await message.chat.ban(user_id=message.reply_to_message.from_user.id)
        return

    msg = message.text.split(' ')
    if len(msg) >= 2 and msg[1].isdigit():
        if await utils.is_admin(int(msg[1]), message):
            return await message.reply('Этого пользователя забанить нельзя.')

        try:
            await message.chat.ban(user_id=int(msg[1]))

        except Exception:
            await message.reply('Не удалось заблокировать пользователя.')
        return
    await message.reply(
        'Для блокировки пользователя необходимо ответить на сообщение или написать Telegram ID через пробел.')
