from aiogram.types import CallbackQuery


def abnormal_verbs_filter(callback: CallbackQuery) -> bool:
    """"""
    abnormal_verbs_callbacks = "abnormal_verbs"
    message = callback.data
    return message == abnormal_verbs_callbacks
