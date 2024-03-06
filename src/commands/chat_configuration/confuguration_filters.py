from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import html_decoration
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.commands.chat_configuration.filers_modify import add_filter, remove_filter
from src.utils import database, keyboards, ChatInfo, filters, utils

router = Router()
router.include_routers(
    add_filter.router,
    remove_filter.router
)


@router.callback_query(F.data == 'settings_filters_btn', filters.CallbackAdminFilter())
async def callback_filters(callback: CallbackQuery, i18n: I18nContext, chat_info: ChatInfo) -> None:
    name = utils.NameFormat(callback.from_user)
    try:
        await callback.message.edit_text(
            text=i18n.command.configuration.filters(name=name.get()),
            reply_markup=keyboards.configuration_filter_keyboard(i18n, chat_info)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'filters_list_btn', filters.CallbackAdminFilter())
async def callback_filters_list(callback: CallbackQuery, i18n: I18nContext, chat_info: ChatInfo) -> None:
    message = i18n.command.configuration.filters.list()
    for filter_id, filter_details in chat_info.filters_list.items():
        message += "\n\n" + i18n.command.configuration.filters.list.filter(
            filter_id=filter_id,
            filter_regex=html_decoration.quote(filter_details.get("regex", "Broken")),
            full_match=filter_details.get("full_match", False)
        )

    await callback.message.edit_text(
        text=message,
        reply_markup=keyboards.configuration_filter_list_keyboard(i18n)
    )
    await callback.answer()


@router.callback_query(F.data == 'filters_switch_btn', filters.CallbackAdminFilter())
async def callback_enter_welcome(callback: CallbackQuery, session: AsyncSession, i18n: I18nContext,
                                 chat_info: ChatInfo) -> None:
    chat_info.switch_filters()
    await database.set_chat_info(session, chat_info.export())
    try:
        await callback.message.edit_reply_markup(
            callback.inline_message_id,
            reply_markup=keyboards.configuration_filter_keyboard(i18n, chat_info)
        )
    except TelegramBadRequest:
        pass
