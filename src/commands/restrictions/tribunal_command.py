import asyncio
from time import time

from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import keyboards, database, utils, ChatInfo, filters

router = Router()


# Трибунал
@router.message(Command('tribunal'))
async def command_tribunal(message: Message, session: AsyncSession, chat_info: ChatInfo) -> None:
    if not message.reply_to_message:  # Проверка что ответ на сообщение
        await message.reply(
            'Команду /tribunal надо писать в ответ на сообщение человека, за ссылку в гулаг которого вы хотите начать голосование')
        return

    if message.from_user.id == message.reply_to_message.from_user.id:  # Проверка что не ответ на свое сообщение
        await message.reply('Нельзя начать трибунал против себя.')
        return

    target_id = message.reply_to_message.from_user.id
    target = await message.chat.get_member(user_id=target_id)
    name = utils.name_format(message.reply_to_message.from_user.id,
                             message.reply_to_message.from_user.username,
                             message.reply_to_message.from_user.first_name,
                             message.reply_to_message.from_user.last_name)

    if target.status in (ChatMemberStatus.CREATOR,
                         ChatMemberStatus.ADMINISTRATOR) or target_id in chat_info.tribunal_immunity:  # Проверка что у пользователя нет иммунитета
        await message.reply('У пользователя иммунитет от трибунала')
        return

    if target.status in (ChatMemberStatus.RESTRICTED,) and not target.can_send_messages:  # Вдруг юзер уже в муте/бане
        await message.reply('Невозможно начать трибунал, пользователь уже ограничен.')
        return

    tribunal_timeout = chat_info.last_tribunal_end
    current_time = int(time())

    if tribunal_timeout >= current_time:  # Проверка что таймаут прошел
        if tribunal_timeout - 90 >= current_time:
            await message.reply(
                f'В чате есть активный трибунал, перед началом нового подождите {tribunal_timeout - current_time} секунд.')
            return
        await message.reply(f'Перед началом нового трибунала, подождите {tribunal_timeout - current_time} секунд.')
        return

    end_time = current_time + 90
    timer = current_time
    chat_info.set_tribunal_timeout(end_time + 90)
    await database.set_chat_info(session, chat_info.export())

    msg = await message.bot.send_poll(chat_id=message.chat.id,
                                      reply_to_message_id=message.reply_to_message.message_id,
                                      question=f'''Трибунал ({utils.name_format(message.reply_to_message.from_user.id,
                                                                                message.reply_to_message.from_user.username,
                                                                                message.reply_to_message.from_user.first_name,
                                                                                message.reply_to_message.from_user.last_name,
                                                                                False)})''',
                                      options=['За', 'Против'],
                                      is_anonymous=False,
                                      reply_markup=keyboards.cancel_tribunal_keyboard(end_time - int(time())))
    while time() < end_time:
        timer += 5
        await asyncio.sleep(min(timer - time(), end_time - time()))
        if ChatInfo(await database.get_chat_info(session, message.chat.id)).last_tribunal_end < time():
            return  # Проверка что трибунал не был отменён администратором

        await msg.edit_reply_markup(reply_markup=keyboards.cancel_tribunal_keyboard(end_time - int(time())))

    poll = await message.bot.stop_poll(chat_id=message.chat.id,
                                       message_id=msg.message_id,
                                       reply_markup=keyboards.ended_tribunal_keyboard())

    if poll.total_voter_count < 3:
        await message.answer(
            f'В голосовании за ссылку {name} приняло слишком мало людей. Минимальное общее количество голосов для признания голосования легитимным - 3')
        return

    votes = {option.text: option.voter_count for option in poll.options}
    muteVotes = int(votes['За'] * 100 / poll.total_voter_count)  # Подсчет процента "за"

    if muteVotes < 66:
        await message.answer(
            f'Голосование за мут {name} закончилось с {muteVotes}% голосов за, но для мута требуется хотя бы 66%, пользователь не будет замучен.')
        return
    tribunalizable = await message.chat.get_member(
        user_id=message.reply_to_message.from_user.id)  # Обновляю инфу окончательно, а то пока был трибунал его могли замутить
    if tribunalizable.status in (ChatMemberStatus.RESTRICTED,) and not tribunalizable.can_send_messages:
        await message.reply('Трибунал завершён, но во время ожидания пользователь получил другое наказание.')
        return
    try:
        mute_period = (votes["За"] * 2) - votes["Против"]
        mute_period_inflected = utils.inflect_with_num(mute_period, ('минуту', 'минут', 'минуты'))
        await message.bot.restrict_chat_member(chat_id=message.chat.id,
                                               user_id=message.reply_to_message.from_user.id,
                                               until_date=(int(time()) + mute_period * 60),
                                               permissions=ChatPermissions(can_send_messages=False))
        await message.answer(
            f'Голосование за мут {name} закончилось с {muteVotes}% голосов за, пользователь отправляется в мут на {mute_period_inflected}.')
    except Exception as e:
        await message.answer(f'Не получилось замутить пользователя.\n\nОшибка: <code>{e}</code>')


# Обработка отмены трибунала
@router.callback_query(F.data == 'cancel_tribunal', filters.CallbackAdminFilter(False))
async def callback_cancel_tribunal(callback: CallbackQuery, session: AsyncSession, chat_info: ChatInfo) -> None:
    chat_info.set_tribunal_timeout(int(time()))
    await database.set_chat_info(session, chat_info.export())
    try:
        name = utils.name_format(callback.from_user.id,
                                 callback.from_user.username,
                                 callback.from_user.first_name,
                                 callback.from_user.last_name,
                                 False)
        await callback.bot.stop_poll(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     reply_markup=keyboards.canceled_tribunal_keyboard(name))
    except Exception as e:
        await callback.answer(f'{e}')
