import re

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import html_decoration
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, ChatInfo, filters

router = Router()


class AddFilter(StatesGroup):
    filter_regex = State()
    filter_fullmatch = State()
    filter_confirm = State()


@router.callback_query(F.data == 'filters_add_btn', filters.CallbackAdminFilter())
async def callback_filters_add(callback: CallbackQuery, i18n: I18nContext, state: FSMContext) -> None:
    await callback.message.answer(i18n.command.configuration.filters.addfilter())
    await state.set_state(AddFilter.filter_regex)
    await callback.answer()


@router.message(AddFilter.filter_regex, Command('cancel'))
@router.message(AddFilter.filter_fullmatch, Command('cancel'))
@router.message(AddFilter.filter_confirm, Command('cancel'))
async def cancel_fsm(message: Message, state: FSMContext, i18n: I18nContext):
    await message.reply(i18n.common.action_canceled())
    await state.clear()


@router.callback_query(AddFilter.filter_confirm, F.data == 'unconfirm')
async def cancel_callback_fsm(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.answer()
    await callback.message.edit_text(i18n.common.action_canceled())
    await state.clear()


@router.message(AddFilter.filter_regex)
async def filteradd_waitregex(message: Message, i18n: I18nContext, state: FSMContext):
    try:
        re.compile(message.text)
        await state.update_data(regex=message.text)
        await state.set_state(AddFilter.filter_fullmatch)
        await message.reply(
            text=i18n.command.configuration.filters.fullmatch(
                regex=html_decoration.quote(message.text)
            ),
            reply_markup=keyboards.confirm_keyboard(i18n)
        )
    except re.error:
        await message.reply(
            i18n.command.configuration.filters.regex_error(
                regex=html_decoration.quote(message.text)
            )
        )


@router.callback_query(AddFilter.filter_fullmatch, F.data == 'confirm')
async def filteradd_fullmatch(callback: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await callback.answer()
    data = await state.update_data(full_match=True)
    await state.set_state(AddFilter.filter_confirm)
    await callback.message.edit_text(
        text=i18n.command.configuration.filters.confirmation(
            regex=html_decoration.quote(
                data.get("regex", "Default String")
            ),
            full_match=True
        ),
        reply_markup=keyboards.confirm_keyboard(i18n))


@router.callback_query(AddFilter.filter_fullmatch, F.data == 'unconfirm')
async def filteradd_fullmatch_no(callback: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await callback.answer()
    data = await state.update_data(full_match=False)
    await state.set_state(AddFilter.filter_confirm)
    await callback.message.edit_text(
        text=i18n.command.configuration.filters.confirmation(
            regex=html_decoration.quote(
                data.get("regex", "Default String")
            ),
            full_match=False
        ),
        reply_markup=keyboards.confirm_keyboard(i18n))


@router.callback_query(AddFilter.filter_confirm, F.data == 'confirm')
async def filteradd_added(callback: CallbackQuery, session: AsyncSession, chat_info: ChatInfo, state: FSMContext,
                          i18n: I18nContext):
    data = await state.get_data()
    await callback.message.edit_text(
        text=i18n.command.configuration.filters.added(
            regex=html_decoration.quote(
                data.get("regex", "Default String")
            )
        )
    )
    chat_info.add_filter(
        regex=data.get("regex"),
        full_match=data.get("full_match")
    )
    await database.set_chat_info(session, chat_info.export())
