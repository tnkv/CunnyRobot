from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, filters
from src.utils.callback_factory import DelwarnCallbackFactory
from src.utils.db import Warns

router = Router()


@router.callback_query(DelwarnCallbackFactory.filter(), filters.CallbackAdminFilter())
async def callback_delwarn(callback: CallbackQuery, callback_data: DelwarnCallbackFactory,
                           session: AsyncSession) -> None:
    deleted_warn = Warns(
        WarnID=callback_data.warn_id,
        TelegramUserID=callback_data.user_id,
        IsActive=False
    )

    await callback.message.edit_text(f'Предупреждение для пользователя <code>{callback_data.user_id}</code> удалено.')
    await database.set_chat_info(session, deleted_warn)


@router.message(Command(commands=['delwarn', 'delwarns']), filters.AdminFilter(), filters.NeedReplyFilter())
async def command_delwarn(message: Message, session: AsyncSession):
    warns = await database.get_one_warn(
        session,
        message.chat.id,
        message.reply_to_message.from_user.id
    )
    if not warns:
        return await message.reply('У пользоваетеля нет предупреждений.')

    warn: Warns = warns[0]
    warn.IsActive = False
    await database.set_chat_info(session, warn)

    link_to_warn = f'<a href="https://t.me/c/{str(warn.TelegramChatID)[4:]}/{warn.MessageID}">{warn.Reason if warn.Reason else "Без причины."}</a>'
    await message.reply(f'Предупреждение для пользователя <code>{warn.TelegramUserID}</code> было удалено.\n\n'
                        f'Удалённое предупреждение:\n'
                        f'{link_to_warn}\n\n'
                        f'У пользователя осталось {len(warns) - 1} предупреждений')


