from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Bot
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
            data["chat_info"] = None

            chat_obj: Chat | None = data.get("event_chat")

            if not chat_obj:
                return await handler(event, data)

            if chat_obj.type == ChatType.CHANNEL:
                bot: Bot = data.get("bot")
                if bot:
                    try:
                        await bot.leave_chat(chat_obj.id)
                        print(f"Unsubscribe from channel ID: {chat_obj.id}.")
                    except Exception:
                        pass

            if chat_obj.type == ChatType.PRIVATE:
                return await handler(event, data)

            chat_in_db = await database.add_chat(session, chat_obj)

            data["chat_info"] = ChatInfo(chat_in_db)

            return await handler(event, data)