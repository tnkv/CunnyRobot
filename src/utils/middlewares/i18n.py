from __future__ import annotations

from abc import ABC
from typing import Optional, cast

from aiogram.types import User
from aiogram_i18n.managers import BaseManager


class UserManager(BaseManager, ABC):

    async def get_locale(self, event_from_user: Optional[User] = None) -> str:
        if event_from_user:
            return event_from_user.language_code or cast(str, self.default_locale)
        return cast(str, self.default_locale)

    async def set_locale(self):
        pass
