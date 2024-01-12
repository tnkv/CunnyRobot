from time import time

import aiogram.exceptions
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ChatPermissions
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
async def command_warn(message: Message, command: CommandObject, session: AsyncSession, chat_info: ChatInfo) -> Message:
    if message.from_user.id == message.reply_to_message.from_user.id:
        return await message.reply('Не могу выдать предупреждение тебе, зачем ты варнишь самого себя.')
    if await utils.is_admin(message.reply_to_message.from_user.id, message):
        return await message.reply('Не могу выдать предупреждение администратору.')

    warn = Warns(TelegramChatID=message.chat.id,
                 TelegramUserID=message.reply_to_message.from_user.id,
                 MessageID=message.message_id)

    if command.args is not None:
        warn.Reason = command.args

    all_warns = await database.add_warn(session, warn)

    admin_name = utils.name_format(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )

    target_name = utils.name_format(
        message.reply_to_message.from_user.id,
        message.reply_to_message.from_user.username,
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name
    )

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
            msg = (f'Пользователь {target_name} получил {warn_count}/{chat_info.warns_count_trigger} предупреждений. '
                   'В качестве наказания был выдан мут на 1 неделю.\n\n'
                   f'{check_warns.display_warns(all_warns)}')
            return await message.answer(msg)
        except aiogram.exceptions.TelegramBadRequest as e:
            return await message.answer(f'Не получилось замутить пользователя.\n\nОшибка: <code>{e}</code>')

    msg = (f'Администратор {admin_name} выдал предупреждение {target_name}\n\n'
           f'Теперь пользователь имеет {warn_count}/{chat_info.warns_count_trigger} предупреждений.\n'
           f'Причина: {warn.Reason}\n'
           f'В случае достижения лимита, пользователь получит мут на 1 неделю.')

    await message.answer(
        text=msg,
        reply_markup=keyboards.delwarn_keyboard(
            warn.WarnID,
            warn.TelegramUserID
        )
    )
