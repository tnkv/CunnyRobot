import re

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import html_decoration
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, ChatInfo, filters

router = Router()


class AddFilter(StatesGroup):
    filter_regex = State()
    filter_fullmatch = State()
    filter_confirm = State()


@router.callback_query(F.data == 'filters_add_btn', filters.CallbackAdminFilter())
async def callback_filters_add(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Для добавления нового фильтра, напишите его regex\n\n'
                                  'Следующее введённое вами сообщение будет воспринято как фильтр, для выхода из режима добавления фильтра используй команду /cancel')
    await state.set_state(AddFilter.filter_regex)
    await callback.answer()


@router.message(AddFilter.filter_regex, Command('cancel'))
@router.message(AddFilter.filter_fullmatch, Command('cancel'))
@router.message(AddFilter.filter_confirm, Command('cancel'))
async def cancel_fsm(message: Message, state: FSMContext):
    await message.reply('Действие отменено.')
    await state.clear()


@router.callback_query(AddFilter.filter_confirm, F.data == 'unconfirm')
async def cancel_callback_fsm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Действие отменено.')
    await state.clear()


@router.message(AddFilter.filter_regex)
async def filteradd_waitregex(message: Message, state: FSMContext):
    try:
        re.compile(message.text)
        await state.update_data(regex=message.text)
        await state.set_state(AddFilter.filter_fullmatch)
        await message.reply(
            text=f'Должен ли фильтр <code>{html_decoration.quote(message.text)}</code> требовать точное совпадение сообщения?',
            reply_markup=keyboards.confirm_keyboard())
    except re.error:
        await message.reply(f'Указанный Regex ({message.text}) не является валидным, проверьте написание.\n\n'
                            'Следующее введённое вами сообщение будет воспринято как фильтр, для выхода из режима добавления фильтра используй команду /cancel')


@router.callback_query(AddFilter.filter_fullmatch, F.data == 'confirm')
async def filteradd_fullmatch(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.update_data(full_match=True)
    await state.set_state(AddFilter.filter_confirm)
    await callback.message.edit_text(
        text=f'Подтвердить добавление фильтра?\n\n'
             f'Регекс: <code>{data.get("regex", "Default String")}</code>\n'
             'Полное соответствие: Да',
        reply_markup=keyboards.confirm_keyboard())


@router.callback_query(AddFilter.filter_fullmatch, F.data == 'unconfirm')
async def filteradd_fullmatch_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.update_data(full_match=False)
    await state.set_state(AddFilter.filter_confirm)
    await callback.message.edit_text(
        text=f'Подтвердить добавление фильтра?\n\n'
             f'Регекс: <code>{data.get("regex", "Default String")}</code>\n'
             'Полное соответствие: Нет',
        reply_markup=keyboards.confirm_keyboard())


@router.callback_query(AddFilter.filter_confirm, F.data == 'confirm')
async def filteradd_added(callback: CallbackQuery, session: AsyncSession, chat_info: ChatInfo, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(
        text=f'Фильтр <code>{data.get("regex", "Default String")}</code> добавлен!\n'
             'Сообщения от пользователей с правами администратора удаляться не будут.')
    chat_info.add_filter(regex=data.get("regex"),
                         full_match=data.get("full_match"))
    await database.set_chat_info(session, chat_info.export())
