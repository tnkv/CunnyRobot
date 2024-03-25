from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.utils import utils

router = Router()


@router.message(Command(commands=['is_cas_ban']))
async def command_is_cas_ban(message: Message, i18n: I18nContext) -> None:
    msg = message.text.split(' ')

    if len(msg) < 2:
        await message.reply(i18n.cas.is_cas_ban.need_telegram_id())
        return

    if not msg[1].isdigit():
        await message.reply(i18n.cas.is_cas_ban.incorrect_telegram_id())
        return

    await message.reply(i18n.test.number(count=int(msg[1])))

    cas_ban_status = await utils.is_cas_ban(int(msg[1]))

    await message.reply(
        text=i18n.cas.is_cas_ban(
            status=i18n.cas.status(
                status=cas_ban_status
            ),
            user_id=msg[1]
        )
    )
