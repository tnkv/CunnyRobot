from os import getenv

BOT_TOKEN = getenv('TOKEN')
ADMIN_ID = int(getenv('ADMIN_ID', 0))

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
