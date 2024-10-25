import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import config
from src.commands import router
from src.utils import db, middlewares, enums, mjson
from src.utils.middlewares.retry import RetryRequestMiddleware

dp = Dispatcher()



async def main() -> None:
    session: AiohttpSession = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    session.middleware(RetryRequestMiddleware())

    bot = Bot(
        token=config.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(
            parse_mode="HTML"
        )
    )

    engine = create_async_engine(url=config.DB_URL)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    i18n_middleware = dp["i18n_middleware"] = I18nMiddleware(
        core=FluentRuntimeCore(
            path="src/resources/locales/{locale}",
            raise_key_error=False,
            locales_map={enums.Locale.EN: enums.Locale.RU},
        ),
        manager=middlewares.LocaleManager(),
        default_locale=enums.Locale.DEFAULT,
    )

    dp.update.outer_middleware(middlewares.DbSessionMiddleware(session_pool=sessionmaker))
    i18n_middleware.setup(dispatcher=dp)

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
