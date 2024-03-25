command-mute-immune_user = This user cannot be muted.
command-mute-mute = { $name } muted.
command-mute-tempmute = { $name } muted for { $period }.

command-unmute-need_telegram_id = To remove restrictions, you need to reply to the message or write Telegram ID.
command-unmute-unmute = The user { $user } has been unrestricted.

command-ban-immune_user =  This user cannot be banned.
command-ban-ban = { $name } banned.
command-ban-need_telegram_id = To ban user, you need to reply to the message or write Telegram ID.
command-ban-ban_id = <code>{ $user }</code> banned.

command-warn-cant_warn_self = You can't warn yourself.
command-warn-cant_warn_admin = You can't warn administrator.
command-warn-warn =
    Administrator { $admin_name } warned { $name }

    The user now has { $warn_number }/{ $warn_number_limit } warnings.
    Reason: { $warn_reason }
    If the limit is reached, the user will receive a mutation for 1 week.
command-warn-warn_limit =
    User { $name } has received { $warn_number }/{ $warn_number_limit } warnings.
    { $name } muted for 1 week.


   { $warn_display }
command-warn-display_warns_header = Warnings received by the user
command-warn-display-noreason = Without reason.
command-warn-check-nowarns_self = You have no warnings.
command-warn-check-nowarns = { $name } have no warnings.
callback-delwarn-delwarn = Warn for <code>{ $user }</code> deleted.
command-delwarn-nowarns = User have no warnings.
command-delwarn-delwarn =
    Warn for { $name } deleted.

    Deleted warning:
    { $warn_link }

    User have { $warn_count } warnings now.
