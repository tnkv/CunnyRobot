import json
import sqlite3 as sq

import config
from src.utils.ChatInfo import ChatInfo

conn = sq.connect('tribunalbot.db')
cur = conn.cursor()


async def initDb() -> None:
    cur.execute('''CREATE TABLE IF NOT EXISTS TribunalBot
                  (TelegramChatID INT, LastTribunalEnd INT, ChatSettings TEXT)''')


async def addChat(TelegramChatID: int) -> None:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    if not records:
        cur.execute('INSERT INTO TribunalBot VALUES(?,?,?)',
                    (TelegramChatID, 0, json.dumps(config.DEFAULT_CHAT_SETTINGS)))
        conn.commit()


def getChatInfo(telegram_chat_id: int) -> list:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (telegram_chat_id,))
    return cur.fetchall()

def setChatInfo(data: tuple) -> None:
    cur.execute('UPDATE TribunalBot SET LastTribunalEnd = ?, ChatSettings = ? WHERE TelegramChatID = ?',
                (data[1], data[2], data[0]))
    conn.commit()

def is_comments(telegram_chat_id) -> bool:
    return ChatInfo(getChatInfo(telegram_chat_id)).is_comments
