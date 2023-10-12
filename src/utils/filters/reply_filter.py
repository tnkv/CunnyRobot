from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils import check_rights


class NeedReplyFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        if not message.reply_to_message:
            await message.reply('А ответить на сообщение?')
            return False

        return True
