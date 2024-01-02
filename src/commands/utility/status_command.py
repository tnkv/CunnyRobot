import platform
from datetime import datetime
from importlib.metadata import version
import git
import psutil

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import database
from src.utils.filters import admin_filter

router = Router()

startup_time = datetime.now()


@router.message(Command(commands=['status']), admin_filter.SuperUserFilter())
async def command_status(message: Message, session: AsyncSession) -> None:
    await message.reply(
        text=f'<b>TribunalBot</b> (<code>{get_commit()}</code>)\n\n'
             f'Uptime: {format_uptime()}\n'
             f'Used RAM: {used_ram()}\n'
             f'Chat count: {await database.chat_count(session)}\n\n'
             f'OS: {get_os()}\n'
             f'CPU: {psutil.cpu_count()} ({psutil.cpu_freq().max / 1000:.2f}GHz)\n'
             f'RAM: {get_ram()}\n\n'
             f'Startup date: {format_time(startup_time)}\n'
             f'System time: {format_time(datetime.now())}\n\n'
             f'<i>Powered by aiogram ({version("aiogram")})</i>\n'
             f''
    )


def get_os() -> str:
    return f'{platform.system()} {platform.release()} ({platform.version()})'


def get_ram() -> str:
    return f'{round(psutil.virtual_memory().total / (1024.0 ** 3), 1)} GB'


def used_ram() -> str:
    process = psutil.Process()
    return f'{round(process.memory_info().rss / 1024.0 ** 2, 2)} MB'


def format_time(date: datetime) -> str:
    return date.strftime('%Y-%m-%d %H:%M:%S')


def format_uptime() -> str:
    uptime = datetime.now() - startup_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m {seconds}s"


def get_commit() -> str:
    repo = git.Repo(search_parent_directories=True)
    return repo.git.rev_parse(repo.head, short=True)
