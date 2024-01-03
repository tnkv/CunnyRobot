from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, utils, ChatInfo, filters

router = Router()


class SetWelcomeText(StatesGroup):
    wait_for_welcome_text = State()
    confirm_welcome_text = State()


class SetWelcomeTime(StatesGroup):
    wait_for_time = State()


@router.callback_query(F.data == 'settings_enter_btn', filters.CallbackAdminFilter())
async def callback_enter(callback: CallbackQuery, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, callback.message.chat.id))
    name = utils.name_format(callback.from_user.id,
                             callback.from_user.username,
                             callback.from_user.first_name,
                             callback.from_user.last_name)
    try:
        await callback.message.edit_text(text='<b>Конфигурация чата</b>\n'
                                              f'<b>Настройки входа</b>\n\n'
                                              f'{name}, используй кнопки ниже для управление чатом.',
                                         reply_markup=keyboards.configuration_welcome_keyboard(chat_info))
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'enter_welcome_btn', filters.CallbackAdminFilter())
async def callback_enter_welcome(callback: CallbackQuery, session: AsyncSession) -> None:
    chat_info = ChatInfo(await database.get_chat_info(session, callback.message.chat.id))
    chat_info.switch_welcome()
    await database.set_chat_info(session, chat_info.export())
    try:
        await callback.message.edit_reply_markup(callback.inline_message_id,
                                                 reply_markup=keyboards.configuration_welcome_keyboard(chat_info))
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'enter_editmsg_btn', filters.CallbackAdminFilter())
async def edit_welcome_msg(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Для установки нового приветствия напишите его в следующем сообщении.\n\n'
                                  'Для упоминания пользователя добавь <code>{user}</code> в тексте.\n'
                                  'Для форматирования текста используй возможности в клиенте.\n\n'
                                  'Следующее ввёденное вами сообщение станет приветствием в этом чате, для выхода из режима редактирования выполни команду /cancel')
    await state.set_state(SetWelcomeText.wait_for_welcome_text)


@router.message(SetWelcomeText.wait_for_welcome_text, Command(commands=['cancel']))
async def cancel_fsm(message: Message, state: FSMContext):
    await message.reply('Действие отменено.')
    await state.clear()


@router.message(SetWelcomeText.wait_for_welcome_text)
async def set_welcome_text(message: Message, state: FSMContext):
    await state.update_data(new_text=message.html_text)
    await message.reply('Теперь все новые участники будут получать следующее сообщение в качестве приветствия:')
    name = utils.name_format(message.from_user.id,
                             message.from_user.username,
                             message.from_user.first_name,
                             message.from_user.last_name)
    welcome_message_text = message.html_text.format(user=name) if '{user}' in message.html_text else message.html_text
    await message.answer(welcome_message_text)
    await state.set_state(SetWelcomeText.confirm_welcome_text)
    await message.answer('Подтвердить изменение?', reply_markup=keyboards.confirm_keyboard())


@router.callback_query(SetWelcomeText.confirm_welcome_text, F.data == 'confirm')
async def confirm_welcome_text(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    chat_info = ChatInfo(await database.get_chat_info(session, callback.message.chat.id))
    fsm_data = await state.get_data()
    await callback.message.edit_text('Новое приветствие установлено.')
    chat_info.set_welcome_text(fsm_data.get('new_text', chat_info.welcome_message_text))
    await database.set_chat_info(session, chat_info.export())
    await state.clear()


@router.callback_query(SetWelcomeText.confirm_welcome_text, F.data == 'unconfirm')
async def unconfirm_welcome_text(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Новое приветствие не будет установлено.')


@router.callback_query(F.data == 'enter_time_btn', filters.CallbackAdminFilter())
async def callback_welcome_time(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        'Напиши количество секунд (0-300), которое потребуется подождать новому участнику, перед тем как получить возможность снять мут.\n\n'
        'Для выхода из режима редактирования испольуй /cancel')
    await state.set_state(SetWelcomeTime.wait_for_time)


@router.message(SetWelcomeTime.wait_for_time, Command(commands=['cancel']))
async def cancel_fsm(message: Message, state: FSMContext):
    await message.reply('Действие отменено.')
    await state.clear()


@router.message(SetWelcomeTime.wait_for_time)
async def set_welcome_time(message: Message, session: AsyncSession, state: FSMContext):
    if not message.text.isdigit():
        await message.reply('Это не похоже на целое число, попробуй ещё раз.')
        return

    seconds = int(message.text)
    if not 0 <= seconds <= 300:
        await message.reply('Количество секунд должно удовлетворять условие "0 <= time <= 300"')
        return

    chat_info = ChatInfo(await database.get_chat_info(session, message.chat.id))
    chat_info.set_welcome_timeout(seconds)
    await database.set_chat_info(session, chat_info.export())

    await state.clear()
    await message.reply(
        f'Теперь новым учасникам придётся ждать {utils.inflect_with_num(seconds, ("секунду", "секунд", "секунды"))} для разблокировки кнопки анмута.')
