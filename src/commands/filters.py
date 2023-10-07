from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils import database

router = Router()

service_message_types = [
    'new_chat_member', 'left_chat_member', 'new_chat_title', 'new_chat_photo',
    'delete_chat_photo', 'pinned_message', 'video_chat_started', 'video_chat_ended',
    'video_chat_participants_invited'
]

class CommentsFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        if not database.is_comments(message.chat.id):
            return False

        is_admin = (await message.chat.get_member(user_id=message.from_user.id)).status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
        is_service = message.content_type in service_message_types
        is_bannable = not message.reply_to_message and not message.is_automatic_forward and (not is_admin or is_service)
        return is_bannable


@router.message(CommentsFilter())
async def comments_mode(message: Message) -> None:
    try:
        await message.delete()
    except Exception:
        pass
