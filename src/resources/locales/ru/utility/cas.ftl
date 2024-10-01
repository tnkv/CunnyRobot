cas-is_cas_ban-need_telegram_id =
    Необходимо указать Telegram ID пользователя через пробел

    <i>Powered by https://cas.chat/api</i>
cas-is_cas_ban-incorrect_telegram_id =
    Некорректный Telegram ID

    <i>Powered by https://cas.chat/api</i>
cas-is_cas_ban =
    Статус блокировки в CAS: { $status }

    <a href="https://cas.chat/query?u={ $user_id }">CAS профиль</a>

    <i>Powered by https://cas.chat/api</i>

cas-status = { $status ->
    [0] Нет заблокирован
    *[other] Заблокирован
    }

cas-autoban = Пользователь, вошедший в чат, обнаружен в базе CAS и был заблокирован.
    Приветственное сообщение удалено.