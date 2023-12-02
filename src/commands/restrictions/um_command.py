from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from src.utils.filters import admin_filter

router = Router()


@router.message(Command(commands=['unmute', 'um', 'unban']), admin_filter.AdminFilter())
async def command_um(message: Message) -> None:
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
