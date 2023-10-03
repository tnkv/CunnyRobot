import json
import sqlite3 as sq

conn = sq.connect('tribunalbot.db')
cur = conn.cursor()


async def initDb() -> None:
    cur.execute('''CREATE TABLE IF NOT EXISTS TribunalBot
                  (TelegramChatID INT, TribunalImmunity TEXT, CaptchaText TEXT, LastTribunalEnd INT )''')


async def addChat(TelegramChatID: int) -> None:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    if not records:
        cur.execute('INSERT INTO TribunalBot VALUES(?,?,?,?)',
                    (TelegramChatID, json.dumps((777000,)),
                     '{user}\nНажми на кнопку ниже, чтобы подтвердить, что ты не бот.', 0))
        conn.commit()


async def addImmune(TelegramChatID: int, TelegramUserID: int) -> None:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    if not records:
        return

    tribunalImmunity = json.loads(records[0][1])
    if TelegramUserID in tribunalImmunity:
        return

    tribunalImmunity.append(TelegramUserID)
    cur.execute('UPDATE TribunalBot SET TribunalImmunity = ? WHERE TelegramChatID = ?',
                (json.dumps(tribunalImmunity), TelegramChatID))
    conn.commit()


async def revokeImmune(TelegramChatID: int, TelegramUserID: int) -> None:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    if not records:
        return

    tribunalImmunity = json.loads(records[0][1])
    if TelegramUserID not in tribunalImmunity:
        return

    tribunalImmunity.remove(TelegramUserID)
    cur.execute('UPDATE TribunalBot SET TribunalImmunity = ? WHERE TelegramChatID = ?',
                (json.dumps(tribunalImmunity), TelegramChatID))
    conn.commit()


async def isImmune(TelegramChatID: int, TelegramUserID: int) -> bool:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    if records:
        return TelegramUserID in json.loads(records[0][1])
    return False


async def setCaptchaText(TelegramChatID: int, CaptchaText: str) -> None:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    if not records:
        return
    cur.execute('UPDATE TribunalBot SET CaptchaText = ? WHERE TelegramChatID = ?',
                (CaptchaText, TelegramChatID))
    conn.commit()


async def getCaptchaText(TelegramChatID: int) -> str:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    return records[0][2] if records else '{user}\nНажми на кнопку ниже, чтобы подтвердить, что ты не бот.'


async def setTribunalTimeout(TelegramChatID: int, date: int) -> None:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    if records:
        cur.execute('UPDATE TribunalBot SET LastTribunalEnd = ? WHERE TelegramChatID = ?',
                    (date, TelegramChatID))
        conn.commit()


async def getTribunalTimeout(TelegramChatID: int) -> int:
    cur.execute('SELECT * FROM TribunalBot WHERE TelegramChatID = ?', (TelegramChatID,))
    records = cur.fetchall()
    return records[0][3] if records else 0
