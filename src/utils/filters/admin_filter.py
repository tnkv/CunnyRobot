from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.utils import utils


class AdminFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        if not await utils.is_admin(message.from_user.id, message):
            await message.reply('Ты не админ.')
            return False

        return True


class CallbackAdminFilter(BaseFilter):
    def __init__(self, need_notify=True):
        self.need_notify = need_notify

    async def __call__(self, callback: CallbackQuery) -> bool:
        if await utils.is_admin(callback.from_user.id, callback.message):
            return True

        if self.need_notify:
            await callback.answer('Ты не админ.')

        await callback.answer()
        return False
