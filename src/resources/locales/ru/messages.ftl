common-errors-cant_delete_msg =
    Не удалось удалить сообщение.

    Ошибка: <code>{ $exception }</code>
common-errors-cant_mute =
    Не удалось замутить пользователя.

    Ошибка: <code>{ $exception }</code>
common-errors-cant_unmute =
    Не удалось размутить пользователя.

    Ошибка: <code>{ $exception }</code>
common-errors-cant_ban =
    Не удалось заблокировать пользователя.

    Ошибка: <code>{ $exception }</code>
common-need_admin_rights = Ты не админ.

callback-button_not_your = Эта кнопка не для тебя.
callback-button_become_active_in = Кнопка заработает через { $seconds }с.

events-welcomer-newchat-noadmin =
    Привет. Для того что бы я мог управлять этим чатом мне необходимы права администратора.
events-welcomer-newchat-admin =
    Бот добавлен в качестве админстратора этого чата.
events-welcomer-captcha_not_solved =
    Привет { $name },если тебя не замутил админ, то ты пропустил сообщение с кнопкой при первом входе, найди его с помощью "<code>@</code>" в поиске.

command-start = Этот бот работает только в чатах, выбери чат куда хочешь добавить бота.

command-is_cas_ban-need_telegram_id =
    Необходимо указать Telegram ID пользователя через пробел

    <i>Powered by https://cas.chat/api</i>
command-is_cas_ban-incorrect_telegram_id =
    Некорректный Telegram ID

    <i>Powered by https://cas.chat/api</i>
command-is_cas_ban =
    Статус блокировки в CAS: { $status }

    <i>Powered by https://cas.chat/api</i>

command-mute-immune_user = Этого пользователя замутить нельзя.
command-mute-mute = Пользователь { $name } замучен.
command-mute-tempmute = Пользователь { $name } замучен на { $period }.

command-unmute-need_telegram_id = Для снятия ограничений необходимо ответить на сообщение или написать Telegram ID через пробел.
command-unmute-unmute = С пользователя { $user } сняты ограничения.

command-ban-immune_user = Этого пользователя заблокировать нельзя.
command-ban-ban = Пользователь { $name } заблокирован.
command-ban-need_telegram_id = Для блокировки пользователя необходимо ответить на сообщение или написать Telegram ID через пробел.
command-ban-ban_id = Пользователь <code>{ $user }</code> заблокирован.

command-warn-cant_warn_self = Нельзя выдать предупреждение самому себе.
command-warn-cant_warn_admin = Нельзя выдать предупреждение администратору.
command-warn-warn =
    Администратор { $admin_name } выдал предупреждение { $name }

    Теперь пользователь имеет { $warn_number }/{ $warn_number_limit } предупреждений.
    Причина: { $warn_reason }
    В случае достижения лимита, пользователь получит мут на 1 неделю.
command-warn-warn_limit =
   Пользователь { $name }  получил { $warn_number }/{ $warn_number_limit } предупреждений. '
   В качестве наказания был выдан мут на 1 неделю.


   { $warn_display }

command-warn-display_warns_header = Предупреждения полученные пользователем
command-warn-display-noreason = Без причины.

command-warn-check-nowarns_self = У вас нет предупреждений.
command-warn-check-nowarns = У пользователя { $name } нет предупреждений.

callback-delwarn-delwarn = Предупреждение для пользователя <code>{ $user }</code> удалено.
command-delwarn-nowarns = У пользователя нет предупреждений.
command-delwarn-delwarn =
    Предупреждение для пользователя { $name } было удалено.\n\n'
    Удалённое предупреждение:\n'
    { $warn_link }\n\n'
    У пользователя осталось { $warn_count } предупреждений')