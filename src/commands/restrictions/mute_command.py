from time import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from aiogram_i18n import I18nContext

from src.utils import utils, filters

router = Router()


@router.message(Command(commands=['mute', 'm']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_mute(message: Message, i18n: I18nContext) -> Message | None:
    if (await utils.is_admin(message.reply_to_message.from_user.id, message.chat)
            or message.reply_to_message.sender_chat):
        return await message.reply(i18n.get('command-mute-immune_user'))

    msg = message.text.split(' ', 2)
    target_name = utils.NameFormat(message.reply_to_message.from_user)

    if len(msg) < 2:
        await message.chat.restrict(
            user_id=message.reply_to_message.from_user.id,
            until_date=0,
            permissions=ChatPermissions(can_send_messages=False))
        return await message.bot.send_message(
            chat_id=message.chat.id,
            text=i18n.get(
                'command-mute-mute', name=target_name.get()
            ),
            reply_to_message_id=message.reply_to_message.message_id
        )
    restriction_period = utils.get_restriction_time(msg[1])

    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        until_date=int(time()) + restriction_period + 1,
        permissions=ChatPermissions(can_send_messages=False)
    )

    if restriction_period != 0 and len(msg) >= 3:
        answ = i18n.get(
            'command-mute-tempmute-reason',
            name=target_name.get(),
            period=msg[1],
            reason=msg[2]
        )
    elif restriction_period != 0:
        answ = i18n.get(
            'command-mute-tempmute',
            name=target_name.get(),
            period=msg[1]
        )
    else:
        answ = i18n.get(
            'command-mute-mute-reason',
            name=target_name.get(),
            reason=' '.join(msg[1:], )
        )

    await message.bot.send_message(
        chat_id=message.chat.id,
        text=answ,
        reply_to_message_id=message.reply_to_message.message_id
    )
