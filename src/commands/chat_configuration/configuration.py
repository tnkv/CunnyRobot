from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, utils
from src.utils.ChatInfo import ChatInfo
from src.utils.filters import admin_filter

router = Router()


@router.message(Command('configure'), admin_filter.AdminFilter())
async def command_configure(message: Message, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, message.chat.id))
    name = utils.name_format(message.from_user.id,
                             message.from_user.username,
                             message.from_user.first_name,
                             message.from_user.last_name)

    await message.reply('<b>Конфигурация чата</b>\n\n'
                        f'{name}, используй кнопки ниже для управление чатом.',
                        reply_markup=keyboards.configuration_main_keyboard(chat_info))


@router.callback_query(F.data == 'comments_settings_btn', admin_filter.CallbackAdminFilter())
async def callback_settings_comments(callback: CallbackQuery, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, callback.message.chat.id))
    chat_info.switch_comments()
    await database.set_chat_info(session, chat_info.export())
    try:
        await callback.message.edit_reply_markup(callback.inline_message_id,
                                                 reply_markup=keyboards.configuration_main_keyboard(chat_info))
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'settings_main_btn', admin_filter.CallbackAdminFilter())
async def callback_settings(callback: CallbackQuery, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, callback.message.chat.id))
    name = utils.name_format(callback.from_user.id,
                             callback.from_user.username,
                             callback.from_user.first_name,
                             callback.from_user.last_name)
    try:
        await callback.message.edit_text(text='<b>Конфигурация чата</b>\n\n'
                                              f'{name}, используй кнопки ниже для управление чатом.',
                                         reply_markup=keyboards.configuration_main_keyboard(chat_info))

    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'settings_filters_btn', admin_filter.CallbackAdminFilter())
async def callback_filters(callback: CallbackQuery, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, callback.message.chat.id))
    name = utils.name_format(callback.from_user.id,
                             callback.from_user.username,
                             callback.from_user.first_name,
                             callback.from_user.last_name)
    try:
        await callback.message.edit_text(text='<b>Конфигурация чата</b>\n'
                                              f'<b>Фильтры</b>\n\n'
                                              f'{name}, используй кнопки ниже для управление чатом.',
                                         reply_markup=keyboards.configuration_filter_keyboard(chat_info))
    except TelegramBadRequest:
        pass
