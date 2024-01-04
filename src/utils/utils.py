from time import time

from aiogram.client.session import aiohttp
from aiogram.utils.markdown import html_decoration
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

ANON_ADMIN_ID = 1087968824
CAS_LINK = 'https://api.cas.chat/check?user_id={user_id}'
ADMIN_STATUS = (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)
TIME_COEFFICIENT = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}

def name_format(UserID: int, userName, firstName, surName,
                isLink=True) -> str:  # Форматирование имени в зависимости от наличия юзернейма, фамилии итд
    if userName is not None:
        return f'<a href="tg://user?id={UserID}">@{userName}</a>' if isLink else f'@{userName}'
    elif surName is not None:
        return f'<a href="tg://user?id={UserID}">{html_decoration.quote(firstName)} {html_decoration.quote(surName)}</a>' if isLink else f'{html_decoration.quote(firstName)} {html_decoration.quote(surName)}'
    return f'<a href="tg://user?id={UserID}">{html_decoration.quote(firstName)}</a>' if isLink else f'{html_decoration.quote(firstName)}'


# Проверка наличия пользователя в базе CAS
async def is_cas_ban(TelegramUserID: int) -> bool:
    session = aiohttp.ClientSession()
    async with session.get(CAS_LINK.format(user_id=TelegramUserID)) as resp:
        answer = await resp.json(content_type='application/json')
        await session.close()

    return answer.get('ok', False)


async def is_admin(user_id: int, message: Message) -> bool:
    if user_id == ANON_ADMIN_ID:
        return True

    if (await message.chat.get_member(user_id=user_id)).status in ADMIN_STATUS:
        return True

    return False


def inflect_with_num(number: int, forms: tuple[str, str, str]) -> str:
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

    return f'{number} {forms[needed_form]}'


def get_restriction_time(duration: str) -> int:
    unit = duration[-1]
    value = int(duration[:-1]) if duration[:-1].isdigit() else 0
    return int(time()) + value * TIME_COEFFICIENT.get(unit, 0) + 1
