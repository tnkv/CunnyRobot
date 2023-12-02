import asyncio
from time import time

from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions, CallbackQuery

from src.utils import keyboards, database, utils
from src.utils.ChatInfo import ChatInfo
from src.utils.filters import admin_filter

router = Router()


# Трибунал
@router.message(Command('tribunal'))
async def command_tribunal(message: Message) -> None:
    if not message.reply_to_message:  # Проверка что ответ на сообщение
        await message.reply(
            'Команду /tribunal надо писать в ответ на сообщение человека, за ссылку в гулаг которого вы хотите начать голосование')
        return

    if message.from_user.id == message.reply_to_message.from_user.id:  # Проверка что не ответ на свое сообщение
        await message.reply('Нельзя начать трибунал против себя.')
        return

    chat_info = ChatInfo(database.getChatInfo(message.chat.id))
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

    tribunalTimeout = chat_info.last_tribunal_end
    if tribunalTimeout >= time():  # Проверка что таймаут прошел
        await message.reply(f'Перед началом нового трибунала, подождите {tribunalTimeout - int(time())} секунд.')
        return

    endTime = int(time()) + 90

    chat_info.set_tribunal_timeout(int(endTime) + 90)
    database.setChatInfo(chat_info.export())

    msg = await message.bot.send_poll(chat_id=message.chat.id,
                                      reply_to_message_id=message.reply_to_message.message_id,
                                      question=f'''Трибунал ({utils.name_format(message.reply_to_message.from_user.id,
                                                                                message.reply_to_message.from_user.username,
                                                                                message.reply_to_message.from_user.first_name,
                                                                                message.reply_to_message.from_user.last_name,
                                                                                False)})''',
                                      options=['За', 'Против'],
                                      is_anonymous=False,
                                      reply_markup=keyboards.cancel_tribunal_keyboard(endTime - int(time())))
    while time() < endTime:
        await asyncio.sleep(min(5.0, endTime - time()))
        if ChatInfo(database.getChatInfo(
                message.chat.id)).last_tribunal_end < time():  # Проверка что трибунал не был отменён администратором
            return

        await msg.edit_reply_markup(reply_markup=keyboards.cancel_tribunal_keyboard(endTime - int(time())))

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
    except Exception:
        pass


# Обработка отмены трибунала
@router.callback_query(F.data == 'cancel_tribunal', admin_filter.CallbackAdminFilter(False))
async def callback_cancel_tribunal(callback: CallbackQuery) -> None:
    chat_info = ChatInfo(database.getChatInfo(callback.message.chat.id))
    chat_info.set_tribunal_timeout(int(time()))
    database.setChatInfo(chat_info.export())
    try:
        name = utils.name_format(callback.from_user.id,
                                 callback.from_user.username,
                                 callback.from_user.first_name,
                                 callback.from_user.last_name,
                                 False)
        await callback.bot.stop_poll(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     reply_markup=keyboards.canceled_tribunal_keyboard(name))
    except Exception:
        return
