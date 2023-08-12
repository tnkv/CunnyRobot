import os

from aiogram import Bot
from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message

from src.utils import database, nameformat

bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
router = Router()

# Выдача иммунитета от трибунала (У всех админов он по умолчанию потому что их замутить нельзя)
@router.message(Command(commands=["give_immune"]))
async def command_give_admin(message: Message) -> None:
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply("Ты не админ.")
        return

    if not message.reply_to_message:
        await message.reply("А ответить на сообщение?")
        return

    await database.addImmune(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(
        f"У пользователя {nameformat.nameFormat(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name)} появился иммунитет от трибунала, проверить наличие можно через /check, забрать иммунитет можно через /revoke_immune")

# Проверка наличия иммунитета
@router.message(Command(commands=["check"]))
async def command_check(message: Message) -> None:
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status

    if not message.reply_to_message:
        await message.reply(
            f"Наличие иммунитета к трибуналу: {await database.isImmune(message.chat.id, message.from_user.id)}")
        return
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply("Ты не админ.")
        return
    await message.reply(
        f"Наличие иммунитета к трибуналу: {await database.isImmune(message.chat.id, message.reply_to_message.from_user.id)}")

# Отмена иммунитета
@router.message(Command(commands=["revoke_immune"]))
async def command_give_admin(message: Message) -> None:
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply("Ты не админ.")
        return

    if not message.reply_to_message:
        await message.reply("А ответить на сообщение?")
        return

    await database.revokeImmune(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(
        f"У пользователя {nameformat.nameFormat(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name)} был отобран иммунитет от трибунала, проверить наличие можно через /check, выдать иммунитет можно через /give_immune")
