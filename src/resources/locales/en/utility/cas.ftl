cas-is_cas_ban-need_telegram_id =
    It is necessary to specify Telegram user ID with a space

    <i>Powered by https://cas.chat/api</i>
cas-is_cas_ban-incorrect_telegram_id =
    Invalid Telegram ID

    <i>Powered by https://cas.chat/api</i>
cas-is_cas_ban =
    Ban status in CAS: { $status }

    <a href="https://cas.chat/query?u={ $user_id }">CAS profile</a>

    <i>Powered by https://cas.chat/api</i>

cas-status = { $status ->
    [0] Not banned
    *[other] Banned
    }

cas-autoban = The user who entered the chat was detected in the CAS database and was banned.
    The welcome message has been deleted.