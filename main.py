import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from src.commands import router
from src.utils import database

dp = Dispatcher()
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')


async def main() -> None:
    await database.initDb()  # создание бд если это надо
    dp.include_routers(router.restrictions_commands,
                       router.utility_commands,
                       router.fun_commands,
                       router.configuration_commands,
                       router.events_commands)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.INFO)
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        logging.warning('Bot stopped')
