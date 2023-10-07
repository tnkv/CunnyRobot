from time import time

from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, ChatPermissions

from src.commands import restrictions
from src.utils import keyboards, database, nameformat
from src.utils.ChatInfo import ChatInfo

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

    chat_info = ChatInfo(database.getChatInfo(event.chat.id))

    if chat_info.is_comments:
        await event.chat.ban(user_id=event.from_user.id)
        await event.chat.restrict(user_id=event.from_user.id,
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
        return

    if not chat_info.welcome_message:
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
        welcome_message_text = chat_info.welcome_message_text.format(
            user=name) if '{user}' in chat_info.welcome_message_text else chat_info.welcome_message_text

        await event.bot.send_message(event.chat.id,
                                     welcome_message_text,
                                     reply_markup=keyboards.captcha_keyboard(
                                         int(time()) + chat_info.welcome_message_timeout,
                                         event.from_user.id,
                                         event.chat.id),
                                     disable_web_page_preview=True)
    except Exception:
        return
