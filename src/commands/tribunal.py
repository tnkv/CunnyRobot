import asyncio
import os
from time import time

from aiogram import Bot
from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from src.utils import keyboards, database, nameformat

bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
router = Router()


# Трибунал
@router.message(Command("tribunal"))
async def command_tribunal(message: Message) -> None:
    if not message.reply_to_message:  # Проверка что ответ на сообщение
        await message.reply(
            "Команду /tribunal надо писать в ответ на сообщение человека, за ссылку в гулаг которого вы хотите начать голосование")
        return

    if message.from_user.id == message.reply_to_message.from_user.id:  # Проверка что не ответ на свое сообщение
        await message.reply("Нельзя начать трибунал против себя.")
        return

    tribunalizable = (await message.chat.get_member(user_id=message.reply_to_message.from_user.id)).status
    if tribunalizable in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR) or await database.isImmune(
            message.chat.id, message.reply_to_message.from_user.id):  # Проверка что у пользователя нет иммунитета
        await message.reply("У пользователя иммунитет от трибунала")
        return

    tribunalTimeout = await database.getTribunalTimeout(message.chat.id)
    if tribunalTimeout >= time():  # Проверка что таймаут прошел
        await message.reply(f"Перед началом нового трибунала, подождите {tribunalTimeout - int(time())} секунд.")
        return

    endTime = int(time() + 90)
    await database.setTribunalTimeout(message.chat.id, endTime + 90)  # Обновление таймаута для трибунала
    msg = await bot.send_poll(chat_id=message.chat.id,
                              reply_to_message_id=message.reply_to_message.message_id,
                              question=f"Трибунал ({nameformat.nameformat(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name, False)})",
                              options=["За", "Против"],
                              is_anonymous=False,
                              reply_markup=keyboards.cancel_tribunal_keyboard(endTime - int(time())))
    while int(time()) < endTime:
        await asyncio.sleep(5)
        if await database.getTribunalTimeout(
                message.chat.id) < time():  # Проверка что трибунал не был отменён администратором
            return

        await msg.edit_reply_markup(reply_markup=keyboards.cancel_tribunal_keyboard(endTime - int(time())))

    poll = await bot.stop_poll(chat_id=message.chat.id, message_id=msg.message_id,
                               reply_markup=keyboards.ended_tribunal_keyboard())

    name = nameformat.nameformat(message.reply_to_message.from_user.id,
                                 message.reply_to_message.from_user.username,
                                 message.reply_to_message.from_user.first_name,
                                 message.reply_to_message.from_user.last_name)

    if poll.total_voter_count < 3:
        await message.answer(
            f"В голосовании за ссылку {name} приняло слишком мало людей. Минимальное общее количество голосов для признания голосования легитимным - 3")
        return

    votes = {option.text: option.voter_count for option in poll.options}
    mute_votes = int(votes['За'] * 100 / poll.total_voter_count)  # Подсчет процента "за"

    if mute_votes < 66:
        await message.answer(
            f"Голосование за мут {name} закончилось с {mute_votes}% голосов за, но для мута требуется хотя бы 66%, пользователь не будет замучен.")
        return

    try:
        await message.bot.restrict_chat_member(chat_id=message.chat.id,
                                               user_id=message.reply_to_message.from_user.id,
                                               until_date=(int(time()) + ((votes['За'] * 2 - votes['Против']) * 60)),
                                               permissions=ChatPermissions(can_send_messages=False))
        await message.answer(
            f"Голосование за мут {name} закончилось с {mute_votes}% голосов за, пользователь отправляется в мут на {(votes['За'] * 2) - votes['Против']} минут.")
    except Exception:
        pass
