from aiogram.types import CallbackQuery
from english_bot_database.english_bot_database import EnglishBotDatabase


async def guess_word_filter(callback: CallbackQuery) -> bool:

    guess_words_callbacks = ["/verbs", "/nouns", "/numbers", "/adjectives",
                             "/conjunctions", "/prepositions", "/pronouns"]
    game_status = ["verbs", "nouns", "numbers", "adjectives", "conjunctions", "prepositions", "pronouns"]
    gamer = EnglishBotDatabase(user_id=callback.from_user.id)
    game = await gamer.checking_user_game()

    message = callback.data
    return game in game_status or message in guess_words_callbacks
