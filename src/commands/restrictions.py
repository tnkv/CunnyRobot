from time import time

from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

router = Router()


# бан
@router.message(Command("ban"))
async def command_ban(message: Message):
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply("Ты не админ.")
        return

    if message.reply_to_message:
        await message.chat.ban(user_id=message.reply_to_message.from_user.id)
        return

    await message.reply("А ответить на сообщение?")


# Мут
@router.message(Command(commands=["mute", "m"]))
async def command_mute(message: Message):
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply("Ты не админ.")
        return

    if not message.reply_to_message:
        await message.reply("А ответить на сообщение?")
        return

    msg = message.text.split(" ")
    if len(msg) < 2:
        await message.chat.restrict(user_id=message.reply_to_message.from_user.id,
                                    until_date=0,
                                    permissions=ChatPermissions(can_send_messages=False))
        return

    await message.chat.restrict(user_id=message.reply_to_message.from_user.id,
                                until_date=getRestrictTime(msg[1]),
                                permissions=ChatPermissions(can_send_messages=False))


# Анбан/анмут
@router.message(Command(commands=["unmute", "um", "unban"]))
async def command_mute(message: Message):
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply("Ты не админ.")
        return

    if not message.reply_to_message:
        await message.reply("А ответить на сообщение?")
        return

    await message.chat.restrict(user_id=message.reply_to_message.from_user.id,
                                until_date=0,
                                permissions=ChatPermissions(can_send_messages=True,
                                                            can_pin_messages=True,
                                                            can_send_other_messages=True,
                                                            can_send_polls=True,
                                                            can_change_info=True,
                                                            can_invite_users=True,
                                                            can_send_audios=True,
                                                            can_send_photos=True,
                                                            can_send_videos=True,
                                                            can_manage_topics=True,
                                                            can_send_documents=True,
                                                            can_send_video_notes=True,
                                                            can_send_voice_notes=True,
                                                            can_add_web_page_previews=True))


# Перевод времени для темпмута
def getRestrictTime(duration):
    unit = duration[-1]
    value = int(duration[:-1])
    coefficient = {"m": 60, "h": 3600, "d": 86400}
    return int(time()) + value * coefficient[unit] if unit in ("m", "h", "d") else 0
