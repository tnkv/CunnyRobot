import os

from aiogram import Bot, Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.types import CallbackQuery, ChatPermissions

from time import time

from src.utils import database, keyboards, nameformat
from src.utils.CaptchaCallbackFactory import CaptchaCallbackFactory

router = Router()
bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")

# Обработка кнопки в капче
@router.callback_query(CaptchaCallbackFactory.filter())  # Принимаю калбек команды
async def callback_captcha(callback: CallbackQuery, callback_data: CaptchaCallbackFactory):
    date = callback_data.date
    actualDate = int(time())
    user = callback_data.user
    chat = callback_data.chat
    if callback.from_user.id != user:
        await callback.answer(text="Эта кнопка не для тебя.", show_alert=True)
        return

    if date + 60 >= actualDate:
        await callback.answer(text=f"Кнопка заработает через {date + 60 - actualDate} секунд.", show_alert=True)
        return

    await callback.answer()
    try:
        await bot.restrict_chat_member(chat_id=chat, user_id=user,
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
@router.callback_query(F.data == "cancel_tribunal")
async def callback_cancel_tribunal(callback: CallbackQuery):
    initiator = (await callback.message.chat.get_member(user_id=callback.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await callback.answer()
        return
    await database.setTribunalTimeout(callback.message.chat.id, int(time()))
    try:
        name = nameformat.nameFormat(callback.from_user.id,
                                     callback.from_user.username,
                                     callback.from_user.first_name,
                                     callback.from_user.last_name,
                                     False)
        await bot.stop_poll(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=keyboards.canceled_tribunal_keyboard(name))
    except Exception:
        return

@router.callback_query(F.data == "ended_tribunal")
@router.callback_query(F.data == "canceled_tribunal")
async def callback_no_answer(callback: CallbackQuery):
    await callback.answer()
