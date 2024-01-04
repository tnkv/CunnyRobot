from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, utils, ChatInfo, filters

router = Router()


@router.message(Command(commands=['give_immune', 'give_immunity']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_give_immune(message: Message, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, message.chat.id))
    name = utils.name_format(message.reply_to_message.from_user.id,
                             message.reply_to_message.from_user.username,
                             message.reply_to_message.from_user.first_name,
                             message.reply_to_message.from_user.last_name)

    if not chat_info.add_immune(message.reply_to_message.from_user.id):
        await message.reply(f'У пользователя {name} уже был иммунитет от трибунала.\n\n'
                            'Проверить наличие можно через /check\n'
                            'Забрать иммунитет можно через /revoke_immune')
        return

    await database.set_chat_info(session, chat_info.export())
    await message.reply(f'Пользователю {name} был выдан иммунитет от трибунала.\n\n'
                        'Проверить наличие можно через /check\n'
                        'Забрать иммунитет можно через /revoke_immune')


# Отмена иммунитета
@router.message(Command(commands=['revoke_immune', 'revoke_immunity']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_revoke_immune(message: Message, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, message.chat.id))
    name = utils.name_format(message.reply_to_message.from_user.id,
                             message.reply_to_message.from_user.username,
                             message.reply_to_message.from_user.first_name,
                             message.reply_to_message.from_user.last_name)

    if not chat_info.revoke_immune(message.reply_to_message.from_user.id):
        await message.reply(f'У пользователя {name} отсутствовал иммунитет к трибуналу.\n\n'
                            'Проверить наличие можно через /check\n'
                            'Выдать иммунитет можно через /give_immune')
        return

    await database.set_chat_info(session, chat_info.export())
    await message.reply(f'У пользователя {name} был отобран иммунитет от трибунала.\n\n'
                        'Проверить наличие можно через /check\n'
                        'Выдать иммунитет можно через /give_immune')


# Проверка наличия иммунитета
@router.message(Command(commands=['check']))
async def command_check(message: Message, session: AsyncSession) -> None:
    is_initiator_admin = await utils.is_admin(message.from_user.id, message)
    chat_info = ChatInfo(await database.get_chat_info(session, message.chat.id))

    if not message.reply_to_message:
        await message.reply(
            f'Наличие иммунитета к трибуналу: {is_initiator_admin or message.from_user.id in chat_info.tribunal_immunity}')
        return

    if not is_initiator_admin:
        await message.reply('Ты не админ.')
        return

    is_target_admin = await utils.is_admin(message.reply_to_message.from_user.id, message)
    await message.reply(
        f'Наличие иммунитета к трибуналу: {is_target_admin or message.reply_to_message.from_user.id in chat_info.tribunal_immunity}')
