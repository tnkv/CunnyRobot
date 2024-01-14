from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram_i18n import I18nContext


class NeedReplyFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message, i18n: I18nContext) -> bool:
        if not message.reply_to_message:
            await message.reply(i18n.get('common-need_reply'))
            return False

        return True
