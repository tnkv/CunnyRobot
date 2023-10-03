from time import time

from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER, RESTRICTED, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, ChatPermissions

from src.commands import restrictions
from src.utils import keyboards, database, nameformat

router = Router()


# Добавляю чат в бд если добавили бота в него
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> (MEMBER | ADMINISTRATOR)))
async def event_new_chat(event: ChatMemberUpdated) -> None:
    await database.addChat(event.chat.id)


# Приветствие нового участника
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def event_new_member(event: ChatMemberUpdated) -> None:
    if await restrictions.isCasBan(event.from_user.id):
        await event.chat.ban(user_id=event.from_user.id)

    welcomeMessage = await database.getCaptchaText(event.chat.id)
    if welcomeMessage == 'disable':
        return

    member = await event.chat.get_member(user_id=event.from_user.id)
    name = nameformat.nameFormat(event.from_user.id,
                                 event.from_user.username,
                                 event.from_user.first_name,
                                 event.from_user.last_name)

    if member.status in (ChatMemberStatus.RESTRICTED,) and not member.can_send_messages:
        await event.bot.send_message(event.chat.id,
                                     f'Привет {name}, если тебя не замутил админ, то ты пропустил сообщение с кнопкой при первом входе, найди его с помощью \"<code>@</code>\" в поиске.')

    try:
        await event.chat.restrict(user_id=event.from_user.id,
                                  until_date=0,
                                  permissions=ChatPermissions(can_send_messages=False))
        await event.bot.send_message(event.chat.id, (welcomeMessage.format(user=name) if '{user}' in welcomeMessage else welcomeMessage),
                                     reply_markup=keyboards.captcha_keyboard(int(time()), event.from_user.id, event.chat.id),
                                     disable_web_page_preview=True)
    except Exception:
        return
