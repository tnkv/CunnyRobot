from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.utils.CaptchaCallbackFactory import CaptchaCallbackFactory


def cancel_tribunal_keyboard(time: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=f"Осталось {time} сек.",
        callback_data="cancel_tribunal")
    )
    return builder.as_markup()


def ended_tribunal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Трибунал завершён.",
        callback_data="ended_tribunal")
    )
    return builder.as_markup()


def canceled_tribunal_keyboard(admin: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=f"Трибунал отменён. ({admin})",
        callback_data="canceled_tribunal")
    )
    return builder.as_markup()


def captcha_keyboard(date: int, TelegramUserID: int, TelegramChatID: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Я не бот", callback_data=CaptchaCallbackFactory(date=date, user=TelegramUserID, chat=TelegramChatID)
    )
    return builder.as_markup()
