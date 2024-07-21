from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import start_keyboard, guess_word_keyboard, default_menu
from aiogram.types import CallbackQuery
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from filters.main_menu_filters import main_menu_filter

router = Router()


@router.callback_query(main_menu_filter)
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    user_param = database.checking_user_game(user_id)
    gamer = Games(user_id, user_param)
    language = database.checking_user_translation(user_id)
    if callback.data == "menu_button":
        database.updating_user_game(user_id)
        keyboard = create_inline_kb(1, **start_keyboard)
        await callback.message.edit_text(text="Hello. Choose something", reply_markup=keyboard)

    if callback.data == "guess_word":
        keyboard = create_inline_kb(2, last_btn=default_menu, **guess_word_keyboard)
        await callback.message.edit_text(text="Choose parts of speech", reply_markup=keyboard)

    if callback.data == "word_constructor":
        database.updating_user_answer(user_id)
        question, variants = gamer.word_constructor(user_id)
        keyboard = create_inline_kb(3, default_menu, *variants)
        await callback.message.edit_text(text=f"'{question}'", reply_markup=keyboard)

    if callback.data == "/v":
        database.updating_user_answer(user_id)
        variants, question = gamer.constructor_phrases(user_id=user_id, language=language)
        keyboard = create_inline_kb(2, default_menu, *variants)
        await callback.message.edit_text(text=f"'{question}'", reply_markup=keyboard)

    await callback.answer()
