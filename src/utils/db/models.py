import json

from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text, String
from sqlalchemy.orm import relationship

import config
from src.utils.db.base import Base


class TribunalBot(Base):
    __tablename__ = 'TribunalBot'
    TelegramChatID = Column(Integer, primary_key=True, unique=True, autoincrement=False)

    ChatType = Column(String(50), default='supergroup')
    Title = Column(String(255), nullable=True)
    Username = Column(String(255), nullable=True)

    LastTribunalEnd = Column(Integer, default=0)
    ChatSettings = Column(Text, default=json.dumps(config.DEFAULT_CHAT_SETTINGS))
    warns = relationship('Warns', back_populates='TelegramChat')


class Warns(Base):
    __tablename__ = 'Warns'
    WarnID = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    TelegramChatID = Column(ForeignKey('TribunalBot.TelegramChatID'))
    TelegramUserID = Column(Integer, default=0)
    Reason = Column(Text, default='')
    MessageID = Column(Integer, default=0)
    IsActive = Column(Boolean, default=True)
    TelegramChat = relationship('TribunalBot', back_populates='warns')
