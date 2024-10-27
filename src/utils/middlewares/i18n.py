from __future__ import annotations

from abc import ABC
from typing import Optional, cast

from aiogram.enums import ChatType
from aiogram.types import TelegramObject, User, Chat
from aiogram_i18n.managers import BaseManager
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import ChatInfo, database


class LocaleManager(BaseManager, ABC):
    async def get_locale(
            self,
            event: TelegramObject,
            session: AsyncSession,
            event_from_user: Optional[User] = None,
            chat_info: Optional[ChatInfo] = None
            ) -> str:
        if not (event.message or event.callback_query or event.chat_member or event.my_chat_member):
            return cast(str, self.default_locale)

        if event.message:
            chat_obj: Chat = event.message.chat
        elif event.callback_query:
            chat_obj: Chat = event.callback_query.message.chat
        elif event.chat_member:
            chat_obj: Chat = event.chat_member.chat
        else:
            chat_obj: Chat = event.my_chat_member.chat
            chat_info.chat_language = event_from_user.language_code
            await database.set_chat_info(session, chat_info.export())


        if chat_obj.type == ChatType.PRIVATE:
            if event_from_user:
                return event_from_user.language_code or cast(str, self.default_locale)

            return cast(str, self.default_locale)

        return chat_info.chat_language or cast(str, self.default_locale)

    async def set_locale(self):
        pass
