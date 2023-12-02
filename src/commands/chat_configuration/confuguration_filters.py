from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from src.commands.chat_configuration.filers_modify import add_filter, remove_filter
from src.utils import database, keyboards
from src.utils.ChatInfo import ChatInfo
from src.utils.filters import admin_filter

router = Router()
router.include_routers(add_filter.router,
                       remove_filter.router)


@router.callback_query(F.data == 'filters_list_btn', admin_filter.CallbackAdminFilter())
async def callback_filters_list(callback: CallbackQuery) -> None:
    chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
    message = ('<b>Конфигурация чата</b>\n'
               '<b>Фильтры</b>\n'
               '<b>Список фильтров</b>\n\n')
    for filter_id, filter_details in chat_info.filters_list.items():
        message += (f'<code>{filter_id}</code>:\n'
                    f'Regex: <code>{filter_details.get("regex", "Broken")}</code>\n'
                    f'Тип проверки: {"Полное соответствие" if filter_details.get("full_match", False) else "Частичное соответствие"}\n\n')

    await callback.message.edit_text(text=message,
                                     reply_markup=keyboards.configuration_filter_list_keyboard())
    await callback.answer()


@router.callback_query(F.data == 'filters_switch_btn', admin_filter.CallbackAdminFilter())
async def callback_enter_welcome(callback: CallbackQuery) -> None:
    chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
    chat_info.switch_filters()
    database.setChatInfo(chat_info.export())
    try:
        await callback.message.edit_reply_markup(callback.inline_message_id,
                                                 reply_markup=keyboards.configuration_filter_keyboard(chat_info))
    except TelegramBadRequest:
        pass