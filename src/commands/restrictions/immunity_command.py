from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, utils, ChatInfo, filters

router = Router()


@router.message(Command(commands=['give_immune', 'give_immunity']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_give_immune(message: Message, session: AsyncSession, chat_info: ChatInfo, i18n: I18nContext) -> Message:
    name = utils.name_format(
        message.reply_to_message.from_user.id,
        message.reply_to_message.from_user.username,
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name
    )

    if not chat_info.add_immune(message.reply_to_message.from_user.id):
        return await message.reply(i18n.get('command-immunity-give-already', name=name))

    await database.set_chat_info(session, chat_info.export())
    await message.reply(i18n.get('command-immunity-give', name=name))


# Отмена иммунитета
@router.message(Command(commands=['revoke_immune', 'revoke_immunity']), filters.AdminFilter(),
                filters.NeedReplyFilter())
async def command_revoke_immune(message: Message, session: AsyncSession, chat_info: ChatInfo, i18n: I18nContext) -> Message:
    name = utils.name_format(
        message.reply_to_message.from_user.id,
        message.reply_to_message.from_user.username,
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name
    )

    if not chat_info.revoke_immune(message.reply_to_message.from_user.id):
        return await message.reply(i18n.get('command-immunity-revoke-already', name=name))

    await database.set_chat_info(session, chat_info.export())
    await message.reply(i18n.get('command-immunity-revoke', name=name))


# Проверка наличия иммунитета
@router.message(Command(commands=['check']))
async def command_check(message: Message, chat_info: ChatInfo, i18n: I18nContext) -> Message | None:
    is_initiator_admin = await utils.is_admin(message.from_user.id, message)

    if not message.reply_to_message:
        immune_status = is_initiator_admin or message.from_user.id in chat_info.tribunal_immunity
        return await message.reply(i18n.get('command-immunity-check', status=immune_status))

    if not is_initiator_admin:
        await message.reply(i18n.get('common-need_admin_rights'))
        return

    is_target_admin = await utils.is_admin(message.reply_to_message.from_user.id, message)
    immune_status = is_target_admin or message.reply_to_message.from_user.id in chat_info.tribunal_immunity

    await message.reply(i18n.get('command-immunity-check', status=immune_status))
