from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.utils import keyboards

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, i18n: I18nContext) -> Message:
    if message.chat.id == message.from_user.id:
        return await message.answer(text=i18n.get("command-start"),
                                    reply_markup=keyboards.add_to_chat_keyboard((await message.bot.get_me()).username))

