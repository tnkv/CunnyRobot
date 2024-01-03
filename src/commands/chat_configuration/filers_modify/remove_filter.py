from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, ChatInfo, filters

router = Router()


class RemoveFilter(StatesGroup):
    removable_id = State()
    confirm_removing = State()


@router.callback_query(F.data == 'filters_remove_btn', filters.CallbackAdminFilter())
async def callback_filters_remove(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Для удаления фильтра, напишите его ID\n\n'
                                  'Следующее введённое вами сообщение будет воспринято как ID фильтра, для выхода из режима удаления фильтра используй команду /cancel')
    await state.set_state(RemoveFilter.removable_id)
    await callback.answer()


@router.message(RemoveFilter.removable_id, Command('cancel'))
@router.message(RemoveFilter.confirm_removing, Command('cancel'))
async def cancel_fsm(message: Message, state: FSMContext):
    await message.reply('Действие отменено.')
    await state.clear()


@router.callback_query(RemoveFilter.confirm_removing, F.data == 'unconfirm')
async def cancel_fsm(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Действие отменено.')
    await state.clear()


@router.message(RemoveFilter.removable_id)
async def filterremove_waitid(message: Message, session: AsyncSession, state: FSMContext):
    chat_info = ChatInfo(await database.get_chat_info(session, message.chat.id))
    selected_filter = chat_info.filters_list.get(message.text)
    if selected_filter is None:
        await message.reply(f'Фильтр с ID <code>{message.text}</code> не найден, проверьте написание.')
        return

    await state.update_data(filter_id=message.text)
    await state.set_state(RemoveFilter.confirm_removing)
    await message.answer('<b>Подтвердить удаление фильтра?</b>\n'
                         'В случаее подтверждения, выбранный фильтр будет удален.\n\n'
                         f'ID: <code>{message.text}</code>\n'
                         f'Регекс: <code>{selected_filter.get("regex")}</code>\n'
                         f'Полное соответствие: <code>{"Да" if selected_filter.get("full_match", False) else "Нет"}</code>',
                         reply_markup=keyboards.confirm_keyboard())


@router.callback_query(RemoveFilter.confirm_removing, F.data == 'confirm')
async def cancel_fsm(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    chat_info = ChatInfo(await database.get_chat_info(session, callback.message.chat.id))
    data = await state.get_data()
    chat_info.remove_filter(data.get('filter_id'))
    await callback.message.edit_text('<b>Фильтр удалён</b>\n')
    await state.clear()
    await database.set_chat_info(session, chat_info.export())
