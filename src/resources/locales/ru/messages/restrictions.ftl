command-mute-immune_user = Этого пользователя замутить нельзя.
command-mute-mute = Пользователь { $name } замьючен.
command-mute-tempmute = Пользователь { $name } замьючен на { $period }.

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
   Пользователь { $name }  получил { $warn_number }/{ $warn_number_limit } предупреждений.
   В качестве наказания был выдан мут на 1 неделю.


   { $warn_display }
command-warn-display_warns_header = Предупреждения полученные пользователем
command-warn-display-noreason = Без причины.
command-warn-check-nowarns_self = У вас нет предупреждений.
command-warn-check-nowarns = У пользователя { $name } нет предупреждений.
callback-delwarn-delwarn = Предупреждение для пользователя <code>{ $user }</code> удалено.
command-delwarn-nowarns = У пользователя нет предупреждений.
command-delwarn-delwarn =
    Предупреждение для пользователя { $name } было удалено.

    Удалённое предупреждение:
    { $warn_link }

    У пользователя осталось { $warn_count } предупреждений
