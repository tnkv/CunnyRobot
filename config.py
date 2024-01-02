from os import getenv

BOT_TOKEN = getenv('TOKEN')

DB_FILE = 'tribunalbot.db'
DB_URL = 'sqlite+aiosqlite:///tribunalbot.db'

DEFAULT_CHAT_SETTINGS = {
    'welcome_message': True,
    'welcome_message_text': '{user}\nНажми на кнопку ниже, чтобы подтвердить, что ты не бот.',
    'welcome_message_timeout': 60,
    'tribunal_immunity': [777000, ],
    'is_comments': False,
    'filters_enabled': False,
    'filters_list': {}
}

