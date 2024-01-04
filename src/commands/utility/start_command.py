from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.utils import keyboards

router = Router()


@router.message(CommandStart())
async def command_start(message: Message) -> Message:
    if message.chat.id == message.from_user.id:
        return await message.answer(text='Этот бот работает только в чатах, выбери чат куда хочешь добавить бота.',
                                    reply_markup=keyboards.add_to_chat_keyboard((await message.bot.get_me()).username))

