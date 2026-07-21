from __future__ import annotations

from abc import ABC
from typing import Optional, cast

from aiogram.enums import ChatType
from aiogram.types import TelegramObject, User, Chat, ChatMemberUpdated
from aiogram_i18n.managers import BaseManager
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import ChatInfo, database


class LocaleManager(BaseManager, ABC):
    async def get_locale(
            self,
            event: TelegramObject,
            session: AsyncSession,
            event_from_user: Optional[User] = None,
            event_chat: Optional[Chat] = None,
            chat_info: Optional[ChatInfo] = None
            ) -> str:

        if not event_from_user:
            return cast(str, self.default_locale)

        if not event_chat or event_chat.type == ChatType.PRIVATE:
            return event_from_user.language_code or cast(str, self.default_locale)

        if chat_info is not None:
            if isinstance(event, ChatMemberUpdated):
                chat_info.chat_language = event_from_user.language_code
                await database.set_chat_info(session, chat_info.export())

            return chat_info.chat_language or cast(str, self.default_locale)

        return event_from_user.language_code or cast(str, self.default_locale)

    async def set_locale(self):
        pass
