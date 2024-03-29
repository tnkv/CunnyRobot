from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, utils

router = Router()


@router.message(Command(commands=['warns', 'checkwarns']))
async def command_checkwarns(message: Message, session: AsyncSession, i18n: I18nContext):
    if not message.reply_to_message:
        warns = await database.get_warns(
            session,
            message.chat.id,
            message.from_user.id
        )
        name = utils.NameFormat(message.from_user)

        if len(warns) == 0:
            return await message.reply(text=i18n.get('command-warn-check-nowarns_self'))

        return await message.reply(display_warns(warns, i18n, name.get()))

    is_initiator_admin = await utils.is_admin(message.from_user.id, message.chat)
    if not is_initiator_admin:
        return await message.reply(text=i18n.get('common-need_admin_rights'))

    target_name = utils.NameFormat(message.reply_to_message.sender_chat or message.reply_to_message.from_user)
    warns = await database.get_warns(
        session,
        message.chat.id,
        message.reply_to_message.from_user.id
    )
    if len(warns) == 0:
        return await message.reply(text=i18n.get('command-warn-check-nowarns', name=target_name.get()))

    return await message.reply(display_warns(warns, i18n, target_name.get()))


def display_warns(warns: list, i18n: I18nContext, user: str = None):
    display = i18n.get('command-warn-display_warns_header')
    display += f' {user}:\n' if user else ':\n'
    counter = 1

    for warn in warns:
        link_to_warn = (
            f'<a href="https://t.me/c/{str(warn.TelegramChatID)[4:]}/{warn.MessageID}">'
            f'{warn.Reason if warn.Reason else i18n.get("command-warn-display-noreason")}</a>'
        )
        display += f'<b>{counter})</b> {link_to_warn}\n'
        counter += 1

    return display
