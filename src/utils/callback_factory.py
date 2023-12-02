from aiogram.filters.callback_data import CallbackData


class CaptchaCallbackFactory(CallbackData, prefix="captcha"):
    """
    Обработка нажатия на кнопку в капче
    """
    date: int
    user: int
    chat: int


class FilterslistCallbackFactory(CallbackData, prefix="filter"):
    """
    Обработка нажатия на кнопку в списке филтьтров
    """
    filter_id: str
