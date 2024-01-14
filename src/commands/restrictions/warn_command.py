from time import time

import aiogram.exceptions
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ChatPermissions
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.commands.restrictions.warns import delwarn, check_warns
from src.utils import filters, database, ChatInfo, utils, keyboards
from src.utils.db import Warns

router = Router()
router.include_routers(
    delwarn.router,
    check_warns.router
)


@router.message(Command(commands=['warn']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_warn(
        message: Message,
        command: CommandObject,
        session: AsyncSession,
        chat_info: ChatInfo,
        i18n: I18nContext) -> Message:
    if message.from_user.id == message.reply_to_message.from_user.id:
        return await message.reply(i18n.get('command-warn-cant_warn_self'))
    if await utils.is_admin(message.reply_to_message.from_user.id, message):
        return await message.reply(i18n.get('command-warn-cant_warn_admin'))

    warn = Warns(TelegramChatID=message.chat.id,
                 TelegramUserID=message.reply_to_message.from_user.id,
                 MessageID=message.message_id)

    if command.args is not None:
        warn.Reason = command.args

    all_warns = await database.add_warn(session, warn)

    admin_name = utils.NameFormat(message.from_user)
    target_name = utils.NameFormat(message.reply_to_message.from_user)

    warn_count = len(all_warns)
    if warn_count >= chat_info.warns_count_trigger:
        await database.deactivate_warns(session, warn)
        try:
            await message.chat.restrict(
                user_id=message.reply_to_message.from_user.id,
                until_date=int(time()) + 604_800 + 1,
                permissions=ChatPermissions(
                    can_send_messages=False
                )
            )
            return await message.answer(
                text=i18n.get(
                    'command-warn-warn_limit',
                    name=target_name.get(),
                    warn_number=warn_count,
                    warn_number_limit=chat_info.warns_count_trigger,
                    warn_displa=check_warns.display_warns(all_warns, i18n)
                )
            )
        except aiogram.exceptions.TelegramBadRequest as e:
            return await message.answer(i18n.get('common-errors-cant_mute', exception=str(e)))

    await message.answer(
        text=i18n.get(
            'command-warn-warn',
            admin_name=admin_name.get(),
            name=target_name.get(),
            warn_number=warn_count,
            warn_number_limit=chat_info.warns_count_trigger,
            warn_reason=warn.Reason
        ),
        reply_markup=keyboards.delwarn_keyboard(
            i18n,
            warn.WarnID,
            warn.TelegramUserID
        )
    )
