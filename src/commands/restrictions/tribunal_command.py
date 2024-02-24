import asyncio
from time import time

from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions, CallbackQuery
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.utils import keyboards, database, utils, ChatInfo, filters

router = Router()


# Трибунал
@router.message(Command('tribunal', 'votemute'))
async def command_tribunal(
        message: Message,
        session: AsyncSession,
        session_pool: async_sessionmaker,
        chat_info: ChatInfo,
        i18n: I18nContext) -> Message | None:
    if not message.reply_to_message:  # Проверка что ответ на сообщение
        return await message.reply(i18n.get('command-tribunal-need_reply'))

    if message.from_user.id == message.reply_to_message.from_user.id:  # Проверка что не ответ на свое сообщение
        return await message.reply(i18n.get('command-tribunal-cant_self'))

    target_id = message.reply_to_message.from_user.id
    target = await message.chat.get_member(user_id=target_id)
    name = utils.NameFormat(message.reply_to_message.from_user)

    if (target.status in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)
            or target_id in chat_info.tribunal_immunity):  # Проверка что у пользователя нет иммунитета
        return await message.reply(i18n.get('command-tribunal-user_immune'))

    if target.status in (ChatMemberStatus.RESTRICTED,) and not target.can_send_messages:  # Вдруг юзер уже в муте/бане
        return await message.reply(i18n.get('command-tribunal-user_already_restricted'))

    tribunal_timeout = chat_info.last_tribunal_end
    current_time = int(time())

    if tribunal_timeout >= current_time:  # Проверка что таймаут прошел
        if tribunal_timeout - 90 >= current_time:
            return await message.reply(
                i18n.get('command-tribunal-timeout-active', time=str(tribunal_timeout - current_time))
            )

        return await message.reply(
            i18n.get('command-tribunal-timeout', time=str(tribunal_timeout - current_time))
        )

    end_time = current_time + 90
    timer = current_time
    chat_info.set_tribunal_timeout(end_time + 90)
    await database.set_chat_info(session, chat_info.export())

    msg = await message.bot.send_poll(
        chat_id=message.chat.id,
        reply_to_message_id=message.reply_to_message.message_id,
        question=i18n.get('command-tribunal-poll_title', name=name.get(False)),
        options=[
            i18n.get('command-tribunal-poll_option-yes'),
            i18n.get('command-tribunal-poll_option-no')
        ],
        is_anonymous=False,
        reply_markup=keyboards.cancel_tribunal_keyboard(i18n, end_time - int(time()))
    )

    while time() < end_time:
        timer += 5
        await asyncio.sleep(min(timer - time(), end_time - time()))
        async with session_pool() as temp_session:
            if (await database.get_chat_info(temp_session, message.chat.id)).LastTribunalEnd < time():
                return  # Проверка что трибунал не был отменён администратором
        try:
            await msg.edit_reply_markup(reply_markup=keyboards.cancel_tribunal_keyboard(i18n, end_time - int(time())))
        except TelegramBadRequest:
            continue

    poll = await message.bot.stop_poll(
        chat_id=message.chat.id,
        message_id=msg.message_id,
        reply_markup=keyboards.ended_tribunal_keyboard(i18n)
    )

    if poll.total_voter_count < 3:
        return await message.answer(
            i18n.get('command-tribunal-insufficient_votes', name=name.get())
        )

    votes = {option.text: option.voter_count for option in poll.options}
    mute_votes = int(
        votes[i18n.get('command-tribunal-poll_option-yes')] * 100 / poll.total_voter_count)  # Подсчет процента "за"

    if mute_votes < 66:
        return await message.answer(
            i18n.get(
                'command-tribunal-insufficient_yesvotes',
                name=name.get(),
                mute_votes_percent=mute_votes
            )
        )

    tribunalizable = await message.chat.get_member(
        user_id=message.reply_to_message.from_user.id)  # Обновляю инфу окончательно, а то пока был трибунал его могли замутить
    if tribunalizable.status in (ChatMemberStatus.RESTRICTED,) and not tribunalizable.can_send_messages:
        await message.reply(i18n.get('command-tribunal-another_restriction'))
        return
    try:
        mute_period = ((votes[i18n.get('command-tribunal-poll_option-yes')] * 2)
                       - votes[i18n.get('command-tribunal-poll_option-no')])

        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            until_date=(int(time()) + mute_period * 60),
            permissions=ChatPermissions(can_send_messages=False)
        )

        await message.answer(
            i18n.get(
                'command-tribunal-finish',
                name=name.get(),
                mute_votes_percent=mute_votes,
                mute_period=mute_period
            )
        )
    except Exception as e:
        await message.answer(i18n.get('common-errors-cant_mute', exception=str(e)))


# Обработка отмены трибунала
@router.callback_query(F.data == 'cancel_tribunal', filters.CallbackAdminFilter(False))
async def callback_cancel_tribunal(
        callback: CallbackQuery,
        session: AsyncSession,
        chat_info: ChatInfo,
        i18n: I18nContext) -> None:
    chat_info.set_tribunal_timeout(int(time()))
    await database.set_chat_info(session, chat_info.export())
    try:
        name = utils.NameFormat(callback.from_user)
        await callback.bot.stop_poll(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=keyboards.canceled_tribunal_keyboard(i18n, name.get(False))
        )
    except Exception as e:
        await callback.answer(i18n.get('common-errors-global', exception=str(e)))
