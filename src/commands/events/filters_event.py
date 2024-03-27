import re
from typing import Optional

from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.utils import utils, ChatInfo

router = Router()

service_message_types = [
    'new_chat_member', 'left_chat_member', 'new_chat_title', 'new_chat_photo',
    'delete_chat_photo', 'pinned_message', 'video_chat_started', 'video_chat_ended',
    'video_chat_participants_invited'
]


class CommentsFilter(BaseFilter):

    async def __call__(self, message: Message, chat_info: Optional[ChatInfo]) -> bool:
        if chat_info is None:
            return False

        if not chat_info.is_comments:
            return False

        if message.left_chat_member and message.left_chat_member.id == message.bot.id:
            return False

        if message.is_automatic_forward or message.reply_to_message:
            return False

        is_service = message.content_type in service_message_types

        if await utils.is_admin(message.from_user.id, message.chat) and not is_service:
            return False

        return True


class CustomFilters(BaseFilter):
    async def __call__(self, message: Message, chat_info: Optional[ChatInfo]) -> bool:
        if chat_info is None:
            return False

        if not chat_info.filters_enabled:
            return False

        if message.left_chat_member and message.left_chat_member.id == message.bot.id:
            return False

        if await utils.is_admin(message.from_user.id, message.chat):
            return False

        if not message.text:
            return False

        for filter_id, details in chat_info.filters_list.items():
            pattern = re.compile(details.get('regex'))
            if pattern.fullmatch(message.text.lower()) if details.get('full_match', False) \
                    else pattern.search(message.text.lower()):
                return True

        return False


@router.message(CommentsFilter())
async def comments_mode(message: Message, i18n: I18nContext) -> None:
    try:
        await message.delete()
    except Exception as e:
        await message.answer(i18n.get("common-errors-cant_delete_msg", exception=str(e)))


@router.message(CustomFilters())
async def comments_mode(message: Message, i18n: I18nContext) -> None:
    try:
        await message.delete()
    except Exception as e:
        await message.answer(i18n.get("common-errors-cant_delete_msg", exception=str(e)))
