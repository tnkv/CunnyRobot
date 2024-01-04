from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from src.utils import utils, filters

router = Router()


@router.message(Command(commands=['mute', 'm']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_mute(message: Message) -> Message | None:
    if await utils.is_admin(message.reply_to_message.from_user.id, message):
        return await message.reply('Этого пользователя замутить нельзя.')

    msg = message.text.split(' ')
    target_name = utils.name_format(
        message.reply_to_message.from_user.id,
        message.reply_to_message.from_user.username,
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name
    )

    if len(msg) < 2:
        await message.chat.restrict(
            user_id=message.reply_to_message.from_user.id,
            until_date=0,
            permissions=ChatPermissions(can_send_messages=False))
        return await message.answer(f'Пользователь {target_name} замучен.')

    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        until_date=utils.get_restriction_time(msg[1]),
        permissions=ChatPermissions(can_send_messages=False)
    )

    await message.answer(f'Пользователь {target_name} замучен на {msg[1]}.')
