from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from aiogram.types import CallbackQuery
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from filters.guess_words_filter import guess_word_filter

router = Router()


@router.callback_query(guess_word_filter)
async def process_guess_words(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    user_param = database.checking_user_game(user_id)
    gamer = Games(user_id, user_param)
    game_status = database.checking_user_game(user_id)
    answer = database.checking_answer(user_id)

    if callback.data == "/g":
        user_param = "g"  # verbs
        question, variants = gamer.gusesing_game(user_id, user_param)
        keyboard = create_inline_kb(2, default_menu, *variants)
        await callback.message.edit_text(text=f"Whats the right translation for '{question}'?", reply_markup=keyboard)

    if callback.data == "/s":
        user_param = "s"
        question, variants = gamer.gusesing_game(user_id, user_param)
        keyboard = create_inline_kb(2, default_menu, *variants)
        await callback.message.edit_text(text=f"Whats the right translation for '{question}'?", reply_markup=keyboard)

    if callback.data == "/c":
        user_param = "c"
        question, variants = gamer.gusesing_game(user_id, user_param)
        keyboard = create_inline_kb(2, default_menu, *variants)
        await callback.message.edit_text(text=f"Whats the right translation for '{question}'?", reply_markup=keyboard)

    if callback.data == "/p":
        user_param = "p"
        question, variants = gamer.gusesing_game(user_id, user_param)
        keyboard = create_inline_kb(2, default_menu, *variants)
        await callback.message.edit_text(text=f"Whats the right translation for '{question}'?", reply_markup=keyboard)

    if callback.data == "/m":
        user_param = "m"
        question, variants = gamer.gusesing_game(user_id, user_param)
        keyboard = create_inline_kb(2, default_menu, *variants)
        await callback.message.edit_text(text=f"Whats the right translation for '{question}'?", reply_markup=keyboard)

    if callback.data == answer and game_status != "v" and game_status != "word_constructor":
        database.updating_user_rating(user_id,)
        question, variants = gamer.gusesing_game(user_id, user_param)
        keyboard = create_inline_kb(2, default_menu, *variants)
        await callback.message.edit_text(text=f"Whats the right translation for '{question}'?", reply_markup=keyboard)
    else:
        database.updating_user_rating(user_id, win=False)
    await callback.answer()
