from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, utils

router = Router()


@router.message(Command(commands=['warns', 'checkwarns']))
async def command_checkwarns(message: Message, session: AsyncSession):
    if not message.reply_to_message:
        warns = await database.get_warns(
            session,
            message.chat.id,
            message.from_user.id
        )
        name = utils.name_format(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )

        if len(warns) == 0:
            return await message.reply('У вас нет предупреждений.')
        return await message.reply(display_warns(warns, name))

    is_initiator_admin = await utils.is_admin(message.from_user.id, message)
    if not is_initiator_admin:
        await message.reply('Ты не админ.')
        return

    name = utils.name_format(
        message.reply_to_message.from_user.id,
        message.reply_to_message.from_user.username,
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name
    )
    warns = await database.get_warns(
        session,
        message.chat.id,
        message.reply_to_message.from_user.id
    )
    if len(warns) == 0:
        return await message.reply(f'У пользователя {name} нет предупреждений.')
    return await message.reply(display_warns(warns, name))


def display_warns(warns: list, user: str = None):
    display = f'Предупреждения полученные пользователем'
    display += f' {user}:\n' if user else ':\n'
    counter = 1
    for warn in warns:
        display += f'<b>{counter})</b> <a href="https://t.me/c/{str(warn.TelegramChatID)[4:]}/{warn.MessageID}">{warn.Reason if warn.Reason else "Без причины."}</a>\n'
        counter += 1

    return display
