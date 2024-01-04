import json
import uuid

from config import DEFAULT_CHAT_SETTINGS
from src.utils.db.models import TribunalBot


class ChatInfo:
    chat_id = 0
    last_tribunal_end = 0
    welcome_message = DEFAULT_CHAT_SETTINGS.get('welcome_message', True)
    welcome_message_text = DEFAULT_CHAT_SETTINGS.get('welcome_message_text',
                                                     '{user}\nНажми на кнопку ниже, чтобы подтвердить, что ты не бот.')
    welcome_message_timeout = DEFAULT_CHAT_SETTINGS.get('welcome_message_timeout', 60)
    tribunal_immunity = DEFAULT_CHAT_SETTINGS.get('tribunal_immunity', [777000, ])
    is_comments = DEFAULT_CHAT_SETTINGS.get('is_comments', False)
    ban_channel = DEFAULT_CHAT_SETTINGS.get('ban_channel', False)
    channel_whitelist = DEFAULT_CHAT_SETTINGS.get('channel_whitelist', [])
    warns_count_trigger = DEFAULT_CHAT_SETTINGS.get('warns_count_trigger', 3)
    filters_enabled = DEFAULT_CHAT_SETTINGS.get('filters_enabled', False)
    filters_list = DEFAULT_CHAT_SETTINGS.get('filters_list', {})

    def __init__(self, chat_in_db: TribunalBot | None):
        if chat_in_db is None:
            return

        self.chat_id: int = chat_in_db.TelegramChatID
        self.last_tribunal_end: int = chat_in_db.LastTribunalEnd

        chat_settings = json.loads(chat_in_db.ChatSettings)
        self.welcome_message: bool = chat_settings.get('welcome_message', self.welcome_message)
        self.welcome_message_text: str = chat_settings.get('welcome_message_text', self.welcome_message_text)
        self.welcome_message_timeout: int = chat_settings.get('welcome_message_timeout', self.welcome_message_timeout)
        self.tribunal_immunity: list = chat_settings.get('tribunal_immunity', self.tribunal_immunity)
        self.is_comments: bool = chat_settings.get('is_comments', self.is_comments)
        self.ban_channel: bool = chat_settings.get('ban_channel', self.ban_channel)
        self.channel_whitelist: list = chat_settings.get('channel_whitelist', self.channel_whitelist)
        self.filters_enabled: bool = chat_settings.get('filters_enabled', self.filters_enabled)
        self.filters_list: dict = chat_settings.get('filters_list', self.filters_list)

    def export(self) -> TribunalBot:
        settings = {
            'welcome_message': self.welcome_message,
            'welcome_message_text': self.welcome_message_text,
            'welcome_message_timeout': self.welcome_message_timeout,
            'tribunal_immunity': self.tribunal_immunity,
            'is_comments': self.is_comments,
            'filters_enabled': self.filters_enabled,
            'filters_list': self.filters_list
        }

        return TribunalBot(TelegramChatID=self.chat_id,
                           LastTribunalEnd=self.last_tribunal_end,
                           ChatSettings=json.dumps(settings))

    def switch_comments(self) -> None:
        self.is_comments = not self.is_comments

    def switch_welcome(self) -> None:
        self.welcome_message = not self.welcome_message

    def switch_filters(self) -> None:
        self.filters_enabled = not self.filters_enabled

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

    def add_filter(self, regex: str, full_match: bool = False):
        self.filters_list[uuid.uuid4().hex] = {
            'regex': regex,
            'full_match': full_match}

    def remove_filter(self, filter_id: str):
        self.filters_list.pop(filter_id)
