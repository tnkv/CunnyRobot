import platform
from datetime import datetime
from importlib.metadata import version
import git
import psutil

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database, filters

router = Router()

STARTUP_TIME = datetime.now()
repo = git.Repo(search_parent_directories=True)
COMMIT = repo.git.rev_parse(repo.head, short=True)
OS = f'{platform.system()} {platform.release()} ({platform.version()})'
CPU = f'{psutil.cpu_count()} ({psutil.cpu_freq().max / 1000:.2f}GHz)'
RAM_AMOUNT = f'{round(psutil.virtual_memory().total / (1024.0 ** 3), 1)} GB'

@router.message(Command(commands=['status']), filters.SuperUserFilter())
async def command_status(message: Message, session: AsyncSession) -> None:
    await message.reply(
        text=f'<b>TribunalBot</b> (<code>{COMMIT}</code>)\n\n'
             f'Uptime: {format_uptime()}\n'
             f'Used RAM: {used_ram()}\n'
             f'Chat count: {await database.chat_count(session)}\n\n'
             f'OS: {OS}\n'
             f'CPU: {CPU}\n'
             f'RAM: {RAM_AMOUNT}\n\n'
             f'Startup date: {format_time(STARTUP_TIME)}\n'
             f'System time: {format_time(datetime.now())}\n\n'
             f'<i>Powered by aiogram ({version("aiogram")})</i>\n'
    )


def used_ram() -> str:
    process = psutil.Process()
    return f'{round(process.memory_info().rss / 1024.0 ** 2, 2)} MB'


def format_time(date: datetime) -> str:
    return date.strftime('%Y-%m-%d %H:%M:%S')


def format_uptime() -> str:
    uptime = datetime.now() - STARTUP_TIME

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m {seconds}s"
