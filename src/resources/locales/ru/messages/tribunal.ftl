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
    Голосование за мут { $name } закончилось с { $mute_votes_percent }% голосов за, но для мута требуется хотя бы 66%, пользователь не будет замьючен.
command-tribunal-another_restriction = Трибунал завершён, но во время ожидания пользователь получил другое наказание.
command-tribunal-finish = Голосование за мут { $name } закончилось с { $mute_votes_percent }% голосов за, пользователь отправляется в мут на { $mute_period } минут.
