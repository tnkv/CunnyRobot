from aiogram import Router

from src.commands.restrictions import (
    ban_command,
    mute_command,
    um_command,
    tribunal_command,
    immunity_command,
    warn_command
)
from src.commands.chat_configuration import (
    configuration,
    confuguration_welcomer,
    confuguration_filters,
    configuration_members
)
from src.commands.events import (
    welcomer_event,
    filters_event,
    callback
)
from src.commands.utility import (
    cas_ban_check,
    status_command,
    start_command,
    set_bot_info
)
from src.commands.fun import (
    moscow
)

restrictions_commands = Router()
restrictions_commands.include_routers(
    ban_command.router,
    mute_command.router,
    um_command.router,
    tribunal_command.router,
    immunity_command.router,
    warn_command.router
)

configuration_commands = Router()
configuration_commands.include_routers(
    configuration.router,
    confuguration_welcomer.router,
    confuguration_filters.router,
    configuration_members.router
)

events_commands = Router()
events_commands.include_routers(
    welcomer_event.router,
    filters_event.router,
    callback.router
)

utility_commands = Router()
utility_commands.include_routers(
    cas_ban_check.router,
    status_command.router,
    start_command.router,
    set_bot_info.router
)

fun_commands = Router()
fun_commands.include_routers(
    moscow.router
)
