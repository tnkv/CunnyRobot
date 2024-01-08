from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from aiogram_i18n import I18nContext

from src.utils import filters

router = Router()


@router.message(Command(commands=['unmute', 'um', 'unban']), filters.AdminFilter())
async def command_um(message: Message, i18n: I18nContext) -> bool | Message:
    if message.reply_to_message:
        if message.from_user.id == 136817688 and message.reply_to_message.sender_chat:
            return await message.chat.unban_sender_chat(message.reply_to_message.sender_chat.id)

        TelegramID = message.reply_to_message.from_user.id
    else:
        msg = message.text.split(' ')
        if len(msg) >= 2 and msg[1].isdigit():
            TelegramID = int(msg[1])
        else:
            return await message.reply(i18n.get('command-unmute-need_telegram_id'))

    try:
        await message.chat.restrict(
            user_id=TelegramID,
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
        await message.reply(i18n.get('command-unmute-unmute', user=TelegramID))

    except Exception as e:
        await message.reply(i18n.get('common-errors-cant_unmute', exception=str(e)))
