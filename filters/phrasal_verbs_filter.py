from aiogram.types import CallbackQuery


def phrasal_verbs_filter(callback: CallbackQuery) -> bool:
    """"""
    phrasal_verbs_callbacks = "phrasal_verbs"
    message = callback.data
    return message == phrasal_verbs_callbacks
