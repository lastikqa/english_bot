from aiogram.types import CallbackQuery


def main_menu_filter(callback: CallbackQuery) -> bool:
    """the filter checks callback in the list of main_menu callbacks"""
    callback_main_menu_list = ["menu_button", "guess_word", "word_constructor", "/v", "/chuck"]
    message = callback.data
    return message in callback_main_menu_list
