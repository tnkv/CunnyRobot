from time import time

from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, ChatPermissions, CallbackQuery
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import keyboards, database, utils, ChatInfo, CaptchaCallbackFactory

router = Router()


# Добавляю чат в бд если добавили бота в него
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def event_new_chat(event: ChatMemberUpdated, session: AsyncSession, i18n: I18nContext) -> None:
    await database.add_chat(session, event.chat.id)
    await event.bot.send_message(
        event.chat.id, text=i18n.get('events-welcomer-newchat-noadmin')
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=(IS_NOT_MEMBER | MEMBER) >> ADMINISTRATOR))
async def event_new_chat(event: ChatMemberUpdated, session: AsyncSession, i18n: I18nContext) -> None:
    await database.add_chat(session, event.chat.id)
    await event.bot.send_message(
        event.chat.id, i18n.get('events-welcomer-newchat-admin')
    )


# Приветствие нового участника
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def event_new_member(event: ChatMemberUpdated, session: AsyncSession, i18n: I18nContext) -> None:
    if await utils.is_cas_ban(event.from_user.id):
        await event.chat.ban(user_id=event.from_user.id)

    chat_info = ChatInfo(await database.get_chat_info(session, event.chat.id))

    if chat_info.is_comments:
        await event.chat.ban(user_id=event.from_user.id)
        await event.chat.restrict(
            user_id=event.from_user.id,
            until_date=0,
            permissions=ChatPermissions(
                can_send_messages=True,
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
                can_add_web_page_previews=True)
        )
        return

    if not chat_info.welcome_message:
        return

    member = await event.chat.get_member(user_id=event.from_user.id)
    name = utils.name_format(
        event.from_user.id,
        event.from_user.username,
        event.from_user.first_name,
        event.from_user.last_name
    )

    if member.status in (ChatMemberStatus.RESTRICTED,) and not member.can_send_messages:
        await event.bot.send_message(
            event.chat.id,
            i18n.get('events-welcomer-captcha_not_solved', name=name)
        )
        return

    try:
        await event.chat.restrict(
            user_id=event.from_user.id,
            until_date=0,
            permissions=ChatPermissions(can_send_messages=False)
        )
        welcome_message_text = chat_info.welcome_message_text.format(
            user=name) if '{user}' in chat_info.welcome_message_text else chat_info.welcome_message_text

        await event.bot.send_message(
            chat_id=event.chat.id,
            text=welcome_message_text,
            reply_markup=keyboards.captcha_keyboard(
                int(time()) + chat_info.welcome_message_timeout,
                event.from_user.id,
                event.chat.id),
            disable_web_page_preview=True
        )
    except Exception as e:
        await event.bot.send_message(
            chat_id=event.chat.id,
            text=i18n.get('common-errors-cant_mute', exception=e)
        )


# Обработка кнопки в капче
@router.callback_query(CaptchaCallbackFactory.filter())  # Принимаю калбек команды
async def callback_captcha(callback: CallbackQuery, callback_data: CaptchaCallbackFactory, i18n: I18nContext) -> None:
    date = callback_data.date
    date_now = int(time())
    user = callback_data.user
    chat = callback_data.chat
    if callback.from_user.id != user:
        await callback.answer(text=i18n.get('callback-button_not_your'), show_alert=True)
        return

    if date_now < date:
        await callback.answer(
            text=i18n.get('callback-button_become_active_in', seconds=date - date_now),
            show_alert=True)
        return

    await callback.answer()
    try:
        await callback.bot.restrict_chat_member(
            chat_id=chat, user_id=user,
            until_date=0,
            permissions=ChatPermissions(
                can_send_messages=True,
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
                can_add_web_page_previews=True
            )
        )
        await callback.message.edit_reply_markup()
    except Exception as e:
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=i18n.get('common-errors-cant_unmute', exception=e)
        )
