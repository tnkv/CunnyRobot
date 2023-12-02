from time import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from src.utils.filters import admin_filter, reply_filter

router = Router()

TIME_COEFFICIENT = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}


@router.message(Command(commands=['mute', 'm']), admin_filter.AdminFilter(), reply_filter.NeedReplyFilter())
async def command_mute(message: Message) -> None:
    msg = message.text.split(' ')
    if len(msg) < 2:
        await message.chat.restrict(user_id=message.reply_to_message.from_user.id,
                                    until_date=0,
                                    permissions=ChatPermissions(can_send_messages=False))
        return

    await message.chat.restrict(user_id=message.reply_to_message.from_user.id,
                                until_date=get_restriction_time(msg[1]),
                                permissions=ChatPermissions(can_send_messages=False))


def get_restriction_time(duration: str) -> int:
    unit = duration[-1]
    value = int(duration[:-1]) if duration[:-1].isdigit() else 0
    return int(time()) + value * TIME_COEFFICIENT.get(unit, 0)
