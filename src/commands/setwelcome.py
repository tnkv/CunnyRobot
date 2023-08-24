from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message

from src.utils import database

router = Router()

# Выдача иммунитета от трибунала (У всех админов он по умолчанию потому что их замутить нельзя)
@router.message(Command(commands=["setwelcome"]))
async def command_setwelcome(message: Message) -> None:
    initiator = (await message.chat.get_member(user_id=message.from_user.id)).status
    if initiator not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR):
        await message.reply("Ты не админ.")
        return

    msg = message.text.split(" ", 1)
    if len(msg) == 1:
        await message.reply('Для установки нового приветственного сообщения напишите его через пробел после команды.\n\nДля упоминания пользователя добавь <code>{user}</code> в тексте.\nДля форматирования текста используй <a href="https://core.telegram.org/bots/api#html-style">разметку HTML</a>\n\nДля того что бы отключить капчу и приветственное сообщение, напиши <code>disable</code> вместо текста.\nДля установки значений по-умолчанию, напиши <code>reset</code> вместо текста')
        return
    if msg[1] == "disable":
        await message.reply("Отправка приветственного сообщения и капча отключена для этого чата, для включения, установите новый текст или сбросьте до настроек по-умолчанию.")
        await database.setCaptchaText(message.chat.id, msg[1])
    elif msg[1] == "reset":
        await message.reply("Настройки приветственного сообщения и капчи были сброшены до настроек по-умолчанию.")
        await database.setCaptchaText(message.chat.id, "{user}\nНажми на кнопку ниже, чтобы подтвердить, что ты не бот.")
    else:
        try:
            await message.reply(f"Теперь в чате установлено новое приветственное сообщение:\n\n{msg[1]}")
            await database.setCaptchaText(message.chat.id, msg[1])
        except Exception:
            await message.reply("Приветственное сообщение не будет изменено, в разметке была допущена ошибка.")