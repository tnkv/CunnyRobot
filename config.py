from os import getenv

BOT_TOKEN = getenv('TOKEN')
ADMIN_ID = int(getenv('ADMIN_ID', 0))

LOCALES = ('ru', 'en')

DB_FILE = 'tribunalbot.db'
DB_URL = 'sqlite+aiosqlite:///tribunalbot.db'

DEFAULT_CHAT_SETTINGS = {
    'welcome_message': True,
    'welcome_message_text': '{user}\nНажми на кнопку ниже, чтобы подтвердить, что ты не бот.',
    'welcome_message_timeout': 60,
    'tribunal_immunity': [777000, ],
    'is_comments': False,
    'ban_channel': False,
    'channel_whitelist': [],
    'warns_count_trigger': 3,
    'filters_enabled': False,
    'filters_list': {},
    'chat_language': 'ru'
}

GROUPS_COMMANDS = {
    "tribunal": "botinfo-cmd-tribunal",
    "warns": "botinfo-cmd-warns",
    "check": "botinfo-cmd-check",
    "is_cas_ban": "botinfo-cmd-casban"
}

ADMIN_GROUP_COMMANDS = {
    "um": "botinfo-admcmd-um",
    "mute": "botinfo-admcmd-mute",
    "ban": "botinfo-admcmd-ban",
    "warn": "botinfo-admcmd-warn",
    "unwarn": "botinfo-admcmd-unwarn",
    "give_immunity": "botinfo-admcmd-giveimmunity",
    "revoke_immunity": "botinfo-admcmd-revokeimminity",
    "configure": "botinfo-admcmd-configure"
}

PM_COMMANDS = {
    "start": "botinfo-cmd-start"
}
