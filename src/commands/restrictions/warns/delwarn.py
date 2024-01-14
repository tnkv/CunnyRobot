from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, filters, utils
from src.utils.callback_factory import DelwarnCallbackFactory
from src.utils.db import Warns

router = Router()


@router.callback_query(DelwarnCallbackFactory.filter(), filters.CallbackAdminFilter())
async def callback_delwarn(
        callback: CallbackQuery,
        callback_data: DelwarnCallbackFactory,
        session: AsyncSession,
        i18n: I18nContext) -> None:
    deleted_warn = Warns(
        WarnID=callback_data.warn_id,
        TelegramUserID=callback_data.user_id,
        IsActive=False
    )

    await callback.message.edit_text(i18n.get('callback-delwarn-delwarn', user=callback_data.user_id))
    await database.set_chat_info(session, deleted_warn)


@router.message(Command(commands=['delwarn', 'delwarns', 'dewarn', 'dewarns', 'unwarn']),
                filters.AdminFilter(),
                filters.NeedReplyFilter())
async def command_delwarn(message: Message, session: AsyncSession, i18n: I18nContext):
    warns = await database.get_warns(
        session,
        message.chat.id,
        message.reply_to_message.from_user.id
    )
    target_name = utils.NameFormat(message.reply_to_message.from_user)

    if not warns:
        return await message.reply(text=i18n.get('command-warn-check-nowarns', name=target_name.get()))

    warn: Warns = warns[-1]
    warn.IsActive = False
    await database.set_chat_info(session, warn)

    link_to_warn = f'<a href="https://t.me/c/{str(warn.TelegramChatID)[4:]}/{warn.MessageID}">{warn.Reason if warn.Reason else i18n.get("command-warn-display-noreason")}</a>'

    await message.reply(
        i18n.get(
            'command-delwarn-delwarn',
            name=target_name.get(),
            warn_link=link_to_warn,
            warn_count=str(len(warns) - 1)
        )
    )
