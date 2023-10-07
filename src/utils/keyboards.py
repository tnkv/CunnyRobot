from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils import ChatInfo
from src.utils.CaptchaCallbackFactory import CaptchaCallbackFactory


def cancel_tribunal_keyboard(time: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=f'Осталось {time} сек.',
        callback_data='cancel_tribunal')
    )

    return builder.as_markup()


def ended_tribunal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Трибунал завершён.',
        callback_data='ended_tribunal')
    )

    return builder.as_markup()


def canceled_tribunal_keyboard(admin: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=f'Трибунал отменён. ({admin})',
        callback_data='canceled_tribunal')
    )

    return builder.as_markup()


def captcha_keyboard(date: int, telegram_user_id: int, telegram_chat_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Я не бот', callback_data=CaptchaCallbackFactory(date=date, user=telegram_user_id, chat=telegram_chat_id)
    )

    return builder.as_markup()


def configuration_main_keyboard(chat_info: ChatInfo) -> InlineKeyboardMarkup:  # TODO: Доделать пункты меню
    builder = InlineKeyboardBuilder()
    builder.button(text=f'Режим комментариев: {"включён" if chat_info.is_comments else "выключен"}',
                   callback_data='comments_settings_btn')
    builder.button(text=f'Настройки входа', callback_data='settings_enter_btn')
    #    builder.button(text=f'Пользователи', callback_data='settings_members_btn')
    #    builder.button(text=f'Фильтры', callback_data='settings_filters_btn')
    builder.adjust(1)

    return builder.as_markup()


def configuration_welcome_keyboard(chat_info: ChatInfo) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f'Приветствие: {"включено" if chat_info.welcome_message else "выключено"}',
                   callback_data='enter_welcome_btn')
    builder.button(text=f'Изменить сообщение', callback_data='enter_editmsg_btn')
    builder.button(text=f'Настроить время', callback_data='enter_time_btn')
    builder.button(text=f'Главное меню', callback_data='settings_main_btn')
    builder.adjust(1)

    return builder.as_markup()

def confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Да', callback_data='confirm')
    builder.button(text='Нет', callback_data='unconfirm')

    return builder.as_markup()
