from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.utils import utils, filters

router = Router()


@router.message(Command('ban'), filters.AdminFilter())
async def command_ban(message: Message, i18n: I18nContext) -> Message | bool | None:
    if message.reply_to_message:
        if await utils.is_admin(message.reply_to_message.from_user.id, message):
            return await message.reply(i18n.get('command-ban-immune_user'))

        if message.reply_to_message.from_user.id == 136817688 and message.reply_to_message.sender_chat:
            return await message.chat.ban_sender_chat(message.reply_to_message.sender_chat.id)

        target_name = utils.NameFormat(message.reply_to_message.from_user)
        await message.chat.ban(user_id=message.reply_to_message.from_user.id)
        return await message.answer(i18n.get('command-ban-ban', name=target_name.get()))

    msg = message.text.split(' ')
    if len(msg) < 2 or not msg[1].isdigit():
        return await message.reply(i18n.get('command-ban-need_telegram_id'))
    try:
        if await utils.is_admin(int(msg[1]), message):
            return await message.reply(i18n.get('command-ban-immune_user'))

        await message.chat.ban(user_id=int(msg[1]))
        return await message.answer(i18n.get('command-ban-ban_id', user=msg[1]))
    except Exception as e:
        await message.reply(i18n.get('common-errors-cant_ban', exception=str(e)))
