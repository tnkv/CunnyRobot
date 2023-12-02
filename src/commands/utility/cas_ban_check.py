from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.utils import utils

router = Router()


@router.message(Command(commands=['is_cas_ban']))
async def command_is_cas_ban(message: Message) -> None:
    msg = message.text.split(' ')
    if len(msg) < 2:
        await message.reply('Необходимо указать Telegram ID пользователя через пробел')
        return

    if not msg[1].isdigit():
        await message.reply('Некорректный Telegram ID')
        return

    await message.reply(f'Статус блокировки в CAS: {await utils.is_cas_ban(int(msg[1]))}')
