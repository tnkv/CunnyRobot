import os
from time import time

from aiogram import Bot
from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER, RESTRICTED
from aiogram.types import ChatMemberUpdated, ChatPermissions

from src.utils import keyboards, database, nameformat

bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
router = Router()


# Добавляю чат в бд если добавили бота в него
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> (MEMBER | ADMINISTRATOR)))
async def event_new_chat(event: ChatMemberUpdated):
    await database.addChat(event.chat.id)


# Отправка капчи новому участнику если он не был замучен до этого
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def event_new_member(event: ChatMemberUpdated):
    welcome_message = await database.getCaptchaText(event.chat.id)
    try:
        await event.chat.restrict(user_id=event.from_user.id,
                                  until_date=0,
                                  permissions=ChatPermissions(can_send_messages=False))
        name = nameformat.nameformat(event.from_user.id,
                                     event.from_user.username,
                                     event.from_user.first_name,
                                     event.from_user.last_name)
        await bot.send_message(event.chat.id, (welcome_message.format(user=f"{name}")
                                               if "{user}" in welcome_message else welcome_message),
                               reply_markup=keyboards.captcha_keyboard(int(time()), event.from_user.id, event.chat.id))
    except Exception:
        return


# Отправка сообщение участнику что нельзя размутиться если у него были до этого ограничены права
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> RESTRICTED))
async def event_new_member(event: ChatMemberUpdated):
    await bot.send_message(event.chat.id,
                           "Привет, если тебя не замутил админ, то ты пропустил сообщение с кнопкой при первом входе, найди его с помощью \"<code>@</code>\" в поиске.")
