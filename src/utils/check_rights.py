from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

ADMIN_STATUS = (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)

async def is_admin(user_id: int, message: Message) -> bool:
    if message.sender_chat and message.sender_chat.id == message.chat.id:
        return True

    if (await message.chat.get_member(user_id=user_id)).status in ADMIN_STATUS:
        return True

    return False
