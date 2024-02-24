from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.utils import keyboards

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, i18n: I18nContext) -> Message:
    if message.chat.type == ChatType.PRIVATE:
        return await message.answer(
            text=i18n.command.start(),
            reply_markup=keyboards.add_to_chat_keyboard(
                i18n,
                (await message.bot.get_me()).username
            )
        )
