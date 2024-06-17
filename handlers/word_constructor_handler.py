from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from filters.word_constructor_filter import word_constructor_filter
router = Router()


@router.callback_query(word_constructor_filter)
async def processing_word_constructors(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    user_param = database.checking_user_game(user_id)
    gamer = Games(user_id, user_param)
    user_question = database.checking_question(user_id)
    user_variants = database.checking_user_variants(user_id)
    variants = database.checking_variants_for_user(user_id)
    game_status = database.checking_user_game(user_id)

    if game_status == "word_constructor" and callback.data in user_variants:
        try:
            user_variants.remove(callback.data)
            database.updating_user_variants(user_id, user_variants)
            if callback.data == "_":
                data = " "
                user_answer = (database.checking_user_answer(user_id=user_id) + data)
            else:
                user_answer = (database.checking_user_answer(user_id=user_id)+callback.data)
            database.updating_user_answer(user_id=user_id, user_answer=user_answer)
            user_variants = database.checking_user_variants(user_id)
            keyboard = create_inline_kb(3, default_menu, *user_variants)
            await callback.message.edit_text(text=f"{user_question} \n{user_answer} ", reply_markup=keyboard)
        except TelegramBadRequest:
            user_answer = database.checking_user_answer(user_id).strip()
            answer = database.checking_answer(user_id)
            if user_answer == answer:
                database.updating_user_answer(user_id)
                database.updating_user_rating(user_id)
                question, variants = gamer.word_constructor(user_id)
                keyboard = create_inline_kb(3, default_menu, *variants)
                await callback.message.edit_text(text=f"'{question}'", reply_markup=keyboard)
            else:
                database.updating_user_answer(user_id)
                database.updating_user_variants(user_id, variants)
                database.updating_user_rating(user_id, win=False)
                keyboard = create_inline_kb(3, default_menu, *variants)
                await callback.message.edit_text(text=f"'{user_question}'", reply_markup=keyboard)

    await callback.answer()
