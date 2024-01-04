import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import config
from src.commands import router
from src.utils.middlewares.db import DbSessionMiddleware
from src.utils import db

dp = Dispatcher()
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')


async def main() -> None:
    engine = create_async_engine(url=config.DB_URL)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_routers(
        router.restrictions_commands,
        router.utility_commands,
        router.fun_commands,
        router.configuration_commands,
        router.events_commands
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        logging.warning('Bot stopped')
