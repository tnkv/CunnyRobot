from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from aiogram_i18n import I18nContext

from src.utils import utils, filters

router = Router()


@router.message(Command(commands=['mute', 'm']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_mute(message: Message, i18n: I18nContext) -> Message | None:
    if await utils.is_admin(message.reply_to_message.from_user.id, message):
        return await message.reply(i18n.get('command-mute-immune_user'))

    msg = message.text.split(' ')
    target_name = utils.NameFormat(message.reply_to_message.from_user)

    if len(msg) < 2:
        await message.chat.restrict(
            user_id=message.reply_to_message.from_user.id,
            until_date=0,
            permissions=ChatPermissions(can_send_messages=False))
        return await message.answer(
            i18n.get(
                'command-mute-mute', name=target_name.get()
            )
        )

    await message.chat.restrict(
        user_id=message.reply_to_message.from_user.id,
        until_date=utils.get_restriction_time(msg[1]),
        permissions=ChatPermissions(can_send_messages=False)
    )

    await message.answer(
        i18n.get(
            'command-mute-mute',
            name=target_name.get(),
            period=msg[1]
        )
    )
