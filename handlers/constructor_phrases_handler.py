from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from filters.constructor_phrases_filter import constructor_phrases_filter
router = Router()


@router.callback_query(constructor_phrases_filter)
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    user_param = database.checking_user_game(user_id)
    gamer = Games(user_id, data="english_5k.json")
    user_question = database.checking_question(user_id)
    user_variants = database.checking_user_variants(user_id)
    variants = database.checking_variants_for_user(user_id)
    game_status = database.checking_user_game(user_id)
    language = database.checking_user_translation(user_id)

    if game_status == "v" and callback.data in user_variants:
        try:
            user_variants.remove(callback.data)
            database.updating_user_variants(user_id, user_variants)
            user = (database.checking_user_answer(user_id=user_id)+" "+callback.data)
            database.updating_user_answer(user_id=user_id, user_answer=user)
            user = database.checking_user_variants(user_id)
            user_ans = database.checking_user_answer(user_id)
            keyboard = create_inline_kb(2, default_menu, *user)
            await callback.message.edit_text(text=f"{user_question} \n{user_ans}", reply_markup=keyboard)
        except TelegramBadRequest:
            user_answer = database.checking_user_answer(user_id).strip()
            answer = database.checking_answer(user_id)
            if user_answer == answer and len(user_variants) == 0:
                database.updating_user_answer(user_id)
                win = (database.checking_counter_user_score(user_id=user_id)) + 1
                database.updating_score_count(user_id=user_id, win=win)
                variants, question = gamer.constructor_phrases(user_id=user_id, language=language)
                keyboard = create_inline_kb(2, default_menu, *variants)
                await callback.message.edit_text(text=f"'{question}'", reply_markup=keyboard)
            else:
                database.updating_user_answer(user_id)
                user_score = database.checking_user_score(user_id=user_id)
                counter_user_score = database.checking_counter_user_score(user_id=user_id)
                database.updating_user_variants(user_id, variants)
                if counter_user_score > user_score:
                    database.updating_user_score(user_id=user_id, counter=counter_user_score)
                database.updating_score_count(user_id=user_id)
                keyboard = create_inline_kb(2, default_menu, *variants)
                await callback.message.edit_text(text=f"'{user_question}'", reply_markup=keyboard)
    await callback.answer()
