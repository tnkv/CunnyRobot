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
common-errors-global =
    Произошла ошибка!

    Ошибка: <code> {$exception} </code>
common-action_canceled = Действие отменено.
common-need_reply = А ответить на сообщение?
common-need_admin_rights = Ты не админ.
common-super_admin_not_set = ADMIN_ID не установлена как переменная окружения.

callback-button_not_your = Эта кнопка не для тебя.
callback-button_become_active_in = Кнопка заработает через { $seconds }с.

events-welcomer-newchat-noadmin =
    Привет. Для того что бы я мог управлять этим чатом мне необходимы права администратора.
events-welcomer-newchat-admin =
    Бот добавлен в качестве админстратора этого чата.
events-welcomer-captcha_not_solved =
    Привет { $name }, если тебя не замутил админ, то ты пропустил сообщение с кнопкой при первом входе, найди его с помощью "<code>@</code>" в поиске.

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

command-immunity-check = Наличие иммунитета к трибуналу: { $status }
command-immunity-give-already =
    У пользователя { $name } уже был иммунитет от трибунала.

    Проверить наличие можно через /check
    Забрать иммунитет можно через /revoke_immune
command-immunity-give =
    Пользователю { $name } был выдан иммунитет от трибунала.

    Проверить наличие можно через /check
    Забрать иммунитет можно через /revoke_immune
command-immunity-revoke-already =
    У пользователя { $name } отсутствовал иммунитет к трибуналу.

    Проверить наличие можно через /check
    Выдать иммунитет можно через /give_immune
command-immunity-revoke =
    У пользователя { $name } был отобран иммунитет от трибунала.

    Проверить наличие можно через /check
    Выдать иммунитет можно через /give_immune

command-tribunal-need_reply =
    Команду /tribunal надо писать в ответ на сообщение человека, за ссылку в гулаг которого вы хотите начать голосование
command-tribunal-cant_self = Нельзя начать трибунал против себя.
command-tribunal-user_immune = У пользователя иммунитет от трибунала.
command-tribunal-user_already_restricted = Невозможно начать трибунал, пользователь уже ограничен.
command-tribunal-timeout-active = В чате есть активный трибунал, перед началом нового подождите { $time } секунд.
command-tribunal-timeout = Перед началом нового трибунала, подождите { $time } секунд.
command-tribunal-poll_title = Трибунал { $name }
command-tribunal-poll_option-yes = За
command-tribunal-poll_option-no = Против
command-tribunal-insufficient_votes =
    В голосовании за ссылку { $name } приняло слишком мало людей. Минимальное общее количество голосов для признания голосования легитимным - 3
command-tribunal-insufficient_yesvotes =
    Голосование за мут { $name } закончилось с { $mute_votes_percent }% голосов за, но для мута требуется хотя бы 66%, пользователь не будет замучен.
command-tribunal-another_restriction = Трибунал завершён, но во время ожидания пользователь получил другое наказание.
command-tribunal-finish = Голосование за мут { $name } закончилось с { $mute_votes_percent }% голосов за, пользователь отправляется в мут на { $mute_period } минут.

keyboards-tribunal-timebutton = Осталось { $time } сек.
keyboards-tribunal-eol = Трибунал завершён.
keyboards-tribunal-canceled = Трибунал отменён. ({ $admin})
keyboards-welcomer-captcha = Я не бот
keyboards-warn-delwarn = Удалить предупреждение

keyboards-configuration-main_menu = Главное меню
keyboards-configuration-back = Назад

keyboards-configuration-main-comment_mode = { $state ->
    [0] Режим комментариев: выключен
    *[other] Режим комментареив: включен
    }
keyboards-configuration-main-enter = Настройки входа
keyboards-configuration-main-members = Пользователи
keyboards-configuration-main-filters = Фильтры

keyboards-configuration-welcome-state = { $state ->
    [0] Приветствие: выключено
    *[other] Приветствие: включено
    }
keyboards-configuration-welcome-editmsg = Изменить сообщение
keyboards-configuration-welcome-edittime = Настроить время

keyboards-configuration-filter-state = { $state ->
    [0] Фильтры: выключены
    *[other] Фильтры: включены
    }
keyboards-configuration-filter-list = Список фильтров ({ $count })
keyboards-configuration-filter-add = Добавить фильтр
keyboards-configuration-filter-remove = Удалить фильтр

keyboards-confirm-yes = Да
keyboards-confirm-no = Нет

keyboards-add_to_chat = Добавить в чат

-configuration-title = <b>Конфигурация чата</b>
-configuration-title-filters = <b>Фильтры</b>
-configuration-title-filters-list = <b>Список фильтров</b>
-configuration-title-welcome = <b>Настройки входа</b>

command-configuration =
    {-configuration-title}

    { $name }, используй кнопки ниже для управления чатом.

command-configuration-filters =
    {-configuration-title}
    {-configuration-title-filters}

    { $name }, используй кнопки ниже для управления чатом.
command-configuration-filters-list =
    {-configuration-title}
    {-configuration-title-filters}
    {-configuration-title-filters-list}
command-configuration-filters-list-filter =
    <code>{ $filter_id }</code>:
    Regex: <code>{ $filter_regex}</code>
    Тип проверки: { $full_match ->
    [0] Частичное соответствие
    *[other] Полное соответствие
}
command-configuration-filters-addfilter =
    Для добавления нового фильтра, напишите его regex

    Следующее введённое вами сообщение будет воспринято как фильтр, для выхода из режима добавления фильтра используй команду /cancel
command-configuration-filters-fullmatch =
    Должен ли фильтр <code>{ $regex }</code> требовать точное совпадение сообщения?
command-configuration-filters-regex_error =
    Указанный Regex (<code>{ $regex }</code>) не является валидным, проверьте написание.

    Следующее введённое вами сообщение будет воспринято как фильтр, для выхода из режима добавления фильтра используй команду /cancel
command-configuration-filters-confirmation =
    Подтвердить добавление фильтра?

    Регекс: <code>{ $regex }</code>
    Полное соответствие: { $full_match ->
    [0] Нет
    *[other] Да
}
command-configuration-filters-added =
    Фильтр <code>{ $regex }</code> добавлен!
    Сообщения от пользователей с правами администратора удаляться не будут.
command-configuration-filters-remove =
    Для удаления фильтра, напишите его ID

    Следующее введённое вами сообщение будет воспринято как ID фильтра, для выхода из режима удаления фильтра используй команду /cancel
command-configuration-filters-remove-notfound =
    Фильтр с ID <code>{ $filter_id }</code> не найден, проверьте написание.
command-configuration-filters-remove-confirmation =
    <b>Подтвердить удаление фильтра?</b>
    В случае подтверждения, выбранный фильтр будет удален.

    ID: <code>{ $filter_id }</code>
    Регекс: <code>{ $regex }</code>
    Полное соответствие: { $full_match ->
    [0] Нет
    *[other] Да
}
command-configuration-filters-remove-removed = <b>Фильтр удалён</b>