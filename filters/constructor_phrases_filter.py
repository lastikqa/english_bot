from aiogram.types import CallbackQuery
from english_bot_database.english_bot_database import EnglishBotDatabase


async def constructor_phrases_filter(callback: CallbackQuery) -> bool:
    gamer = EnglishBotDatabase(user_id=callback.from_user.id)
    game = await gamer.checking_user_game()
    return game == "v"