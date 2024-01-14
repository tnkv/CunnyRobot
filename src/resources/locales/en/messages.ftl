common-errors-cant_delete_msg =
    Failed to delete message.

    Error code: <code>{ $exception }</code>
common-errors-cant_mute =
    Failed to mute the user.

    Error code: <code>{ $exception }</code>
common-errors-cant_unmute =
    Failed to unmute the user.

    Error code: <code>{ $exception }</code>
common-errors-cant_ban =
    Failed to ban the user.

    Error code: <code>{ $exception }</code>
common-errors-global =
    An error occurred!

    Error code: <code> {$exception} </code>
common-action_canceled = Action canceled.
common-need_reply = Need a reply to a message?
common-need_admin_rights = You're not an admin..
common-super_admin_not_set = ADMIN_ID is not set as an environmental variable.

callback-button_not_your = This button is not for you.
callback-button_become_active_in = The button becomes active after { $seconds }s.

events-welcomer-newchat-noadmin =
    Hello. I need admin rights to manage this chat.
events-welcomer-newchat-admin =
    Bot has been added as an admin of this chat.
events-welcomer-captcha_not_solved =
    Hello { $name }, If you're not muted by admin, you missed the message with the button on your first joining the chat, find it with "<code>@</code>" in the search.

command-start = This bot only works in chat, choose a chat where you want to add the bot.

command-is_cas_ban-need_telegram_id =
    It is necessary to specify Telegram user ID with a space

    <i>Powered by https://cas.chat/api</i>
command-is_cas_ban-incorrect_telegram_id =
    Invalid Telegram ID

    <i>Powered by https://cas.chat/api</i>
command-is_cas_ban =
    Ban status in CAS:: { $status }

    <i>Powered by https://cas.chat/api</i>

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

keyboards-tribunal-timebutton = { $time }s left.
keyboards-tribunal-eol = The tribunal is over.
keyboards-tribunal-canceled = Tribunal canceled. ({ $admin})
keyboards-welcomer-captcha = I'm not a bot
keyboards-warn-delwarn = Remove warning

keyboards-configuration-main_menu = Main menu
keyboards-configuration-back = Back

keyboards-configuration-main-comment_mode = { $state ->
    [0] Comment mode: disabled
    *[other] Comment mode: enabled
    }
keyboards-configuration-main-enter = Welcome settings
keyboards-configuration-main-members = Members
keyboards-configuration-main-filters = Filters

keyboards-configuration-welcome-state = { $state ->
    [0] Welcome message: disabled
    *[other] Welcome message: enabled
    }
keyboards-configuration-welcome-editmsg = Edit welcome
keyboards-configuration-welcome-edittime = Edit time

keyboards-configuration-filter-state = { $state ->
    [0] Filters: disabled
    *[other] Filters: enabled
    }
keyboards-configuration-filter-list = Filter list ({ $count })
keyboards-configuration-filter-add = Add filter
keyboards-configuration-filter-remove = Remove filter

keyboards-configuration-members-lang = Chat language ( {$lang} )

keyboards-confirm-yes = Yes
keyboards-confirm-no = No

keyboards-add_to_chat = Add to chat

-configuration-title = <b>Chat configuration</b>
-configuration-title-filters = <b>Filters</b>
-configuration-title-filters-list = <b>Filter list</b>
-configuration-title-welcome = <b>Welcome settings</b>
-configuration-title-members = <b>Members</b>
-configuration-title-members-lang = <b>Language selection</b>

command-configuration =
    {-configuration-title}

    { $name }, use the buttons below to control the chat.

command-configuration-filters =
    {-configuration-title}
    {-configuration-title-filters}

    { $name }, use the buttons below to control the chat.
command-configuration-filters-list =
    {-configuration-title}
    {-configuration-title-filters}
    {-configuration-title-filters-list}
command-configuration-filters-list-filter =
    <code>{ $filter_id }</code>:
    Regex: <code>{ $filter_regex}</code>
    Type of check: { $full_match ->
    [0] Partial compliance
    *[other] Full compliance
}
command-configuration-filters-addfilter =
    To add a new filter, write its regex

    The next message you enter will be taken as a filter, to exit the mode of adding a filter use the /cancel command
command-configuration-filters-fullmatch =
    Should the <code>{ $regex }</code> filter require an exact message match?
command-configuration-filters-regex_error =
    The specified Regex (<code>{ $regex }</code>) is not valid, check the spelling.

    The next message you enter will be taken as a filter, to exit the mode of adding a filter use the /cancel command
command-configuration-filters-confirmation =
    Confirm adding a filter?

    Regex: <code>{ $regex }</code>
    Type of check: { $full_match ->
    [0] Partial compliance
    *[other] Full compliance
}
command-configuration-filters-added =
    The <code>{ $regex }</code> filter has been added!
    Messages from users with administrator privileges will not be deleted.
command-configuration-filters-remove =
    To remove a filter, write its ID

    The next message you enter will be taken as the filter ID, to exit the filter removal mode use the /cancel command
command-configuration-filters-remove-notfound =
    Filter with ID <code>{ $filter_id }</code> was not found, check the spelling.
command-configuration-filters-remove-confirmation =
    <b>Confirm filter deletion?</b>
    If confirmed, the selected filter will be deleted.

    ID: <code>{ $filter_id }</code>
    Regex: <code>{ $regex }</code>
    Type of check: { $full_match ->
    [0] Partial compliance
    *[other] Full compliance
}
command-configuration-filters-remove-removed = <b>Filter deleted.</b>

command-configuration-welcome =
    {-configuration-title}
    {-configuration-title-welcome}

    { $name }, use the buttons below to control the chat.
command-configuration-welcome-setwelcome =
    To set up a new greeting, write it in the following message.

    To mention the user, add <code>{"{user}"}</code> in the text.
    For text formatting, use the options in the client.

    The next message you enter will become a greeting in this chat, to exit the edit mode run the command /cancel
command-configuration-welcome-setwelcome-preview =
    All new members will now receive the following message as a welcome message:
command-configuration-welcome-setwelcome-confirm = Confirm the change?
command-configuration-welcome-setwelcome-set = A new greeting has been installed.
command-configuration-welcome-setwelcome-unset = The new greeting will not be installed.
command-configuration-welcome-settime =
    Write the number of seconds (0-300) that a new member will need to wait before being able to remove a mute.

    To exit edit mode use /cancel
command-configuration-welcome-settime-no_number = It doesn't look like an integer, try again.
command-configuration-welcome-settime-limit = The number of seconds must satisfy the condition "0 <= time <= 300"
command-configuration-welcome-settime-set = New members will now have to wait { $seconds } seconds to unlock the unmute button.

command-configuration-members =
    {-configuration-title}
    {-configuration-title-members}

    { $name }, use the buttons below to control the chat.

command-configuration-members-lang =
    {-configuration-title}
    {-configuration-title-members}
    {-configuration-title-members-lang}

    { $name }, use the buttons below to control the chat.
