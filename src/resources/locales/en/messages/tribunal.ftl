command-immunity-check = Tribunal imminity: { $status }
command-immunity-give-already =
    User { $name } already had immunity from the tribunal.

    You can check availability via /check
    You can pick up immunity with /revoke_immune
command-immunity-give =
    User { $name } has been granted immunity from the tribunal.

    You can check availability via /check
    You can pick up immunity with /revoke_immune
command-immunity-revoke-already =
    User { $name } was not immune to the tribunal.

    You can check availability via /check
    You can grant immunity with /give_immune
command-immunity-revoke =
    The user { $name } has had his immunity from the tribunal taken away.

    You can check availability via /check
    You can grant immunity with /give_immune

command-tribunal-need_reply =
    The /tribunal command should have a reply to the message of the user you want to start voting against
command-tribunal-cant_self = You can't start a tribunal against yourself.
command-tribunal-user_immune = The user is immune from the tribunal.
command-tribunal-user_already_restricted = Unable to start a tribunal, the user is already restricted.
command-tribunal-timeout-active = There is an active tribunal in chat, wait { $time } seconds before starting a new one.
command-tribunal-timeout = Wait { $time } seconds before starting a new tribunal.
command-tribunal-poll_title = Tribunal { $name }
command-tribunal-poll_option-yes = For
command-tribunal-poll_option-no = Against
command-tribunal-insufficient_votes =
    Too few people voted for the { $name }. TThe minimum total number of votes to be considered legitimate is 3
command-tribunal-insufficient_yesvotes =
    Voting for mute { $name } ended with { $mute_votes_percent }% in favor, but at least 66% is required for mute, the user will not be muted.
command-tribunal-another_restriction = Трибунал завершён, но во время ожидания пользователь получил другое наказание.
command-tribunal-finish = Голосование за мут { $name } закончилось с { $mute_votes_percent }% голосов за, пользователь отправляется в мут на { $mute_period } минут.
