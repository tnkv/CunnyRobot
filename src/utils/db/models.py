import json

from sqlalchemy import Column, Integer, String

import config
from src.utils.db.base import Base

class TribunalBot(Base):
    __tablename__ = 'TribunalBot'

    TelegramChatID = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    LastTribunalEnd = Column(Integer, default=0)
    ChatSettings = Column(String, default=json.dumps(config.DEFAULT_CHAT_SETTINGS))

