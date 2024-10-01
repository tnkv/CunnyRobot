from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import TelegramObject, Chat
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
            data["session_pool"] = self.session_pool
            if not (event.message or event.callback_query or event.chat_member):
                return await handler(event, data)
            data["chat_info"] = None

            if event.message:
                chat_obj: Chat = event.message.chat
            elif event.callback_query:
                chat_obj: Chat = event.callback_query.message.chat
            else:
                chat_obj: Chat = event.chat_member.chat

            if chat_obj.type != ChatType.PRIVATE:
                chat_in_db = await database.get_chat_info(session, chat_obj.id)

                if chat_in_db is None:
                    chat_in_db = await database.add_chat(session, chat_obj.id)

                data["chat_info"] = ChatInfo(chat_in_db)

            return await handler(event, data)
