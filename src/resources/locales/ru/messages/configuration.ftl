-configuration-title = <b>Конфигурация чата</b>
-configuration-title-filters = <b>Фильтры</b>
-configuration-title-filters-list = <b>Список фильтров</b>
-configuration-title-welcome = <b>Настройки входа</b>
-configuration-title-members = <b>Участники</b>
-configuration-title-members-lang = <b>Выбор языка</b>

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

    Regex: <code>{ $regex }</code>
    Тип проверки: { $full_match ->
    [0] Частичное соответствие
    *[other] Полное соответствие
}
command-configuration-filters-added =
    Фильтр <code>{ $regex }</code> добавлен!
    Сообщения от пользователей с правами администратора удаляться не будут. Все сообщения перед проверкой переходят в lowercase.
command-configuration-filters-remove =
    Для удаления фильтра, напишите его ID

    Следующее введённое вами сообщение будет воспринято как ID фильтра, для выхода из режима удаления фильтра используй команду /cancel
command-configuration-filters-remove-notfound =
    Фильтр с ID <code>{ $filter_id }</code> не найден, проверьте написание.
command-configuration-filters-remove-confirmation =
    <b>Подтвердить удаление фильтра?</b>
    В случае подтверждения, выбранный фильтр будет удален.

    ID: <code>{ $filter_id }</code>
    Regex: <code>{ $regex }</code>
    Тип проверки: { $full_match ->
    [0] Частичное соответствие
    *[other] Полное соответствие
}
command-configuration-filters-remove-removed = <b>Фильтр удалён</b>

command-configuration-welcome =
    {-configuration-title}
    {-configuration-title-welcome}

    { $name }, используй кнопки ниже для управления чатом.
command-configuration-welcome-setwelcome =
    Для установки нового приветствия напишите его в следующем сообщении.

    Для упоминания пользователя добавь <code>{"{user}"}</code> в тексте.
    Для форматирования текста используй возможности в клиенте.

    Следующее ввёденное вами сообщение станет приветствием в этом чате, для выхода из режима редактирования выполни команду /cancel
command-configuration-welcome-setwelcome-preview =
    Теперь все новые участники будут получать следующее сообщение в качестве приветствия:
command-configuration-welcome-setwelcome-confirm = Подвердить изменение?
command-configuration-welcome-setwelcome-set = Новое приветствие установлено.
command-configuration-welcome-setwelcome-unset = Новое приветствие не будет установлено.
command-configuration-welcome-settime =
    Напиши количество секунд (0-300), которое потребуется подождать новому участнику, перед тем как получить возможность снять мут.

    Для выхода из режима редактирования испольуй /cancel
command-configuration-welcome-settime-no_number = Это не похоже на целое число, попробуй ещё раз.
command-configuration-welcome-settime-limit = Количество секунд должно удовлетворять условию "0 <= time <= 300"
command-configuration-welcome-settime-set = Теперь новым учасникам придётся ждать { $seconds } для разблокировки кнопки снятия мута.

command-configuration-members =
    {-configuration-title}
    {-configuration-title-members}

    { $name }, используй кнопки ниже для управления чатом.

command-configuration-members-lang =
    {-configuration-title}
    {-configuration-title-members}
    {-configuration-title-members-lang}

    { $name }, используй кнопки ниже для управления чатом.
