from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import (
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllChatAdministrators,
    Message
)
from aiogram_i18n import LazyProxy, I18nContext

from aiogram_i18n.types import BotCommand

import config
from src.utils import filters

router = Router()

group_commands = [
    BotCommand(command=cmd, description=LazyProxy(dscrpt))
    for cmd, dscrpt in config.GROUPS_COMMANDS.items()
]
admin_group_commands = [
    BotCommand(command=cmd, description=LazyProxy(dscrpt))
    for cmd, dscrpt in config.ADMIN_GROUP_COMMANDS.items()
]
pm_commands = [
    BotCommand(command=cmd, description=LazyProxy(dscrpt))
    for cmd, dscrpt in config.PM_COMMANDS.items()
]


@router.message(Command(commands=["setup"]), filters.SuperUserFilter())
async def startup(message: Message, bot: Bot, i18n: I18nContext):
    for language in config.LOCALES:
        i18n.locale = language
        await bot.set_my_commands(
            commands=group_commands,
            scope=BotCommandScopeAllGroupChats(),
            language_code=language
        )
        await bot.set_my_commands(
            commands=group_commands + admin_group_commands,
            scope=BotCommandScopeAllChatAdministrators(),
            language_code=language
        )
        await bot.set_my_commands(
            commands=pm_commands,
            scope=BotCommandScopeAllPrivateChats(),
            language_code=language
        )
    await message.answer(i18n.get("setup"))
