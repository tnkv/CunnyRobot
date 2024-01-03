from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import TribunalBot, Warns


async def add_chat(session: AsyncSession, telegram_chat_id: int) -> TribunalBot:
    request = select(TribunalBot).filter_by(TelegramChatID=telegram_chat_id)
    result: Result = await session.execute(request)
    res: TribunalBot = result.scalar_one_or_none()

    if res is not None:
        return res

    telegram_chat = TribunalBot(TelegramChatID=telegram_chat_id)
    session.add(telegram_chat)
    await session.commit()
    return telegram_chat


async def get_chat_info(session: AsyncSession, telegram_chat_id: int) -> TribunalBot | None:
    request = select(TribunalBot).filter_by(TelegramChatID=telegram_chat_id)
    result: Result = await session.execute(request)
    return result.scalar_one_or_none()


async def set_chat_info(session: AsyncSession, telegram_chat: TribunalBot) -> None:
    await session.merge(telegram_chat)
    await session.commit()


async def chat_count(session: AsyncSession) -> int:
    request = select(func.count()).select_from(TribunalBot)
    result = await session.execute(request)
    return result.scalar()

async def add_warn(session: AsyncSession, warn: Warns) -> None:
    session.add(warn)
    await session.commit()
