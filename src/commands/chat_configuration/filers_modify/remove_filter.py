from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.text_decorations import html_decoration
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, ChatInfo, filters

router = Router()


class RemoveFilter(StatesGroup):
    removable_id = State()
    confirm_removing = State()


@router.callback_query(F.data == 'filters_remove_btn', filters.CallbackAdminFilter())
async def callback_filters_remove(callback: CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    await callback.message.answer(i18n.command.configuration.filters.remove())
    await state.set_state(RemoveFilter.removable_id)
    await callback.answer()


@router.message(RemoveFilter.removable_id, Command('cancel'))
@router.message(RemoveFilter.confirm_removing, Command('cancel'))
async def cancel_fsm(message: Message, state: FSMContext, i18n: I18nContext):
    await message.reply(i18n.common.action_canceled())
    await state.clear()


@router.callback_query(RemoveFilter.confirm_removing, F.data == 'unconfirm')
async def cancel_fsm(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.message.edit_text(i18n.common.action_canceled())
    await state.clear()


@router.message(RemoveFilter.removable_id)
async def filterremove_waitid(message: Message, chat_info: ChatInfo, i18n: I18nContext, state: FSMContext):
    selected_filter = chat_info.filters_list.get(message.text)
    if selected_filter is None:
        return await message.reply(i18n.command.configuration.filters.remove.notfound(filter_id=message.text))

    await state.update_data(filter_id=message.text)
    await state.set_state(RemoveFilter.confirm_removing)
    await message.answer(
        i18n.command.configuration.filters.remove.confirmation(
            filter_id=message.text,
            regex=html_decoration.quote(
                selected_filter.get("regex")
            ),
            full_match=selected_filter.get("full_match", False)
        ),
        reply_markup=keyboards.confirm_keyboard(i18n)
    )


@router.callback_query(RemoveFilter.confirm_removing, F.data == 'confirm')
async def cancel_fsm(
        callback: CallbackQuery,
        session: AsyncSession,
        chat_info: ChatInfo,
        state: FSMContext,
        i18n: I18nContext):
    data = await state.get_data()
    chat_info.remove_filter(data.get('filter_id'))
    await callback.message.edit_text(i18n.command.configuration.filters.remove.removed())
    await state.clear()
    await database.set_chat_info(session, chat_info.export())
