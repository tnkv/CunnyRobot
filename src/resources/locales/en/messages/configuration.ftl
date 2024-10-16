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
    Messages from users with administrator privileges will not be deleted. All messages go to lowercase before being checked.
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

    Following parameters can be used in the text for substitution:
    • <code>{"{user}"}</code> — for user mention
    • <code>{"{user_name}"}</code> — for user name
    • <code>{"{user_id}"}</code> — for user ID.
    • <code>{"{chat_title}"}</code> — for chat title
    • <code>{"{timestamp}"}</code> — UNIX Timestamp.

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
