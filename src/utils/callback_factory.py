from aiogram.filters.callback_data import CallbackData


class CaptchaCallbackFactory(CallbackData, prefix="captcha"):
    """
    Обработка нажатия на кнопку в капче
    """
    date: int
    user: int
    chat: int

class DelwarnCallbackFactory(CallbackData, prefix="delwarn"):
    """
    Обработка удаления конкретного варна, по айди
    """
    warn_id: int
    user_id: int
