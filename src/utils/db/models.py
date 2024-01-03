import json

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

import config
from src.utils.db.base import Base

class TribunalBot(Base):
    __tablename__ = 'TribunalBot'

    TelegramChatID = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    LastTribunalEnd = Column(Integer, default=0)
    ChatSettings = Column(String, default=json.dumps(config.DEFAULT_CHAT_SETTINGS))

class Warns(Base):
    __tablename__ = 'Warns'
    WarnID = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    TelegramChatID = Column(Integer, ForeignKey('TribunalBot.TelegramChatID'))
    TelegramUserID = Column(Integer, default=0)
    Reason = Column(String, default='')
    MessageID = Column(Integer, default=0)
    IsActive = Column(Boolean, default=True)

