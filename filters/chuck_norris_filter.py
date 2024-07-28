from aiogram.types import CallbackQuery


def chuck_filter(callback: CallbackQuery) -> bool:
    """"""
    message = callback.data
    return message == "/chuck" or message == "/translation"