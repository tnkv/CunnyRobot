from aiogram.client.session import aiohttp
from aiogram.utils.markdown import html_decoration
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

CAS_LINK = 'https://api.cas.chat/check?user_id={user_id}'
ADMIN_STATUS = (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)


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
    if message.sender_chat and message.sender_chat.id == message.chat.id:
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
