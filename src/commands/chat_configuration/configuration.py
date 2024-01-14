from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, utils, ChatInfo, filters

router = Router()


@router.message(Command('configure'), filters.AdminFilter())
async def command_configure(message: Message, chat_info: ChatInfo, i18n: I18nContext) -> None:
    name = utils.NameFormat(message.from_user)

    await message.reply(i18n.command.configuration(name=name.get()),
                        reply_markup=keyboards.configuration_main_keyboard(i18n, chat_info))


@router.callback_query(F.data == 'comments_settings_btn', filters.CallbackAdminFilter())
async def callback_settings_comments(callback: CallbackQuery, session: AsyncSession, chat_info: ChatInfo,
                                     i18n: I18nContext) -> None:
    chat_info.switch_comments()
    await database.set_chat_info(session, chat_info.export())
    try:
        await callback.message.edit_reply_markup(
            callback.inline_message_id,
            reply_markup=keyboards.configuration_main_keyboard(i18n, chat_info)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'settings_main_btn', filters.CallbackAdminFilter())
async def callback_settings(callback: CallbackQuery, chat_info: ChatInfo, i18n: I18nContext) -> None:
    name = utils.NameFormat(callback.from_user)
    try:
        await callback.message.edit_text(text=i18n.command.configuration(name=name.get()),
                                         reply_markup=keyboards.configuration_main_keyboard(i18n, chat_info))

    except TelegramBadRequest:
        pass
