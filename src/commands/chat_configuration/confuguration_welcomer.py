from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.text_decorations import html_decoration
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, keyboards, utils, ChatInfo, filters

router = Router()


class SetWelcomeText(StatesGroup):
    wait_for_welcome_text = State()
    confirm_welcome_text = State()


class SetWelcomeTime(StatesGroup):
    wait_for_time = State()


@router.callback_query(F.data == 'settings_enter_btn', filters.CallbackAdminFilter())
async def callback_enter(callback: CallbackQuery, chat_info: ChatInfo, i18n: I18nContext) -> None:
    name = utils.NameFormat(callback.from_user)
    try:
        await callback.message.edit_text(
            text=i18n.command.configuration.welcome(name=name.get()),
            reply_markup=keyboards.configuration_welcome_keyboard(i18n, chat_info)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'enter_welcome_btn', filters.CallbackAdminFilter())
async def callback_enter_welcome(callback: CallbackQuery, session: AsyncSession, chat_info: ChatInfo,
                                 i18n: I18nContext) -> None:
    chat_info.switch_welcome()
    await database.set_chat_info(session, chat_info.export())
    try:
        await callback.message.edit_reply_markup(
            callback.inline_message_id,
            reply_markup=keyboards.configuration_welcome_keyboard(i18n, chat_info)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == 'enter_editmsg_btn', filters.CallbackAdminFilter())
async def edit_welcome_msg(callback: CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    await callback.answer()
    await callback.message.answer(i18n.command.configuration.welcome.setwelcome())
    await state.set_state(SetWelcomeText.wait_for_welcome_text)


@router.message(SetWelcomeText.wait_for_welcome_text, Command(commands=['cancel']))
async def cancel_fsm(message: Message, state: FSMContext, i18n: I18nContext):
    await message.reply(i18n.common.action_canceled())
    await state.clear()


@router.message(SetWelcomeText.wait_for_welcome_text)
async def set_welcome_text(message: Message, i18n: I18nContext, state: FSMContext):
    await state.update_data(new_text=message.html_text)
    await message.reply(i18n.command.configuration.welcome.setwelcome.preview())
    name = utils.NameFormat(message.from_user)
    welcome_message_text = (
        message.html_text
        .replace("{user}", name.get())
        .replace("{user_nolink}", name.get(False))
        .replace("{user_id}", str(message.from_user.id))
        .replace("{chat_name}", message.chat.title or str(message.chat.id))
    )

    await message.answer(welcome_message_text)
    await state.set_state(SetWelcomeText.confirm_welcome_text)
    await message.answer(
        i18n.command.configuration.welcome.setwelcome.confirm(),
        reply_markup=keyboards.confirm_keyboard(i18n)
    )


@router.callback_query(SetWelcomeText.confirm_welcome_text, F.data == 'confirm')
async def confirm_welcome_text(
        callback: CallbackQuery,
        session: AsyncSession,
        i18n: I18nContext,
        state: FSMContext,
        chat_info: ChatInfo):
    fsm_data = await state.get_data()
    await callback.message.edit_text(i18n.command.configuration.welcome.setwelcome.set())
    chat_info.set_welcome_text(fsm_data.get('new_text', chat_info.welcome_message_text))
    await database.set_chat_info(session, chat_info.export())
    await state.clear()


@router.callback_query(SetWelcomeText.confirm_welcome_text, F.data == 'unconfirm')
async def unconfirm_welcome_text(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.clear()
    await callback.message.edit_text(i18n.command.configuration.welcome.setwelcome.unset())


@router.callback_query(F.data == 'enter_time_btn', filters.CallbackAdminFilter())
async def callback_welcome_time(callback: CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    await callback.answer()
    await callback.message.answer(i18n.command.configuration.welcome.settime())
    await state.set_state(SetWelcomeTime.wait_for_time)


@router.message(SetWelcomeTime.wait_for_time, Command(commands=['cancel']))
async def cancel_fsm(message: Message, state: FSMContext, i18n: I18nContext):
    await message.reply(i18n.common.action_canceled())
    await state.clear()


@router.message(SetWelcomeTime.wait_for_time)
async def set_welcome_time(message: Message, session: AsyncSession, state: FSMContext, chat_info: ChatInfo,
                           i18n: I18nContext):
    if not message.text.isdigit():
        return await message.reply(i18n.command.configuration.welcome.settime.no_number())

    seconds = int(message.text)
    if not 0 <= seconds <= 300:
        return await message.reply(html_decoration.quote(i18n.command.configuration.welcome.settime.limit()))

    chat_info.set_welcome_timeout(seconds)
    await database.set_chat_info(session, chat_info.export())

    await state.clear()
    await message.reply(i18n.command.configuration.welcome.settime.set(seconds=seconds))
