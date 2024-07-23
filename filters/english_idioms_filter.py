from aiogram.types import CallbackQuery


def english_idioms_filter(callback: CallbackQuery) -> bool:
    """"""
    english_idiom = "/idioms"
    message = callback.data
    return message == english_idiom
