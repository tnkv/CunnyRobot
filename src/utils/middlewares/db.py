from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.utils import database
from src.utils import ChatInfo

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session

            chat_type = event.message.chat.type if event.message else event.callback_query.message.chat.type
            if chat_type != ChatType.PRIVATE:
                chat_id = event.message.chat.id if event.message else event.callback_query.message.chat.id
                chat_in_db = await database.get_chat_info(session, chat_id)
                data["chat_info"] = ChatInfo(chat_in_db)

            return await handler(event, data)
