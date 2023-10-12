from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.utils import check_rights


class AdminFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        if not await check_rights.is_admin(message.from_user.id, message):
            await message.reply('Ты не админ.')
            return False

        return True


class CallbackAdminFilter(BaseFilter):
    def __init__(self, need_notify=True):
        self.need_notify = need_notify

    async def __call__(self, callback: CallbackQuery) -> bool:
        if await check_rights.is_admin(callback.from_user.id, callback.message):
            return True

        if self.need_notify:
            await callback.answer('Ты не админ.')

        await callback.answer()
        return False
