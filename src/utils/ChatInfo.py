import json
from config import DEFAULT_CHAT_SETTINGS


class ChatInfo:
    chat_id = 0
    last_tribunal_end = 0
    welcome_message = DEFAULT_CHAT_SETTINGS.get('welcome_message', True)
    welcome_message_text = DEFAULT_CHAT_SETTINGS.get('welcome_message_text',
                                                     '{user}\nНажми на кнопку ниже, чтобы подтвердить, что ты не бот.')
    welcome_message_timeout = DEFAULT_CHAT_SETTINGS.get('welcome_message_timeout', 60)
    tribunal_immunity = DEFAULT_CHAT_SETTINGS.get('tribunal_immunity', [777000, ])
    is_comments = DEFAULT_CHAT_SETTINGS.get('is_comments', False)

    def __init__(self, chat_in_db: list):
        if not chat_in_db:
            return

        self.chat_id: int = chat_in_db[0][0]
        self.last_tribunal_end: int = chat_in_db[0][1]

        chat_settings = json.loads(chat_in_db[0][2])
        self.welcome_message: bool = chat_settings.get('welcome_message', self.welcome_message)
        self.welcome_message_text: str = chat_settings.get('welcome_message_text', self.welcome_message_text)
        self.welcome_message_timeout: int = chat_settings.get('welcome_message_timeout', self.welcome_message_timeout)
        self.tribunal_immunity: list = chat_settings.get('tribunal_immunity', self.tribunal_immunity)
        self.is_comments: bool = chat_settings.get('is_comments', self.is_comments)

    def export(self) -> tuple:
        settings = {
            'welcome_message': self.welcome_message,
            'welcome_message_text': self.welcome_message_text,
            'welcome_message_timeout': self.welcome_message_timeout,
            'tribunal_immunity': self.tribunal_immunity,
            'is_comments': self.is_comments
        }

        return self.chat_id, self.last_tribunal_end, json.dumps(settings)

    def switch_comments(self) -> None:
        self.is_comments = not self.is_comments

    def switch_welcome(self) -> None:
        self.welcome_message = not self.welcome_message

    def add_immune(self, telegram_user_id: int) -> bool:
        if telegram_user_id in self.tribunal_immunity:
            return False

        self.tribunal_immunity.append(telegram_user_id)
        return True

    def revoke_immune(self, telegram_user_id: int) -> bool:
        if telegram_user_id not in self.tribunal_immunity:
            return False

        self.tribunal_immunity.remove(telegram_user_id)
        return True

    def set_tribunal_timeout(self, date: int) -> None:
        self.last_tribunal_end = date

    def set_welcome_text(self, welcome_message_text: str):
        self.welcome_message_text = welcome_message_text

    def set_welcome_timeout(self, timeout: int):
        self.welcome_message_timeout = timeout
