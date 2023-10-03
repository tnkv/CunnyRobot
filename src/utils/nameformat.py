from aiogram.utils.markdown import html_decoration


def nameFormat(UserID: int, userName, firstName, surName, isLink=True) -> str:  # Форматирование имени в зависимости от наличия юзернейма, фамилии итд
    if userName is not None:
        return f'<a href="tg://user?id={UserID}">@{userName}</a>' if isLink else f'@{userName}'
    elif surName is not None:
        return f'<a href="tg://user?id={UserID}">{html_decoration.quote(firstName)} {html_decoration.quote(surName)}</a>' if isLink else f'{html_decoration.quote(firstName)} {html_decoration.quote(surName)}'
    return f'<a href="tg://user?id={UserID}">{html_decoration.quote(firstName)}</a>' if isLink else f'{html_decoration.quote(firstName)}'
