from aiogram.client.session import aiohttp
from aiogram.enums import ChatMemberStatus
from aiogram.types import User, Chat
from aiogram.utils.markdown import html_decoration

ANON_ADMIN_ID = 1087968824
CAS_LINK = 'https://api.cas.chat/check?user_id={user_id}'
ADMIN_STATUS = (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)
TIME_COEFFICIENT = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}


class NameFormat:
    def __init__(self, user: User):
        self.user_id = user.id
        self.username = user.username
        self.full_name = user.full_name

    def get(self, is_link=True) -> str:
        if self.username:
            return f'<a href="tg://user?id={self.user_id}">@{self.username}</a>' \
                if is_link and self.user_id > 0 \
                else f'@{self.username}'

        return f'<a href="tg://user?id={self.user_id}">{html_decoration.quote(self.full_name)}</a>' \
            if is_link and self.user_id > 0 \
            else f'{html_decoration.quote(self.full_name)}'


# Проверка наличия пользователя в базе CAS
async def is_cas_ban(telegram_user_id: int) -> bool:
    session = aiohttp.ClientSession()
    async with session.get(CAS_LINK.format(user_id=telegram_user_id)) as resp:
        answer = await resp.json(content_type='application/json')
        await session.close()

    return answer.get('ok', False)


async def is_admin(user_id: int, chat: Chat) -> bool:
    if user_id == ANON_ADMIN_ID:
        return True

    if (await chat.get_member(user_id=user_id)).status in ADMIN_STATUS:
        return True

    return False


def get_restriction_time(duration: str) -> int:
    unit = duration[-1]
    value = int(duration[:-1]) if duration[:-1].isdigit() else 0
    return value * TIME_COEFFICIENT.get(unit, 0)


def inflect_with_num(number) -> int:
    # 0 - 1 секунда
    # 1 - 10 секунд
    # 2 - 2 секунды
    units = number % 10
    tens = number % 100 - units

    if tens == 10 or units >= 5 or units == 0:
        needed_form = 1
    elif units > 1:
        needed_form = 2
    else:
        needed_form = 0

    return needed_form
