from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from aiogram.types import CallbackQuery
from games.games import Games
from filters.guess_words_filter import guess_word_filter
from aiogram.types import InputMediaAudio, BufferedInputFile

router = Router()


@router.callback_query(guess_word_filter)
async def process_guess_words(callback: CallbackQuery):
    user_id = callback.from_user.id
    game = Games(user_id, data="english_5k.json")
    database = game.database
    game_status = await database.checking_user_game()
    answer = await database.checking_answer()

    if callback.data in ("/verbs", "/nouns", "/numbers", "/adjectives", "/prepositions", "/conjunctions", "/pronouns") :
        await database.updating_user_game(game= callback.data.replace("/", ""))
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == answer and game_status != "phrase_constructor" and game_status != "word_constructor":
        await database.updating_user_rating()
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                                                caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)
    else:
        await database.updating_user_rating(win=False)
    await callback.answer()
