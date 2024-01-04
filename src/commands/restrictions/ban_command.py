from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.utils import utils, filters

router = Router()


@router.message(Command('ban'), filters.AdminFilter())
async def command_ban(message: Message) -> Message | bool | None:
    msg = message.text.split(' ')
    if message.reply_to_message:
        if await utils.is_admin(message.reply_to_message.from_user.id, message):
            return await message.reply('Этого пользователя забанить нельзя.')

        if message.reply_to_message.from_user.id == 136817688 and message.reply_to_message.sender_chat:
            return await message.chat.ban_sender_chat(message.reply_to_message.sender_chat.id)

        target_name = utils.name_format(
            message.reply_to_message.from_user.id,
            message.reply_to_message.from_user.username,
            message.reply_to_message.from_user.first_name,
            message.reply_to_message.from_user.last_name
        )
        await message.chat.ban(
            user_id=message.reply_to_message.from_user.id,
            until_date=utils.get_restriction_time(msg[1])
        )
        return await message.answer(f'Пользователь {target_name} заблокирован.')

    if len(msg) < 2 or not msg[1].isdigit():
        return await message.reply(
            'Для блокировки пользователя необходимо ответить на сообщение или написать Telegram ID через пробел.'
        )

    if await utils.is_admin(int(msg[1]), message):
        return await message.reply('Этого пользователя забанить нельзя.')

    try:
        await message.chat.ban(
            user_id=int(msg[1]),
            until_date=utils.get_restriction_time(msg[1])
        )
        return await message.answer(f'Пользователь <code>{msg[1]}</code> заблокирован.')
    except Exception as e:
        await message.reply(f'Не удалось заблокировать пользователя.\n\nОшибка: <code>{e}</code>')
