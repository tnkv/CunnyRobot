from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.utils import database, keyboards
from src.utils.ChatInfo import ChatInfo
from src.utils.nameformat import nameFormat

router = Router()


@router.message(Command('configure'))
async def command_configure(message: Message) -> None:
    chat_info = ChatInfo(database.getChatInfo(message.chat.id))
    name = nameFormat(message.from_user.id,
                      message.from_user.username,
                      message.from_user.first_name,
                      message.from_user.last_name)

    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply('Ты не админ.')
        return

    await message.reply('<b>Конфигурация чата</b>\n\n'
                        f'{name}, используй кнопки ниже для управление чатом.',
                        reply_markup=keyboards.configuration_main_keyboard(chat_info))


@router.callback_query(F.data == 'comments_settings_btn')
async def callback_settings_comments(callback: CallbackQuery) -> None:
    initiator = (await callback.bot.get_chat_member(chat_id=callback.message.chat.id,
                                                    user_id=callback.from_user.id)).status
    if initiator in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
        chat_info.switch_comments()
        database.setChatInfo(chat_info.export())
        try:
            await callback.message.edit_reply_markup(callback.inline_message_id,
                                                     reply_markup=keyboards.configuration_main_keyboard(chat_info))
        except TelegramBadRequest:
            pass

    await callback.answer()
