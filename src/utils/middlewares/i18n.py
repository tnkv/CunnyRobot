from __future__ import annotations

from abc import ABC
from typing import Optional, cast

from aiogram.enums import ChatType
from aiogram.types import TelegramObject
from aiogram_i18n.managers import BaseManager

from src.utils import ChatInfo


class LocaleManager(BaseManager, ABC):
    async def get_locale(self, event: TelegramObject, chat_info: Optional[ChatInfo] = None) -> str:
        if not (event.message or event.callback_query):
            return cast(str, self.default_locale)

        chat_type = event.message.chat.type if event.message else event.callback_query.message.chat.type
        if chat_type == ChatType.PRIVATE:
            return cast(str, self.default_locale)

        return chat_info.chat_language

    async def set_locale(self):
        pass
