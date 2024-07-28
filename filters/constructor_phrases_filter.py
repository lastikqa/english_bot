from aiogram.types import CallbackQuery
from english_bot_database.english_bot_database import EnglishBotDatabase


def constructor_phrases_filter(callback: CallbackQuery) -> bool:
    game = EnglishBotDatabase.checking_user_game(user_id=callback.from_user.id)
    return game == "v"