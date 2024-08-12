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

    if callback.data == "/verbs":
        await database.updating_user_game(game="verbs")
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/nouns":
        await database.updating_user_game(game="nouns")
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)
    elif callback.data == "/numbers":
        await database.updating_user_game(game="numbers")
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)
    elif callback.data == "/adjectives":
        await database.updating_user_game(game="adjectives")
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/prepositions":
        await database.updating_user_game(game="prepositions")
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/conjunctions":
        await database.updating_user_game(game="conjunctions")
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/pronouns":
        await database.updating_user_game(game="pronouns")
        question, variants, level, audio = await game.guessing_game()
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == answer and game_status != "v" and game_status != "word_constructor":
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
