from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

import config
from src.utils import ChatInfo
from src.utils.callback_factory import CaptchaCallbackFactory, DelwarnCallbackFactory, SetLangFactory


def cancel_tribunal_keyboard(i18n: I18nContext, time: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.keyboards.tribunal.timbebutton(time=time),
        callback_data='cancel_tribunal'
    )

    return builder.as_markup()


def ended_tribunal_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.keyboards.tribunal.eol(),
        callback_data='ended_tribunal'
    )

    return builder.as_markup()


def canceled_tribunal_keyboard(i18n: I18nContext, admin: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.keyboards.tribunal.canceled(admin=admin),
        callback_data='canceled_tribunal'
    )

    return builder.as_markup()


def captcha_keyboard(i18n: I18nContext, date: int, telegram_user_id: int,
                     telegram_chat_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.keyboards.welcomer.captcha(),
        callback_data=CaptchaCallbackFactory(
            date=date,
            user=telegram_user_id,
            chat=telegram_chat_id
        )
    )

    return builder.as_markup()


def delwarn_keyboard(i18n: I18nContext, warn_id: int, user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.keyboards.warn.delwarn(),
        callback_data=DelwarnCallbackFactory(
            warn_id=warn_id,
            user_id=user_id
        )
    )

    return builder.as_markup()


def configuration_main_keyboard(i18n: I18nContext, chat_info: ChatInfo) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.keyboards.configuration.main.comment_mode(state=chat_info.is_comments),
                   callback_data='comments_settings_btn')
    builder.button(text=i18n.keyboards.configuration.main.enter(), callback_data='settings_enter_btn')
    builder.button(text=i18n.keyboards.configuration.main.members(), callback_data='settings_members_btn')
    builder.button(text=i18n.keyboards.configuration.main.filters(), callback_data='settings_filters_btn')
    builder.adjust(1)

    return builder.as_markup()


def configuration_welcome_keyboard(i18n: I18nContext, chat_info: ChatInfo) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.keyboards.configuration.welcome.state(state=chat_info.welcome_message),
                   callback_data='enter_welcome_btn')
    builder.button(text=i18n.keyboards.configuration.welcome.editmsg(), callback_data='enter_editmsg_btn')
    builder.button(text=i18n.keyboards.configuration.welcome.edittime(), callback_data='enter_time_btn')
    builder.button(text=i18n.keyboards.configuration.main_menu(), callback_data='settings_main_btn')
    builder.adjust(1)

    return builder.as_markup()


def configuration_filter_keyboard(i18n: I18nContext, chat_info: ChatInfo) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.keyboards.configuration.filter.state(state=chat_info.filters_enabled),
                   callback_data='filters_switch_btn')
    builder.button(text=i18n.keyboards.configuration.filter.list(count=len(chat_info.filters_list)),
                   callback_data='filters_list_btn')
    builder.button(text=i18n.keyboards.configuration.filter.add(), callback_data='filters_add_btn')
    builder.button(text=i18n.keyboards.configuration.main_menu(), callback_data='settings_main_btn')
    builder.adjust(1)

    return builder.as_markup()


def configuration_filter_list_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.keyboards.configuration.filter.remove(), callback_data='filters_remove_btn')
    builder.button(text=i18n.keyboards.configuration.filter.add(), callback_data='filters_add_btn')
    builder.button(text=i18n.keyboards.configuration.back(), callback_data='settings_filters_btn')
    builder.button(text=i18n.keyboards.configuration.main_menu(), callback_data='settings_main_btn')
    builder.adjust(2)

    return builder.as_markup()


def configuration_members_keyboard(i18n: I18nContext, chat_info: ChatInfo) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.keyboards.configuration.members.lang(
            lang=chat_info.chat_language
        ),
        callback_data='settings_members_setlang'
    )
    builder.button(
        text=i18n.keyboards.configuration.main_menu(),
        callback_data='settings_main_btn'
    )
    builder.adjust(1)

    return builder.as_markup()


def configuration_members_lang_keyboard(i18n: I18nContext, chat_info: ChatInfo) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lang in config.LOCALES:
        if lang == chat_info.chat_language:
            builder.button(text=f'{lang} ✅', callback_data=lang)
            continue
        builder.button(text=lang, callback_data=SetLangFactory(lang=lang))
    builder.button(text=i18n.keyboards.configuration.back(), callback_data='settings_members_btn')
    builder.button(text=i18n.keyboards.configuration.main_menu(), callback_data='settings_main_btn')
    builder.adjust(2)
    return builder.as_markup()


def confirm_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.keyboards.confirm.yes(), callback_data='confirm')
    builder.button(text=i18n.keyboards.confirm.no(), callback_data='unconfirm')

    return builder.as_markup()


def add_to_chat_keyboard(i18n: I18nContext, bot_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.keyboards.add_to_chat(), url=f'https://t.me/{bot_username}?startgroup=start')

    return builder.as_markup()
