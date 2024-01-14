from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.commands.chat_configuration.filers_modify import add_filter, remove_filter
from src.utils import database, keyboards, ChatInfo, filters, utils
from src.utils.callback_factory import SetLangFactory

router = Router()


@router.callback_query(F.data == 'settings_members_btn', filters.CallbackAdminFilter())
async def callback_members(callback: CallbackQuery, i18n: I18nContext, chat_info: ChatInfo) -> None:
    name = utils.NameFormat(callback.from_user)
    try:
        await callback.message.edit_text(
            text=i18n.command.configuration.members(name=name.get()),
            reply_markup=keyboards.configuration_members_keyboard(i18n, chat_info)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'settings_members_setlang', filters.CallbackAdminFilter())
async def callback_members_setlang(callback: CallbackQuery, i18n: I18nContext, chat_info: ChatInfo) -> None:
    name = utils.NameFormat(callback.from_user)
    try:
        await callback.message.edit_text(
            text=i18n.command.configuration.members.lang(name=name.get()),
            reply_markup=keyboards.configuration_members_lang_keyboard(i18n, chat_info)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(SetLangFactory.filter(), filters.CallbackAdminFilter())
async def callback_setlang(
        callback: CallbackQuery,
        callback_data: SetLangFactory,
        session: AsyncSession,
        i18n: I18nContext,
        chat_info: ChatInfo) -> None:
    name = utils.NameFormat(callback.from_user)
    chat_info.set_lang(callback_data.lang)
    i18n.locale = callback_data.lang
    await callback.answer()
    await callback.message.edit_text(
        text=i18n.command.configuration.members.lang(name=name.get()),
        reply_markup=keyboards.configuration_members_lang_keyboard(i18n, chat_info)
    )
    await database.set_chat_info(session, chat_info.export())
