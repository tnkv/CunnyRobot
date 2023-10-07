def inflect_with_num(number: int, forms: tuple[str, str, str]) -> str:
    # 0 - 1 секунда
    # 1 - 10 секунд
    # 2 - 2 секунды
    units = number % 10
    tens = number % 100 - units

    if tens == 10 or units >= 5 or units == 0:
        needed_form = 1
    elif units > 1:
        needed_form = 2
    else:
        needed_form = 0

    return f'{number} {forms[needed_form]}'
