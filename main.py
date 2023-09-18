import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from src.commands import tribunal, newchat, promote, restrictions, callback, setwelcome
from src.utils import database

dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")


async def main() -> None:
    await database.initDb()  # создание бд если это надо
    dp.include_routers(tribunal.router, newchat.router, promote.router, restrictions.router, callback.router,
                       setwelcome.router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        logging.warning("Bot stopped")
