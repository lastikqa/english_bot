from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from aiogram.types import CallbackQuery
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from filters.guess_words_filter import guess_word_filter
from aiogram.types import InputMediaAudio, BufferedInputFile

router = Router()


@router.callback_query(guess_word_filter)
async def process_guess_words(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    game_status = database.checking_user_game(user_id)
    game = Games(user_id, data="english_5k.json")
    answer = database.checking_answer(user_id)

    if callback.data == "/verbs":
        database.updating_user_game(user_id=user_id, game="verbs")
        question, variants, level, audio = game.gusesing_game(user_id)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/nouns":
        database.updating_user_game(user_id=user_id, game="nouns")
        question, variants, level, audio = game.gusesing_game(user_id)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/adjectives":
        database.updating_user_game(user_id, game="adjectives")
        question, variants, level, audio = game.gusesing_game(user_id)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/prepositions":
        database.updating_user_game(user_id, game="prepositions")
        question, variants, level, audio = game.gusesing_game(user_id)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/conjunctions":
        database.updating_user_game(user_id, game="conjunctions")
        question, variants, level, audio = game.gusesing_game(user_id)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == "/pronouns":
        database.updating_user_game(user_id, game="pronouns")
        question, variants, level, audio = game.gusesing_game(user_id)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                          caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)

    elif callback.data == answer and game_status != "v" and game_status != "word_constructor":
        database.updating_user_rating(user_id,)
        question, variants, level, audio = game.gusesing_game(user_id)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                                                caption=f"Level {level} \nWhats the right translation for '{question}'?"),
                                          reply_markup=keyboard)
    else:
        database.updating_user_rating(user_id, win=False)
    await callback.answer()
