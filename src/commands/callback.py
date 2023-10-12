from time import time

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, ChatPermissions

from src.utils import database, keyboards, nameformat, inflect_with_num
from src.utils.CaptchaCallbackFactory import CaptchaCallbackFactory
from src.utils.ChatInfo import ChatInfo
from src.utils.filters import admin_filter

router = Router()


# Обработка кнопки в капче
@router.callback_query(CaptchaCallbackFactory.filter())  # Принимаю калбек команды
async def callback_captcha(callback: CallbackQuery, callback_data: CaptchaCallbackFactory) -> None:
    date = callback_data.date
    date_now = int(time())
    user = callback_data.user
    chat = callback_data.chat
    if callback.from_user.id != user:
        await callback.answer(text='Эта кнопка не для тебя.', show_alert=True)
        return

    if date_now < date:
        await callback.answer(
            text=f'Кнопка заработает через {inflect_with_num.inflect_with_num(date - date_now, ("секунда", "cекунд", "cекунды"))}',
            show_alert=True)
        return

    await callback.answer()
    try:
        await callback.bot.restrict_chat_member(chat_id=chat, user_id=user,
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
        await callback.message.edit_reply_markup()
    except Exception:
        return


# Обработка отмены трибунала
@router.callback_query(F.data == 'cancel_tribunal', admin_filter.CallbackAdminFilter(False))
async def callback_cancel_tribunal(callback: CallbackQuery) -> None:
    chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
    chat_info.set_tribunal_timeout(int(time()))
    database.setChatInfo(chat_info.export())

    try:
        name = nameformat.nameFormat(callback.from_user.id,
                                     callback.from_user.username,
                                     callback.from_user.first_name,
                                     callback.from_user.last_name,
                                     False)
        await callback.bot.stop_poll(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     reply_markup=keyboards.canceled_tribunal_keyboard(name))
    except Exception:
        return


@router.callback_query(F.data.in_(('canceled_tribunal', 'ended_tribunal', 'confirm', 'unconfirm')))
async def callback_no_answer(callback: CallbackQuery) -> None:
    await callback.answer()


@router.callback_query(F.data == 'settings_enter_btn', admin_filter.CallbackAdminFilter())
async def callback_enter(callback: CallbackQuery) -> None:
    chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
    try:
        await callback.message.edit_reply_markup(callback.inline_message_id,
                                                 reply_markup=keyboards.configuration_welcome_keyboard(chat_info))
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'settings_main_btn', admin_filter.CallbackAdminFilter())
async def callback_settings(callback: CallbackQuery) -> None:
    chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
    try:
        await callback.message.edit_reply_markup(callback.inline_message_id,
                                                 reply_markup=keyboards.configuration_main_keyboard(chat_info))
    except TelegramBadRequest:
        pass
