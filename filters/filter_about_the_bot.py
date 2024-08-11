from aiogram.types import CallbackQuery


def about_the_bot_filter(callback: CallbackQuery) -> bool:
    """"""
    callbacks = ["/bot_commands", "/guess_words", "/constructor_games", "/about_the_bot", "/rating"]
    message = callback.data
    return message in callbacks
