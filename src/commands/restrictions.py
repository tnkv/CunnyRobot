from time import time

import aiohttp
from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

router = Router()
CAS_LINK = 'https://api.cas.chat/check?user_id={user_id}'
TIME_COEFFICIENT = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}

# Бан
@router.message(Command('ban'))
async def command_ban(message: Message) -> None:
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply('Ты не админ.')
        return

    if message.reply_to_message:
        if message.reply_to_message.from_user.id == 136817688 and message.reply_to_message.sender_chat:
            await message.chat.ban_sender_chat(message.reply_to_message.sender_chat.id)
            return

        await message.chat.ban(user_id=message.reply_to_message.from_user.id)
        return

    msg = message.text.split(' ')
    if len(msg) >= 2 and msg[1].isdigit():
        try:
            await message.chat.ban(user_id=int(msg[1]))
        except Exception:
            await message.reply('Не удалось заблокировать пользователя.')
        return
    await message.reply(
        'Для блокировки пользователя необходимо ответить на сообщение или написать Telegram ID через пробел.')


# Мут
@router.message(Command(commands=['mute', 'm']))
async def command_mute(message: Message) -> None:
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply('Ты не админ.')
        return

    if not message.reply_to_message:
        await message.reply('А ответить на сообщение?')
        return

    msg = message.text.split(' ')
    if len(msg) < 2:
        await message.chat.restrict(user_id=message.reply_to_message.from_user.id,
                                    until_date=0,
                                    permissions=ChatPermissions(can_send_messages=False))
        return

    await message.chat.restrict(user_id=message.reply_to_message.from_user.id,
                                until_date=getRestrictTime(msg[1]),
                                permissions=ChatPermissions(can_send_messages=False))


# Анбан/анмут
@router.message(Command(commands=['unmute', 'um', 'unban']))
async def command_mute(message: Message) -> None:
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply('Ты не админ.')
        return

    if message.reply_to_message:
        if message.from_user.id == 136817688 and message.reply_to_message.sender_chat:
            await message.chat.unban_sender_chat(message.reply_to_message.sender_chat.id)
            return

        TelegramID = message.reply_to_message.from_user.id
    else:
        msg = message.text.split(' ')
        if len(msg) >= 2 and msg[1].isdigit():
            TelegramID = int(msg[1])
        else:
            await message.reply(
                'Для снятия ограничений необходимо ответить на сообщение или написать Telegram ID через пробел.')
            return
    try:
        await message.chat.restrict(user_id=TelegramID,
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
    except Exception:
        await message.reply('Не удалось снять огранчиения.')


@router.message(Command(commands=['is_cas_ban']))
async def command_mute(message: Message) -> None:
    msg = message.text.split(' ')
    if len(msg) < 2:
        await message.reply('Необходимо указать Telegram ID пользователя через пробел')
        return
    if not msg[1].isdigit():
        await message.reply('Некорректный Telegram ID')
        return
    await message.reply(f'Статус блокировки в CAS: {await isCasBan(int(msg[1]))}')


# Перевод времени для темпмута
def getRestrictTime(duration: str) -> int:
    unit = duration[-1]
    value = int(duration[:-1]) if duration[:-1].isdigit() else 0
    return int(time()) + value * TIME_COEFFICIENT.get(unit, 0)


# Проверка наличия пользователя в базе CAS
async def isCasBan(TelegramUserID: int) -> bool:
    session = aiohttp.ClientSession()
    async with session.get(CAS_LINK.format(user_id=TelegramUserID)) as resp:
        answer = await resp.json(content_type='application/json')
        await session.close()

    return answer.get('ok', False)
