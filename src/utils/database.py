from aiogram.types import Chat, User
from sqlalchemy import select, Result, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import TribunalBot, Warns


async def add_chat(session: AsyncSession, chat: Chat) -> TribunalBot:
    request = select(TribunalBot).filter_by(TelegramChatID=chat.id)
    result: Result = await session.execute(request)
    res: TribunalBot = result.scalar_one_or_none()

    if res is not None:
        res.ChatType = chat.type
        res.Title = chat.title
        res.UserName = chat.username
        await session.commit()
        return res

    telegram_chat = TribunalBot(
        TelegramChatID=chat.id,
        ChatType=chat.type,
        Title=chat.title,
        Username=chat.username
    )

    session.add(telegram_chat)
    await session.commit()
    return telegram_chat


async def get_chat_info(session: AsyncSession, chat: Chat) -> TribunalBot | None:
    request = select(TribunalBot).filter_by(TelegramChatID=chat.id)
    result: Result = await session.execute(request)
    return result.scalar_one_or_none()


async def set_chat_info(session: AsyncSession, record: TribunalBot | Warns) -> None:
    await session.merge(record)
    await session.commit()


async def chat_count(session: AsyncSession) -> int:
    request = select(func.count()).select_from(TribunalBot)
    result = await session.execute(request)
    return result.scalar()


async def add_warn(session: AsyncSession, warn: Warns):
    session.add(warn)
    await session.commit()

    request = select(Warns).filter_by(
        TelegramChatID=warn.TelegramChatID,
        TelegramUserID=warn.TelegramUserID,
        IsActive=True
    )
    result: Result = await session.execute(request)
    return result.scalars().all()


async def deactivate_warns(session: AsyncSession, warn: Warns) -> None:
    request = (update(Warns)
               .filter_by(
        TelegramChatID=warn.TelegramChatID,
        TelegramUserID=warn.TelegramUserID
    )
               .values(IsActive=False)
               )
    await session.execute(request)
    await session.commit()


async def get_warns(session: AsyncSession, chat: Chat, user: User):
    request = select(Warns).filter_by(
        TelegramChatID=chat.id,
        TelegramUserID=user.id,
        IsActive=True
    )

    result: Result = await session.execute(request)
    return result.scalars().all()
