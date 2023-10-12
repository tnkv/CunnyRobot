from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.utils import database, keyboards
from src.utils.ChatInfo import ChatInfo
from src.utils.filters import admin_filter
from src.utils.nameformat import nameFormat

router = Router()


@router.message(Command('configure'), admin_filter.AdminFilter())
async def command_configure(message: Message) -> None:
    chat_info = ChatInfo(database.getChatInfo(message.chat.id))
    name = nameFormat(message.from_user.id,
                      message.from_user.username,
                      message.from_user.first_name,
                      message.from_user.last_name)

    await message.reply('<b>Конфигурация чата</b>\n\n'
                        f'{name}, используй кнопки ниже для управление чатом.',
                        reply_markup=keyboards.configuration_main_keyboard(chat_info))


@router.callback_query(F.data == 'comments_settings_btn', admin_filter.CallbackAdminFilter())
async def callback_settings_comments(callback: CallbackQuery) -> None:
    chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
    chat_info.switch_comments()
    database.setChatInfo(chat_info.export())
    try:
        await callback.message.edit_reply_markup(callback.inline_message_id,
                                                 reply_markup=keyboards.configuration_main_keyboard(chat_info))
    except TelegramBadRequest:
        pass
