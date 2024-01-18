from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

import config
from src.utils import utils


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, i18n: I18nContext) -> bool:
        if not await utils.is_admin(message.from_user.id, message.chat):
            await message.reply(i18n.get('common-need_admin_rights'))
            return False

        return True


class CallbackAdminFilter(BaseFilter):
    def __init__(self, need_notify=True):
        self.need_notify = need_notify

    async def __call__(self, callback: CallbackQuery, i18n: I18nContext) -> bool:
        if await utils.is_admin(callback.from_user.id, callback.message.chat):
            return True

        if self.need_notify:
            await callback.answer(i18n.get('common-need_admin_rights'))

        await callback.answer()
        return False


class SuperUserFilter(BaseFilter):
    async def __call__(self, message: Message, i18n: I18nContext) -> bool:
        if config.ADMIN_ID == 0:
            await message.answer(i18n.get('common-super_admin_not_set'))
            return False

        if message.from_user.id == config.ADMIN_ID:
            return True

        return False
