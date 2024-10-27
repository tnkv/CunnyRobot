import asyncio
from time import time

from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, ChatPermissions, CallbackQuery
from aiogram.utils.text_decorations import html_decoration
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
async def event_new_member(event: ChatMemberUpdated, chat_info: ChatInfo, i18n: I18nContext) -> None:
    invited_by_admin = await utils.is_admin(event.from_user.id, event.chat)
    if chat_info.is_comments:
        if invited_by_admin:
            return

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

    member = await event.chat.get_member(user_id=event.new_chat_member.user.id)

    name = utils.NameFormat(event.new_chat_member.user)

    if member.status in (ChatMemberStatus.RESTRICTED,) and not member.can_send_messages:
        await event.bot.send_message(
            event.chat.id,
            i18n.get('events-welcomer-captcha_not_solved', name=name.get())
        )
        return

    try:
        if not invited_by_admin:
            await event.chat.restrict(
                user_id=event.from_user.id,
                until_date=0,
                permissions=ChatPermissions(can_send_messages=False)
            )
        welcome_message_text = (
            chat_info.welcome_message_text
            .replace("{user}", name.get())
            .replace("{user_name}", html_decoration.quote(event.new_chat_member.user.full_name))
            .replace("{user_id}", str(event.from_user.id))
            .replace("{chat_title}", event.chat.title or str(event.chat.id))
            .replace("{timestamp}", str(int(time())))
        )
        msg = await event.bot.send_message(
            chat_id=event.chat.id,
            text=welcome_message_text,
            reply_markup=None if invited_by_admin else keyboards.captcha_keyboard(
                i18n,
                int(time()) + chat_info.welcome_message_timeout,
                event.from_user.id,
                event.chat.id),
            disable_web_page_preview=True
        )
    except Exception as e:
        msg = await event.bot.send_message(
            chat_id=event.chat.id,
            text=i18n.get('common-errors-cant_mute', exception=str(e))
        )

    if await utils.is_cas_ban(event.from_user.id):
        await event.chat.ban(user_id=event.from_user.id)
        await msg.edit_text(
            text=i18n.cas.autoban()
        )

        # Удаляю сообщение через 10 минут, что бы не было спама в чат от меня же
        await asyncio.sleep(10 * 60)
        try:
            await msg.delete()
        except Exception:
            pass
        return

    # Повторная проверка CAS
    await asyncio.sleep(30 * 60)

    if await utils.is_cas_ban(event.from_user.id):
        try:
            await event.chat.ban(user_id=event.from_user.id)
            await msg.edit_text(
                text=i18n.cas.autoban()
            )
            await asyncio.sleep(5 * 60)
            await msg.delete()
        except Exception:
            pass


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
            text=i18n.callback.button_become_active_in(
                seconds=i18n.common.format.seconds.wait(
                    form=utils.inflect_with_num(date - date_now),
                    count=date - date_now
                )
            ),
            show_alert=True
        )
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
    except TelegramBadRequest:
        return
    except Exception as e:
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=i18n.get('common-errors-cant_unmute', exception=str(e))
        )
