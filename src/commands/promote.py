from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message

from src.utils import database, nameformat
from src.utils.ChatInfo import ChatInfo

router = Router()
ADMIN_STATUS = (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)


# Выдача иммунитета от трибунала (У всех админов он по умолчанию потому что их замутить нельзя)
@router.message(Command(commands=['give_immune', 'give_immunity']))
async def command_give_admin(message: Message) -> None:
    if (await message.chat.get_member(user_id=message.from_user.id)).status not in ADMIN_STATUS:
        await message.reply('Ты не админ.')
        return

    if not message.reply_to_message:
        await message.reply('А ответить на сообщение?')
        return

    chat_info = ChatInfo(database.getChatInfo(message.chat.id))
    name = nameformat.nameFormat(message.reply_to_message.from_user.id,
                                 message.reply_to_message.from_user.username,
                                 message.reply_to_message.from_user.first_name,
                                 message.reply_to_message.from_user.last_name)

    if not chat_info.add_immune(message.reply_to_message.from_user.id):
        await message.reply(f'У пользователя {name} уже был иммунитет от трибунала.\n\n'
                            'Проверить наличие можно через /check\n'
                            'Забрать иммунитет можно через /revoke_immune')
        return

    database.setChatInfo(chat_info.export())
    await message.reply(f'Пользователю {name} был выдан иммунитет от трибунала.\n\n'
                        'Проверить наличие можно через /check\n'
                        'Забрать иммунитет можно через /revoke_immune')


# Отмена иммунитета
@router.message(Command(commands=['revoke_immune', 'revoke_immunity']))
async def command_revoke_admin(message: Message) -> None:
    if not ((await message.chat.get_member(user_id=message.from_user.id)).status in ADMIN_STATUS):
        await message.reply('Ты не админ.')
        return

    if not message.reply_to_message:
        await message.reply('А ответить на сообщение?')
        return

    chat_info = ChatInfo(database.getChatInfo(message.chat.id))
    name = nameformat.nameFormat(message.reply_to_message.from_user.id,
                                 message.reply_to_message.from_user.username,
                                 message.reply_to_message.from_user.first_name,
                                 message.reply_to_message.from_user.last_name)
    if not chat_info.revoke_immune(message.reply_to_message.from_user.id):
        await message.reply(f'У пользователя {name} отсутствовал иммунитет к трибуналу.\n\n'
                            'Проверить наличие можно через /check\n'
                            'Выдать иммунитет можно через /give_immune')
        return

    database.setChatInfo(chat_info.export())
    await message.reply(f'У пользователя {name} был отобран иммунитет от трибунала.\n\n'
                        'Проверить наличие можно через /check\n'
                        'Выдать иммунитет можно через /give_immune')


# Проверка наличия иммунитета
@router.message(Command(commands=['check']))
async def command_check(message: Message) -> None:
    is_initiator_admin = ((await message.chat.get_member(user_id=message.from_user.id)).status in ADMIN_STATUS)
    chat_info = ChatInfo(database.getChatInfo(message.chat.id))

    if not message.reply_to_message:
        await message.reply(
            f'Наличие иммунитета к трибуналу: {is_initiator_admin or message.from_user.id in chat_info.tribunal_immunity}')
        return

    if not is_initiator_admin:
        await message.reply('Ты не админ.')
        return

    is_target_admin = (await message.chat.get_member(user_id=message.reply_to_message.from_user.id)).status in (
        ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)
    await message.reply(
        f'Наличие иммунитета к трибуналу: {is_target_admin or message.reply_to_message.from_user.id in chat_info.tribunal_immunity}')
