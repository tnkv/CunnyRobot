import re

from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils import database, utils
from src.utils.ChatInfo import ChatInfo

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

        is_admin = await utils.is_admin(message.from_user.id, message)
        is_service = message.content_type in service_message_types
        is_bannable = not message.reply_to_message and not message.is_automatic_forward and (not is_admin or is_service)
        return is_bannable


class CustomFilters(BaseFilter):
    async def __call__(self, message: Message):
        chat_info = ChatInfo(database.getChatInfo(message.chat.id))
        is_admin = await utils.is_admin(message.from_user.id, message)

        if is_admin or not chat_info.filters_enabled:
            return False

        for filter_id, details in chat_info.filters_list.items():
            pattern = re.compile(details.get('regex'))
            if pattern.fullmatch(message.text) if details.get('full_match', False) else pattern.search(message.text):
                return True

        return False


@router.message(CommentsFilter())
async def comments_mode(message: Message) -> None:
    try:
        await message.delete()
    except Exception:
        pass


@router.message(CustomFilters())
async def comments_mode(message: Message) -> None:
    try:
        await message.delete()
    except Exception:
        pass
